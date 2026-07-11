import dataclasses

import pytest

from engine import state as st


def test_gamestate_is_immutable():
    game = st.new_game("Halvard")
    with pytest.raises(dataclasses.FrozenInstanceError):
        game.watch = 5


def test_new_game_defaults_blank_name_to_the_observer():
    assert st.new_game("   ").observer == "the observer"
    assert st.new_game("Halvard").observer == "Halvard"


def test_add_flag_returns_new_state_without_touching_original():
    game = st.new_game("H")
    flagged = st.add_flag(game, "SCANNED_1")
    assert st.has_flag(flagged, "SCANNED_1")
    assert not st.has_flag(game, "SCANNED_1")


def test_journal_entries_record_the_watch_they_were_written_on():
    game = st.new_game("H")
    game = st.add_journal(game, "the tea was cold before i finished it.")
    game = st.next_watch(game)
    game = st.add_journal(game, "two more gone. i remember both.")
    assert [e.watch for e in game.journal] == [1, 2]


def test_tend_updates_only_the_named_thing():
    game = st.new_game("H")
    game = dataclasses.replace(game, watch=4)
    game = st.tend(game, "CLOCK")
    assert st.last_tended(game, "CLOCK") == 4
    assert st.last_tended(game, "GENERATOR") == 1


def test_tend_rejects_unknown_thing():
    with pytest.raises(ValueError):
        st.tend(st.new_game("H"), "TEAPOT")


def test_generator_warning_starts_at_watch_four_when_neglected():
    game = st.new_game("H")
    assert not st.generator_warning_active(game)
    game = dataclasses.replace(game, watch=3)
    assert not st.generator_warning_active(game)
    game = dataclasses.replace(game, watch=4)
    assert st.generator_warning_active(game)


def test_tending_generator_clears_warning_and_strikes():
    game = dataclasses.replace(st.new_game("H"), watch=4, generator_strikes=1)
    game = st.tend(game, "GENERATOR")
    assert not st.generator_warning_active(game)
    assert game.generator_strikes == 0


def test_two_ignored_warning_sleeps_become_fatal():
    game = dataclasses.replace(st.new_game("H"), watch=4)
    game = st.record_sleep_strikes(game)
    assert not st.generator_is_fatal(game)
    game = st.next_watch(game)
    game = st.record_sleep_strikes(game)
    assert st.generator_is_fatal(game)


def test_sleep_with_no_active_warning_resets_strikes():
    game = dataclasses.replace(st.new_game("H"), watch=4, generator_strikes=1)
    game = st.tend(game, "GENERATOR")
    game = st.record_sleep_strikes(game)
    assert game.generator_strikes == 0


def test_set_ending_accepts_only_known_endings():
    game = st.new_game("H")
    assert st.set_ending(game, "KEEPER").ending == "KEEPER"
    with pytest.raises(ValueError):
        st.set_ending(game, "HAPPY")


def test_spend_act_increments_and_next_watch_resets():
    game = st.new_game("H")
    game = st.spend_act(st.spend_act(game))
    assert game.acts == 2
    assert st.next_watch(game).acts == 0


def test_supersede_hides_entry_from_living_journal():
    game = st.new_game("H")
    game = st.add_journal(game, "first")
    game = st.add_journal(game, "second")
    game = st.supersede_journal(game, 0)
    living = st.living_journal(game)
    assert [e.text for _, e in living] == ["second"]
    assert len(game.journal) == 2
