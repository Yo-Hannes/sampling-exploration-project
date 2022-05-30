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
    name_in_url = 'explore_stage'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    gender = models.StringField()
    age = models.IntegerField()
    consent = models.StringField(initial="non", blank=True)
    continue_button = models.BooleanField(initial=False, blank=True)
    number_exploration = models.IntegerField(initial=0)

    # sampling stage responses 
    left_choice_count = models.IntegerField(initial=0, blank=False)
    right_choice_count = models.IntegerField(initial=0, blank=False)
    choice_history = models.StringField(initial="", blank=True)
    choice_time = models.StringField(initial="", blank=True)
    a_payoff_history = models.StringField(initial="", blank=True)
    b_payoff_history = models.StringField(initial="", blank=True)
    explore_stop = models.BooleanField(initial=False)

    #added this to try sth
    final_choice = models.StringField(initial="non", blank=True)
    outcome_a = models.CurrencyField(initial=0)
    outcome_b = models.CurrencyField(initial=0)

    information_choice_a = models.BooleanField(initial=False) # only relevant for exploitation stage
    information_choice_b = models.BooleanField(initial=False) # only relevant for exploitation stage
    trial_payoff = models.CurrencyField(initial=1)
    total_payoff = models.CurrencyField(initial=0)


###### Functions ###################


def determine_outcome_shown(player):


    outcome_list_a = random.choices(
        list([player.session.config['payoff_high_a'],player.session.config['payoff_low_a']]),\
        weights = (player.session.config['probability_win_a'],1-player.session.config['probability_win_a']),
        k = 1
    )
    outcome_list_b = random.choices(
        list([player.session.config['payoff_high_b'],player.session.config['payoff_low_b']]),\
        weights = (player.session.config['probability_win_b'],1-player.session.config['probability_win_b']),
        k = 1
    )
    player.outcome_a = Currency(outcome_list_a[0])  # to create the same "luck" for all, use a seed?
    player.outcome_b = Currency(outcome_list_b[0])
    
    if player.choice_a == "b":
        player.outcome_b = player.outcome_b
        player.trial_payoff = player.outcome_b
    elif player.choice_a == "a": 
        player.outcome_a = player.outcome_a
        player.trial_payoff = player.outcome_a
    else :
        player.trial_payoff = 0

def calculate_trial_payoff(player):
    #prev_player = player.in_round(player.round_number - 1)
    if player.round_number > 1:
        prev_player = player.in_round(player.round_number - 1)
        player.total_payoff = prev_player.total_payoff + player.trial_payoff
    else : 
        player.total_payoff = player.trial_payoff

def display_final_decision(player):
    if player.explore_stop: # when pushing stop explore OR getting to the end of all rounds then set the return to true
        return True 
    else:
        return False
#def next_app(player):
 #   if player.explore_stop == True:
  #      player.round_number = 100


## PAGES ####

class Consent(Page):
    form_model = 'player'
    form_fields = ['consent', 'continue_button']
    @staticmethod
    def is_displayed(player):
       return player.round_number == 1
    
    def vars_for_template(player):
        return dict(consent = player.consent, continue_button = player.continue_button)


class Instruction(Page):
    @staticmethod
    def is_displayed(player):
       return player.round_number == 1 and player.consent == "yes" and player.continue_button == True
       
    def vars_for_template(player):
        return dict(information_cost = player.session.config['information_cost'], 
        switching_cost = player.session.config['switching_cost'],
        previous_choice = None)

class Instructions_Option1(Page):
    @staticmethod
    def is_displayed(player):
       #return player.round_number == 1
       return player.round_number == 1 and player.consent == "yes" and player.continue_button == True

       
    def vars_for_template(player):
        return dict(information_cost = player.session.config['information_cost'], 
        switching_cost = player.session.config['switching_cost'],
        previous_choice = None)

class Instructions_Option2(Page):
    @staticmethod
    def is_displayed(player):
       #return player.round_number == 1
        return player.round_number == 1 and player.consent == "yes" and player.continue_button == True

       
    def vars_for_template(player):
        return dict(information_cost = player.session.config['information_cost'], 
        switching_cost = player.session.config['switching_cost'],
        previous_choice = None)

class Instructions_Done_sampling(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1 and player.consent == "yes" and player.continue_button == True

       #return player.round_number == 1
       
    def vars_for_template(player):
        return dict(information_cost = player.session.config['information_cost'], 
        switching_cost = player.session.config['switching_cost'],
        previous_choice = None)


class Decide(Page):
    form_model = 'player'
    form_fields = ['left_choice_count', 'right_choice_count',
                   'choice_history', 'choice_time', "a_payoff_history", "b_payoff_history"]

    def vars_for_template(player):
        template_vars = {
            "symbols" : player.participant.vars["symbols"],
            "outcomes" : player.participant.vars["outcomes"],
            "payoff_a"  : [player.session.config['payoff_high_a'], player.session.config['payoff_low_a']],
            "probability_a" : player.session.config['probability_win_a'],
            "payoff_b"  : [player.session.config['payoff_high_b'], player.session.config['payoff_low_b']],
            "probability_b" : player.session.config['probability_win_b']
        }

        return template_vars


page_sequence = [Decide]
