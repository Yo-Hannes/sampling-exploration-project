import numpy
from otree.api import *
from numpy import random
import random
import settings

 

author = 'Johannes Leder'

doc = """
This experiment consists of two stages: explore and exploit stage. In the explore stage the player can explore for as many rounds as she wants.
Leaving the explore stage, the exploitation stage starts. The exploitation stage is 100 trials long. Here the player can choose between A and B, 
receives feedback about the choosen alternative and can receive information about the forgone payoff for an fee (FIC = forgone information cost). The player can switch between 
A and B, but this comes at an additional cost (SWC = switchting cost)
"""


class Constants(BaseConstants):
    name_in_url = 'comprehension_stage'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    quiz1 = models.IntegerField(label='What is the cost for information?')
    quiz2 = models.IntegerField(label="What is the cost for switching between options?")
    quiz3 = models.BooleanField(label="Do you have to pay to choose the same option twice?")


## PAGES ####

class Comprehension(Page):
    form_model = 'player'
    form_fields = ['quiz1', 'quiz2', 'quiz3']
    @staticmethod
    def is_displayed(player):
       return player.round_number == 1 #or player.consent == "non" 
    
    def error_message(player: Player, values):
        solutions = dict(quiz1=player.session.config['information_cost'], quiz2=player.session.config['switching_cost'], quiz3=False)
        if values != solutions:
            return "One or more answers were incorrect."    
   

class Results(Page):
    pass


page_sequence = [Comprehension, Results]