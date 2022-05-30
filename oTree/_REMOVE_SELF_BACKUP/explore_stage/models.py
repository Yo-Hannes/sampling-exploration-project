from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)


author = 'Johannes Leder'

doc = """
This experiment consists of two stages: explore and exploit stage. In the explore stage the player can explore for as many rounds as she wants.
Leaving the explore stage, the exploitation stage starts. The exploitation stage is 100 trials long. Here the player can choose between A and B, 
receives feedback about the choosen alternative and can receive information about the forgone payoff for an fee (FIC = forgone information cost). The player can switch between 
A and B, but this comes at an additional cost (SWC = switchting cost)
"""


class Constants(BaseConstants):
    name_in_url = 'explore_exploit_experiment'
    players_per_group = None
    num_rounds = 100
    switching_cost = 5


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    #gender = models.StringField()
    age = models.IntegerField()
    number_exploration = models.IntegerField(initial=0)
    choice_a = models.BooleanField(initial=False)
    outcome_a = models.IntegerField(initial=-99)
    outcome_b = models.IntegerField(initial=-99)
    information_choice_a = models.BooleanField(initial=False) # only relevant for exploitation stage
    information_choice_b = models.BooleanField(initial=False) # only relevant for exploitation stage

    def determine_outcome(player):
        if self.choice_a == False:
            self.outcome_a = ""
            self.outcome_b = self.outcome_b 
        else: 
            self.outcome_a = self.outcome_a
            self.outcome_b = ""


