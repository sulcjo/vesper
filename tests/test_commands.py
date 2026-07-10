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
