from content import watches
from engine import commands, state as st
from engine.io import ScriptedIO


def _fresh():
    return st.new_game("Halvard")


def test_parse_splits_command_and_argument():
    assert commands.parse("eye vs-0088") == ("EYE", "vs-0088")
    assert commands.parse("  scan  ") == ("SCAN", "")
    assert commands.parse("") == ("", "")


def test_unknown_command_is_answered_not_crashed():
    io = ScriptedIO()
    state, signal = commands.dispatch(_fresh(), "DANCE", io)
    assert signal is None
    assert any("UNRECOGNISED" in text for _, text in io.said)


def test_scan_sets_watch_flag_and_draws_the_plot():
    io = ScriptedIO()
    state, _ = commands.dispatch(_fresh(), "SCAN", io)
    assert st.has_flag(state, "SCANNED_1")
    assert any(kind == "art" and "┌" in text for kind, text in io.said)


def test_diff_requires_a_scan_first():
    io = ScriptedIO()
    state, _ = commands.dispatch(_fresh(), "DIFF", io)
    assert not st.has_flag(state, "DIFFED_1")
    assert any("RUN SCAN FIRST" in text for _, text in io.said)


def test_journal_write_records_the_players_own_words():
    io = ScriptedIO(answers=["the kettle sang early tonight.", "."])
    state, _ = commands.dispatch(_fresh(), "JOURNAL WRITE", io)
    assert len(state.journal) == 1
    assert state.journal[0].text == "the kettle sang early tonight."


def test_journal_read_replays_entries_inside_pages():
    state = st.add_journal(_fresh(), "the kettle sang early tonight.")
    io = ScriptedIO()
    state, _ = commands.dispatch(state, "JOURNAL READ", io)
    transcript = io.transcript()
    assert "WATCH 1" in transcript
    assert "kettle" in transcript


def test_journal_fade_never_touches_current_watch():
    assert watches.journal_fade(7, 7) == 0.0
    assert watches.journal_fade(4, 1) == 0.0
    assert watches.journal_fade(6, 1) > watches.journal_fade(6, 5)


def test_sleep_signals_the_shell():
    io = ScriptedIO()
    _, signal = commands.dispatch(_fresh(), "SLEEP", io)
    assert signal == "sleep"


def test_answer_refused_before_the_question():
    io = ScriptedIO()
    state, signal = commands.dispatch(_fresh(), "ANSWER", io)
    assert signal is None
    assert state.ending is None
    assert any("NO CHANNEL" in text for _, text in io.said)


def test_help_hides_the_door_until_late():
    io_early = ScriptedIO()
    commands.dispatch(_fresh(), "HELP", io_early)
    assert "OUTSIDE" not in io_early.transcript()


def test_single_letter_aliases_resolve():
    assert commands.parse("s")[0] == "SCAN"
    assert commands.parse("e the lantern") == ("EYE", "the lantern")
    assert commands.parse("?")[0] == "HELP"


def test_deep_night_acts_cost_and_duties_are_free():
    io = ScriptedIO()
    state = _fresh()
    state, _ = commands.dispatch(state, "SCAN", io)
    state, _ = commands.dispatch(state, "STATUS", io)
    assert state.acts == 0
    state, _ = commands.dispatch(state, "WALK dome", io)
    state, _ = commands.dispatch(state, "LISTEN", io)
    assert state.acts == 2


def test_invalid_targets_cost_nothing():
    io = ScriptedIO()
    state = _fresh()
    state, _ = commands.dispatch(state, "WALK nowhere", io)
    state, _ = commands.dispatch(state, "EYE VS-9999", io)
    state, _ = commands.dispatch(state, "TEND teapot", io)
    assert state.acts == 0


def test_fatigue_prose_past_the_budget():
    import dataclasses
    io = ScriptedIO()
    state = dataclasses.replace(_fresh(), acts=st.NIGHT_BUDGET)
    state, _ = commands.dispatch(state, "WALK dome", io)
    assert "short coat" in io.transcript()


def test_final_watch_is_exempt_from_fatigue():
    import dataclasses
    io = ScriptedIO()
    state = dataclasses.replace(_fresh(), watch=9, acts=st.NIGHT_BUDGET + 2)
    state, _ = commands.dispatch(state, "WALK dome", io)
    assert "short coat" not in io.transcript()


def test_journal_copy_restores_all_but_one_word():
    import dataclasses
    from engine import draw
    state = st.add_journal(_fresh(), "the kettle sang early and i thought "
                                     "of the pier and the sun on the water")
    state = dataclasses.replace(state, watch=7)
    io = ScriptedIO()
    state, _ = commands.dispatch(state, "JOURNAL COPY", io)
    living = st.living_journal(state)
    assert len(living) == 1
    _, fresh_entry = living[0]
    assert fresh_entry.watch == 7
    holes = sum(1 for tok in fresh_entry.text.split()
                if draw.GONE_CHAR in tok)
    assert holes == 1
    assert "RESTORED:" in io.transcript()
    assert state.acts == 1


def test_journal_copy_with_nothing_faded_is_free():
    state = st.add_journal(_fresh(), "fresh ink tonight")
    io = ScriptedIO()
    state, _ = commands.dispatch(state, "JOURNAL COPY", io)
    assert state.acts == 0
    assert "NO PAGE NEEDS THE PEN" in io.transcript()


def test_journal_write_offers_a_watch_specific_pen_prompt():
    import dataclasses
    io = ScriptedIO(answers=["the name is still mine.", "."])
    state = dataclasses.replace(_fresh(), watch=6)
    state, _ = commands.dispatch(state, "JOURNAL WRITE", io)
    assert "write the name you still have" in io.transcript()


def test_unlisted_verbs_answer_without_costing_the_night():
    io = ScriptedIO()
    state = _fresh()
    state, signal = commands.dispatch(state, "TEA", io)
    assert signal is None
    assert state.acts == 0
    assert "kettle" in io.transcript()
    io2 = ScriptedIO()
    state, _ = commands.dispatch(state, "TEA", io2)
    assert "only so deep" in io2.transcript()  # second cup refused
    io3 = ScriptedIO()
    state, _ = commands.dispatch(state, "XYZZY", io3)
    assert "NOTHING HAPPENS." in io3.transcript()


def test_repeat_listen_is_short_and_free():
    io = ScriptedIO()
    state = _fresh()
    state, _ = commands.dispatch(state, "LISTEN", io)
    acts_after_first = state.acts
    state, _ = commands.dispatch(state, "LISTEN", io)
    assert state.acts == acts_after_first
    assert any("gave" in t or "door" in t for _, t in io.said)


def test_repeat_walk_and_tend_are_short_and_free():
    io = ScriptedIO()
    state = _fresh()
    state, _ = commands.dispatch(state, "WALK dome", io)
    state, _ = commands.dispatch(state, "TEND CLOCK", io)
    acts = state.acts
    state, _ = commands.dispatch(state, "WALK dome", io)
    state, _ = commands.dispatch(state, "TEND CLOCK", io)
    assert state.acts == acts
    assert "SERVICED THIS WATCH" in io.transcript()


def test_unknown_command_lines_vary_with_state():
    import dataclasses
    lines = set()
    for acts in range(4):
        io = ScriptedIO()
        state = dataclasses.replace(_fresh(), acts=acts)
        commands.dispatch(state, "DANCE", io)
        lines.add(io.said[-1][1])
    assert len(lines) >= 3


def test_journal_write_survives_input_running_dry():
    # regression: EOF mid-entry used to loop forever appending QUIT
    io = ScriptedIO(answers=["the kettle sang early tonight"])  # no "."
    state, _ = commands.dispatch(_fresh(), "JOURNAL WRITE", io)
    assert len(state.journal) == 1
    assert state.journal[0].text == "the kettle sang early tonight"
    io2 = ScriptedIO(answers=[])  # dry immediately
    state2, _ = commands.dispatch(_fresh(), "JOURNAL WRITE", io2)
    assert len(state2.journal) == 0


def test_answer_prompt_eof_sits_back_instead_of_sending():
    import dataclasses
    state = dataclasses.replace(st.add_flag(_fresh(), "QUESTION_ASKED"),
                                watch=9)
    io = ScriptedIO(answers=[])
    state, signal = commands.dispatch(state, "ANSWER", io)
    assert signal is None
    assert state.ending is None


def test_diff_rows_never_exceed_wrap_width():
    import dataclasses
    io = ScriptedIO()
    state = dataclasses.replace(_fresh(), watch=8)
    state, _ = commands.dispatch(state, "SCAN", io)
    state, _ = commands.dispatch(state, "DIFF", io)
    rows = [t for k, t in io.said if k == "os" and "└" in t or "NO SUCH" in t]
    assert rows
    assert all(len(t) <= 78 for t in rows)
