#!/usr/bin/env python2.7

# Standard libs
import random

# External libs
from game import Game
from player import Bot 

class StrayBot(Bot):

    def onGameRevealed(self, players, spies):
        self.players = players
        self.spies = spies

        # Bind spy/resistance versions of API methods
        self._select = { True  : self._selectAsSpy,
                         False : self._selectAsResistance }
        self._vote   = { True  : self._voteAsSpy,
                         False : self._voteAsResistance }

    def select(self, players, count):
        return self._select[self.spy](players, count)

    def _selectAsResistance(self, players, count):
        me = [p for p in players if p.index == self.index][0]
        my_list_index = players.index(me)

        # Select me and the upcoming leaders
        team = [me]
        for i in range(1, count):
            team.append(players[(my_list_index + i) % len(players)])

        return team

    def _selectAsSpy(self, players, count):
        return self._selectAsResistance(players, count)

    def vote(self, team):
        return self._vote[self.spy](team)

    def _voteAsResistance(self, team):
        return True

    def _voteAsSpy(self, team):
        # If we need to sabotage the next mission
        if self.game.wins + 1 >= Game.NUM_WINS:
            # Vote yes if there are spies on the team
            # Vote no if there aren't any spies on the team
            return len([p for p in self.game.team if p in self.spies]) > 0

        # Otherwise, vote counter to our actual interests until we need to
        # play our hand

        # Vote no if there are spies on the team
        # Vote yes if there aren't any spies on the team
        return len([p for p in self.game.team if p in self.spies]) == 0

    def sabotage(self):
        # Sabotage for the win
        if self.game.losses + 1 >= Game.NUM_LOSSES:
            return True

        # If the resistance hasn't successfully completed any missions yet
        if self.game.wins == 0:
            # Pass this mission to gain some trust
            return False

        # If I'm the only spy on the mission, sabotage!
        if len([p for p in self.game.team if p in self.spies]) == 1:
            return True

        # There are multiple spies on the team
        # Flip a coin to fail it
        return random.random() <= 0.5
