import dataclasses
import json

import pytest

from engine import persistence, state as st


@pytest.fixture()
def home(tmp_path, monkeypatch):
    monkeypatch.setenv("VESPER_HOME", str(tmp_path))
    return tmp_path


def _played_state():
    game = st.new_game("Halvard")
    game = st.add_flag(game, "SCANNED_1", "REPORTED_1")
    game = st.add_journal(game, "the tea was cold before i finished it.")
    game = st.witness(game, "VS-0117")
    game = dataclasses.replace(game, watch=3)
    game = st.tend(game, "PLANT")
    return game


def test_roundtrip_preserves_everything(home):
    before = _played_state()
    persistence.save(before)
    after = persistence.load()
    assert after == before


def test_load_returns_none_when_no_save_exists(home):
    assert persistence.load() is None


def test_corrupt_json_raises_save_error(home):
    persistence.save(_played_state())
    persistence.save_path().write_text("{ not json", encoding="utf-8")
    with pytest.raises(persistence.SaveError):
        persistence.load()


def test_wrong_schema_raises_save_error(home):
    persistence.save(_played_state())
    data = json.loads(persistence.save_path().read_text(encoding="utf-8"))
    data["schema"] = 99
    persistence.save_path().write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(persistence.SaveError):
        persistence.load()


def test_missing_field_raises_save_error(home):
    persistence.save(_played_state())
    data = json.loads(persistence.save_path().read_text(encoding="utf-8"))
    del data["journal"]
    persistence.save_path().write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(persistence.SaveError):
        persistence.load()


def test_unknown_ending_rejected(home):
    persistence.save(_played_state())
    data = json.loads(persistence.save_path().read_text(encoding="utf-8"))
    data["ending"] = "HAPPY"
    persistence.save_path().write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(persistence.SaveError):
        persistence.load()


def test_watch_out_of_range_rejected(home):
    persistence.save(_played_state())
    data = json.loads(persistence.save_path().read_text(encoding="utf-8"))
    data["watch"] = 100
    persistence.save_path().write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(persistence.SaveError):
        persistence.load()


def test_delete_is_idempotent(home):
    persistence.delete()
    persistence.save(_played_state())
    persistence.delete()
    assert persistence.load() is None


def test_schema_one_save_loads_with_defaults(home):
    persistence.save(_played_state())
    data = json.loads(persistence.save_path().read_text(encoding="utf-8"))
    data["schema"] = 1
    del data["acts"]
    del data["final_words"]
    data["journal"] = [[w, t] for w, t, _ in data["journal"]]
    persistence.save_path().write_text(json.dumps(data), encoding="utf-8")
    loaded = persistence.load()
    assert loaded.acts == 0
    assert loaded.final_words == ""
    assert loaded.journal[0].superseded is False


def test_ledger_roundtrip_and_corruption_tolerance(home):
    assert persistence.load_ledger() == []
    persistence.append_ledger("Josef", "KEEPER", 9)
    persistence.append_ledger("Josef", "ANSWER", 9)
    runs = persistence.load_ledger()
    assert [r["ending"] for r in runs] == ["KEEPER", "ANSWER"]
    persistence.ledger_path().write_text("{ broken", encoding="utf-8")
    assert persistence.load_ledger() == []
