from otree.api import *


doc = """
This is the final payoff displayed to the participant
"""


class Constants(BaseConstants):
    name_in_url = 'final_payoffs'
    players_per_group = None
    num_rounds = 1



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass
    


# PAGES
class Overall_Results(Page):
    def vars_for_template(player):
        return dict(
                overall_payoff = player.participant.vars["total_payoff"]
                )


page_sequence = [Overall_Results]
