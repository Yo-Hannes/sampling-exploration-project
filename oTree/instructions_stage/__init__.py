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
    name_in_url = 'instructions_stage'
    players_per_group = None
    num_rounds = 20


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    gender = models.StringField()
    age = models.IntegerField()
    # (initial=False, blank= False)
    consent = models.BooleanField(
    label="Do you conset to this and want to participate?")
    continue_button = models.BooleanField(initial=False, blank=True)
    
    # decisions
    choice = models.StringField(initial="non", blank=True)
    information_cost_round = models.CurrencyField(initial = 0) # 0 - did not, 5 - did pick
    switching_cost_round = models.CurrencyField(initial = 0)


    # symbols
    symbol_on_button_left = models.StringField(initial="non", blank=True)
    symbol_on_button_right = models.StringField(initial="non", blank=True)

    # outcome
    outcome_on_button_left  = models.StringField(initial="non", blank=True)
    outcome_on_button_right = models.StringField(initial="non", blank=True)

    # payoff tracker 
    trial_payoff = models.CurrencyField(initial = 0)
    payout_left = models.CurrencyField(initial = 0)
    payout_right = models.CurrencyField(initial = 0)

###### Functions ###################

def creating_session(subsession):
    import random
    for player in subsession.get_players():
        # randomly assign symbols to buttons
        symbols = ['Kreis.png', 'Stern.png']
        random.shuffle(symbols)
        player.symbol_on_button_left = symbols[0]
        player.symbol_on_button_right = symbols[1]
        player.participant.vars["symbols"] = symbols[:]

        # randomly assign outcomes to buttons
        outcomes = ["a", "b"]
        random.shuffle(outcomes)
        player.outcome_on_button_left = outcomes[0]
        player.outcome_on_button_right = outcomes[1]
        player.participant.vars["outcomes"] = outcomes[:]
        player.participant.vars["outcomes_instructions"] = outcomes[:]

        if subsession.round_number == 1:
            for player in subsession.get_players():
                player.participant.vars["total_payoff"] = 0
                player.participant.vars["previous_choice"] = ""


def determine_outcome_shown(player):
    outcome_list_a = random.choices(
        list([player.session.config['payoff_high_a'],
              player.session.config['payoff_low_a']]),
        weights=(player.session.config['probability_win_a'],
                 1-player.session.config['probability_win_a']),
        k=1
    )
    outcome_list_b = random.choices(
        list([player.session.config['payoff_high_b'],
              player.session.config['payoff_low_b']]),
        weights=(player.session.config['probability_win_b'],
                 1-player.session.config['probability_win_b']),
        k=1
    )
    # to create the same "luck" for all, use a seed?
    player.outcome_a = Currency(outcome_list_a[0])
    player.outcome_b = Currency(outcome_list_b[0])

    if player.choice == "b":
        player.outcome_b = player.outcome_b
        player.trial_payoff = player.outcome_b
    elif player.choice == "a":
        player.outcome_a = player.outcome_a
        player.trial_payoff = player.outcome_a
    else:
        player.trial_payoff = 0


def calculate_trial_payoff(player):
    #prev_player = player.in_round(player.round_number - 1)
    if player.round_number > 1:
        prev_player = player.in_round(player.round_number - 1)
        player.total_payoff = prev_player.total_payoff + player.trial_payoff
    else:
        player.total_payoff = player.trial_payoff


def display_final_decision(player):
    # return true in case the current round is the maximum number of rounds
    end_of_rounds = player.round_number == Constants.num_rounds
    # when pushing stop explore OR getting to the end of all rounds then set the return to true
    if player.explore_stop or end_of_rounds:
        return True
    else:
        return False
# def next_app(player):
 #   if player.explore_stop == True:
  #      player.round_number = 100


## PAGES ####

class Consent(Page):
    form_model = 'player'
    form_fields = ['consent']  # , 'continue_button'
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1  # or player.consent == "non"

   # def vars_for_template(player):
    #    return dict(consent = player.consent, continue_button = player.continue_button)

    def error_message(player: Player, values):
        solutions = dict(consent=True)
        if values != solutions:
            return "You have to consent to continue."


class Instruction_1(Page):
    form_model = 'player'
    form_fields = ['choice']
    @staticmethod
    def is_displayed(player):
        # and player.consent == "yes" and player.continue_button == True
        return player.round_number == 1

    def vars_for_template(player):
        template_vars = {
            "symbols": player.participant.vars["symbols"],
            "outcomes": player.participant.vars["outcomes"],
            "payoff_a": [player.session.config['payoff_high_a'], player.session.config['payoff_low_a']],
            "probability_a": player.session.config['probability_win_a'],
            "payoff_b": [player.session.config['payoff_high_b'], player.session.config['payoff_low_b']],
            "probability_b": player.session.config['probability_win_b']
        }

        return template_vars


class Instruction_2(Page):
    form_model = 'player'
    form_fields = ['choice']
    @staticmethod
    def is_displayed(player):
        # and player.consent == "yes" and player.continue_button == True
        return player.round_number == 1

    def vars_for_template(player):
        template_vars = {
            "symbols": player.participant.vars["symbols"],
            "outcomes": player.participant.vars["outcomes"],
            "payoff_a": ["Payoff","Payoff"],
            "probability_a": player.session.config['probability_win_a'],
            "payoff_b": ["Payoff","Payoff"],
            "probability_b": player.session.config['probability_win_b']
        }

        return template_vars


class Instruction_3(Page):
    form_model = 'player'
    form_fields = [
        'continue_button',
        'choice',
        'information_cost_round',
        'switching_cost_round',
        'trial_payoff',
        'payout_left',
        'payout_right']


    @staticmethod
    def vars_for_template(player):
        template_vars = {
            "symbols": player.participant.vars["symbols"],
            "outcomes": player.participant.vars["outcomes"],
            "payoff_a": [player.session.config['payoff_high_a'], player.session.config['payoff_low_a']],
            "probability_a": player.session.config['probability_win_a'],
            "payoff_b": [player.session.config['payoff_high_b'], player.session.config['payoff_low_b']],
            "probability_b": player.session.config['probability_win_b'],
            "information_cost" : player.session.config['information_cost'],
            "switching_cost" : player.session.config['switching_cost'],
            "previous_choice" : player.participant.vars["previous_choice"],
            "round": player.round_number
        }

        return template_vars
    @staticmethod    
    def before_next_page(player, timeout_happened):
        print()
        player.participant.vars["previous_choice"] = player.choice
    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        print('upcoming app is', upcoming_apps)
        if player.continue_button: 
            return "comprehension_stage"

page_sequence = [
    Consent, 
    Instruction_1, 
    Instruction_2,
    Instruction_3
                 ]
