"""TEND — the three things that need him.

The generator keeps him alive. The clock keeps him regular. The plant
keeps him kind. None of this is stated; it is what the scenes are for.
"""

from __future__ import annotations

from engine import draw, state as st
from engine.io import IO
from engine.state import GameState

THINGS = ("GENERATOR", "CLOCK", "PLANT")


def generator_fraction(state: GameState) -> float:
    age = state.watch - st.last_tended(state, "GENERATOR")
    return max(0.1, 1.0 - 0.28 * age)


def plant_fraction(state: GameState) -> float:
    age = state.watch - st.last_tended(state, "PLANT")
    return max(0.2, 1.0 - 0.2 * age)


def tend(state: GameState, thing: str, io: IO) -> GameState:
    thing = thing.strip().upper()
    if thing not in THINGS:
        io.say(f"TEND: {thing or '(NOTHING)'} IS NOT A STATION SYSTEM.", "os")
        io.say("the station's needs are short: the generator, the clock, "
               "the plant. so are yours, these days.", "dim")
        return state
    warned = st.generator_warning_active(state)
    state = st.tend(state, thing)
    scene = {"GENERATOR": _generator, "CLOCK": _clock, "PLANT": _plant}[thing]
    scene(state, io, warned)
    return state


def _generator(state: GameState, io: IO, warned: bool) -> None:
    io.say("GENERATOR ROOM — MAINTENANCE CYCLE", "os")
    if warned:
        io.say("the stumble in the rotation is audible from the corridor "
               "now, a heartbeat with a held breath in it. you bleed "
               "the lines — fuel oil threading down your wrist, warm "
               "as blood and stubborn under the nails for days — swap "
               "the fouled injector, and stand with your palm flat on "
               "the housing, eyes shut, until the rhythm comes back "
               "true under your hand like a fever breaking.")
        io.say("it would have stopped. you know the sound of it deciding. "
               "an untended generator on a cold watch is not a mishap, "
               "out here; it is a decision made by not making it.")
    else:
        io.say("filters, feed lines, the slow warm smell of fuel oil. the "
               "generator does not need you tonight, but machines that "
               "are only visited when they scream learn to scream. your "
               "father said that about dogs. it holds for everything.")
    io.art(["  " + draw.render_gauge("GENERATOR", generator_fraction(state))])
    io.say("GENERATOR NOMINAL.", "os")


def _clock(state: GameState, io: IO, warned: bool) -> None:  # noqa: ARG001
    io.say("QUARTERS — THE CLOCK", "os")
    io.say("the key is brass, cross-hatched where a hundred years of "
           "finger and thumb have gripped it, and it turns stiff for "
           "the first three and sweet for the rest. eleven turns, "
           "never twelve, the spring taken just shy of its temper — "
           "you can feel the temper coming, a gathering refusal in "
           "the metal, and you stop the turn a breath before it the "
           "way you were taught. the numerals are in a script nobody "
           "has read aloud in living memory, which is fine. the "
           "clock is not for reading. it is for the tick.")
    if state.watch >= 6:
        io.say("the tick divides the dark into pieces small enough to "
               "carry. lately you have caught yourself counting along, "
               "and stopping yourself, because counting along is what "
           "the east does, and you will not give it the satisfaction.",
               "dim")
    io.say("CLOCK WOUND.", "os")


def _plant(state: GameState, io: IO, warned: bool) -> None:  # noqa: ARG001
    io.say("PLANT ROOM — WATERING", "os")
    if state.watch >= 8:
        io.say("there is a new leaf. now. of all the epochs it could have "
               "chosen, with the east of the sky standing open like a "
               "removed tooth, the plant has decided on a new leaf, pale "
               "as paper, aimed with total confidence at the grow-lamp.")
        io.say("it believes in a sun it has never seen. you stand in the "
               "green smell for longer than the watering strictly takes.")
    else:
        io.say("half a measure, poured slow at the roots. the water "
               "disappears into the gravel with a small ticking, like "
               "far-off doors closing one by one, and the green smell "
               "lifts — sharper for a moment, the plant's one word. "
               "it is the only thing on the station younger than you, "
               "and the only thing aboard that takes without asking "
               "and gives nothing back but that smell. you have had "
               "worse colleagues.")
    io.art(["  " + draw.render_gauge("MOISTURE", plant_fraction(state))])
    io.say("HYDROPONICS NOMINAL.", "os")
