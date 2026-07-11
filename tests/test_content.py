"""Content integrity plus full scripted playthroughs of every ending."""

from content import catalog, endings, watches
from engine import commands, shell, state as st
from engine.io import ScriptedIO
from engine.state import ENDINGS, FINAL_WATCH


# ── catalogue integrity ───────────────────────────────────────────────

def test_designations_are_unique():
    ids = [s.id for s in catalog.ALL]
    assert len(ids) == len(set(ids))


def test_positions_are_unique_and_inside_the_plot():
    cells = [(s.x, s.y) for s in catalog.ALL]
    assert len(cells) == len(set(cells))
    for star in catalog.ALL:
        assert 0 <= star.x < catalog.SKY_WIDTH
        assert 0 <= star.y < catalog.SKY_HEIGHT


def test_removals_are_scheduled_on_playable_watches():
    for star in catalog.ALL:
        if star.gone is not None:
            assert 2 <= star.gone <= FINAL_WATCH - 1


def test_every_watch_after_the_first_loses_something():
    for watch in range(2, FINAL_WATCH):
        assert any(s.gone == watch for s in catalog.ALL), watch


def test_names_resolve_case_insensitively():
    assert catalog.by_id("the lantern").id == "VS-0088"
    assert catalog.by_id("vs-0088").id == "VS-0088"
    assert catalog.by_id("VS-9999") is None


def test_witnessed_star_is_retained_on_its_removal_watch_only():
    import dataclasses
    star = catalog.by_id("VS-0301")  # gone on watch 3
    game = st.witness(st.new_game("H"), star.id)
    game3 = dataclasses.replace(game, watch=3)
    game4 = dataclasses.replace(game, watch=4)
    assert catalog.is_visible(star, game3)
    assert not catalog.is_visible(star, game4)


def test_the_front_erases_the_east_on_the_final_watch():
    import dataclasses
    game = dataclasses.replace(st.new_game("H"), watch=FINAL_WATCH)
    for x, _, _ in catalog.visible_stars(game):
        assert x < catalog.FRONT_RECT[0]


def test_all_endings_have_scenes():
    assert set(endings._SCENES) == set(ENDINGS)


def test_every_watch_has_a_waking():
    assert set(watches._WAKES) == set(range(1, FINAL_WATCH + 1))


# ── playthroughs ─────────────────────────────────────────────────────

def _play(script: list[str], answers: list[str] | None = None):
    io = ScriptedIO(answers)
    state = st.new_game("Halvard")
    state = watches.wake(state, io)
    for line in script:
        state, signal = commands.dispatch(state, line, io)
        if signal == "sleep":
            state = shell.advance_after_sleep(state, io)
        if state.ending is not None:
            endings.play(state, io)
            return state, io
    return state, io


FULL_WATCH = ["SCAN", "DIFF", "EYE the Lantern", "LISTEN",
              "TEND GENERATOR", "REPORT", "SLEEP"]

# survive to watch 8 with minimal effort: tend the generator just
# often enough that no two consecutive sleeps carry an active warning
_TO_WATCH_8 = (["SLEEP"] * 3
               + ["TEND GENERATOR", "SLEEP", "SLEEP"]
               + ["TEND GENERATOR", "SLEEP", "SLEEP"])


def test_keeper_ending_full_dutiful_run():
    script = FULL_WATCH * 8 + ["SCAN", "DIFF", "REPORT", "SLEEP"]
    state, io = _play(script, answers=["the count is mine.", "."])
    assert state.ending == "KEEPER"
    assert "STILL THERE. STILL HERE." in io.transcript()


def test_quiet_ending_by_burning_the_journal():
    script = FULL_WATCH * 8 + ["JOURNAL BURN"]
    state, io = _play(script, answers=["BURN"])
    assert state.ending == "QUIET"
    assert "NO ACTION FOLLOWS." in io.transcript()


def test_quiet_ending_by_lying_down_unreported():
    script = FULL_WATCH * 8 + ["SLEEP"]
    state, _ = _play(script)
    assert state.ending == "QUIET"


def test_answer_ending_by_keying_the_send():
    script = FULL_WATCH * 8 + ["LISTEN", "ANSWER"]
    state, io = _play(script, answers=["SEND"])
    assert state.ending == "ANSWER"
    assert "REMY" in io.transcript()


def test_cold_ending_after_two_ignored_warnings():
    state, io = _play(["SLEEP"] * 5)
    assert state.ending == "COLD"
    assert "NO OBSERVER OF RECORD" in io.transcript()


def test_outside_ending_by_override():
    script = _TO_WATCH_8 + ["OUTSIDE", "OUTSIDE"]
    state, io = _play(script)
    assert state.ending == "OUTSIDE"
    assert "OVERRIDE" in io.transcript()


def test_outside_survivable_with_full_checks_and_sense():
    script = (_TO_WATCH_8
              + ["SUIT SEALS", "SUIT AIR", "SUIT TETHER", "OUTSIDE",
                 "TEND GENERATOR", "SLEEP",
                 "SCAN", "DIFF", "REPORT", "SLEEP"])
    state, _ = _play(script, answers=["RETURN"])
    assert state.ending == "KEEPER"
    assert st.has_flag(state, "WENT_OUTSIDE")


def test_the_wire_quotes_the_journal_back_on_watch_eight():
    script = (FULL_WATCH * 7) + ["JOURNAL WRITE", "LISTEN"]
    answers = ["the plant has a new leaf tonight.", "."]
    state, io = _play(script, answers=answers)
    transcript = io.transcript()
    assert "TRAFFIC COULD NOT BE LOGGED" in transcript


def test_shelf_lists_and_opens_the_volumes():
    io = ScriptedIO()
    state = st.new_game("Halvard")
    state, _ = commands.dispatch(state, "SHELF", io)
    assert "OKONKWO" in io.transcript()
    state, _ = commands.dispatch(state, "SHELF REMY", io)
    assert st.has_flag(state, "READ_REMY")
    assert "STILL THERE. STILL HERE." in io.transcript()


def test_the_pulse_goes_wrong_on_watch_seven():
    script = FULL_WATCH * 6 + ["LISTEN"]
    state, io = _play(script)
    assert st.has_flag(state, "HEARD_PULSE_WRONG")
    assert "DECREASING" in io.transcript()


def test_keeper_epilogue_replays_journal_unfaded():
    script = (FULL_WATCH * 8
              + ["JOURNAL WRITE", "SCAN", "DIFF", "REPORT", "SLEEP"])
    answers = ["the plant has a new leaf tonight.", "."]
    state, io = _play(script, answers=answers)
    assert state.ending == "KEEPER"
    transcript = io.transcript()
    assert "every word present. every word kept." in transcript
    assert "the plant has a new leaf tonight." in transcript
    assert "ANNOTATIONS IN YOUR HAND:" in transcript


def test_answer_transmits_and_decays_the_players_own_words():
    script = FULL_WATCH * 8 + ["LISTEN", "ANSWER"]
    state, io = _play(script, answers=["remember the pier"])
    assert state.ending == "ANSWER"
    assert state.final_words == "remember the pier"
    transcript = io.transcript()
    assert "“remember the pier,” you send" in transcript
    from engine import draw
    assert draw.GONE_CHAR in transcript


def test_sign_in_book_lists_previous_runs():
    from content import boot
    ledger = [{"name": "Josef", "ending": "KEEPER", "watch": 9}]
    io = ScriptedIO(answers=["Josef"])
    name = boot.sign_in(io, ledger)
    transcript = io.transcript()
    assert name == "Josef"
    assert "watch closed in good order" in transcript
    assert "you have never signed this book before" in transcript


def test_deaths_print_a_surviving_journal_fragment():
    script = (["JOURNAL WRITE"] + ["SLEEP"] * 5)
    state, io = _play(script, answers=["the kettle sang early tonight "
                                       "and i let it.", "."])
    assert state.ending == "COLD"
    assert "PAPER RECORD — UNFILED" in io.transcript()
