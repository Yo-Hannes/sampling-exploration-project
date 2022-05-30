from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Decide(Page):
    form_model = 'player'
    form_fields = ['choice_a'] 
    def before_next_page(self):
        player = self.player
        player.number_exploration = self.round_number
        #self.determine_outcome()

## this does not work -- do I need to use vars for template?

class Results(Page):
    pass


page_sequence = [Decide, Results]
