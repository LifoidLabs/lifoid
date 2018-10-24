"""
Automaton definition: FSM based bot
Author:   Romary Dupuis <romary@me.com>
Copyright (C) 2017-2018 Romary Dupuis
"""
import json
from transitions.extensions import HierarchicalMachine as Machine
from awesomedecorators import timeit
from lifoid.bot import Bot


class Automaton(Bot):
    """
    IoT bot based on state-machine.
    State-machine is provided by https://github.com/pytransitions/transitions
    Various kind of "Machines" are available. By default `Automaton` implements
    `HierarchicalMachine`. GraphMachine can be used to get a visualization with
    PyGraphviz.
    JSON serialization methods allow to save and load state-machines.
    In cases where event dispatching is done in threads, one can use
    either LockedMachine or LockedHierarchicalMachine where function access
    (!sic) is secured with reentrant locks. This does not save you from
    corrupting your machine by tinkering with member variables of your model or
    state machine.

    """
    @classmethod
    def from_json(cls, json_dump):
        """
        Instantiates and returns an Automaton from a JSON object
        """
        ctxt = json.loads(json_dump)
        automaton = cls(ctxt['lifoid_id'])
        for k in ctxt:
            automaton[k] = ctxt[k]
        automaton.machine.set_state(automaton['__state__'])
        return automaton

    @timeit
    def load_machine(self, mtype, states, transitions, initial):
        """
        Builds and returns a state-machine along with time spent doing so.
        """
        return mtype(
            model=self,
            states=states,
            transitions=transitions,
            initial=initial,
            prepare_event='prepare',
            finalize_event='finalize'
        )

    def __init__(self, lifoid_id, mtype=Machine):
        super(Automaton, self).__init__(lifoid_id)
        self.machine, perf = self.load_machine(
            mtype,
            self.states,
            self.transitions,
            self.initial
        )
        self.logger.debug('Machine built in {}'.format(perf))
        self['__state__'] = self.state

    def finalize(self, _render, _message):
        """
        Always logs machine state after processing a message
        """
        self.logger.debug('State: {}'.format(self.state))

    def prepare(self, _render, _message):
        """
        Always logs machine state before processing a message
        """
        self.logger.debug('State: {}'.format(self.state))

    def to_json(self):
        """
        JSON serialization
        """
        self['__state__'] = self.state
        return json.dumps(self.copy())
