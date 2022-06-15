from os import environ 

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

PARTICIPANT_FIELDS = [] #NEW

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

SESSION_CONFIGS = [
     dict(
        name='Explore_exploit',
        display_name="test_all",
        num_demo_participants=1,
        app_sequence=[
         'instructions_stage',
         'comprehension_stage',
         'explore_stage',
         'exploit_stage',
         'final_payoffs'
         ],
        switching_cost = 9,
        information_cost = 1,
        probability_win_a = .8,
        probability_win_b = .6,
        payoff_high_a = 10,
        payoff_low_a = -10,
        payoff_high_b = 10,
        payoff_low_b = -10,
        switching_after_round = 50,
        doc="""
    Edit the 'switching cost' and 'information cost' parameter to change the cost of information and switching
    """
     ),
      dict(
        name='Instructions',
        display_name="test_instructions",
        num_demo_participants=1,
        app_sequence=['instructions_stage'],
        switching_cost = 5,
        information_cost = 5,
        probability_win_a = 1.00,
        probability_win_b = 1.00,
        payoff_high_a = 1,
        payoff_low_a = 2,
        payoff_high_b = 2,
        payoff_low_b = 2,
        doc="""
    Edit the 'switching cost' and 'information cost' parameter to change the cost of information and switching
    """
     ),
     dict(
        name='Comprehension',
        display_name="test_comprehension",
        num_demo_participants=1,
        app_sequence=['comprehension_stage']
     ),
     dict(
        name='Explore',
        display_name="test_explore",
        num_demo_participants=1,
        app_sequence=['explore_stage'],
        switching_cost = 5,
        information_cost = 5,
        probability_win_a = 1.00,
        probability_win_b = 1.00,
        payoff_high_a = 1,
        payoff_low_a = 2,
        payoff_high_b = 2,
        payoff_low_b = 2,
        doc="""
    Edit the 'switching cost' and 'information cost' parameter to change the cost of information and switching
    """
     ),

     dict(
        name='Exploit',
        display_name="test_exploit",
        num_demo_participants=1,
        app_sequence=['exploit_stage'],
        switching_cost = 5,
        information_cost = 5,
        probability_win_a = 1.00,
        probability_win_b = 1.00,
        payoff_high_a = 1,
        payoff_low_a = 2,
        payoff_high_b = 2,
        payoff_low_b = 2,
        doc="""
    Edit the 'switching cost' and 'information cost' parameter to change the cost of information and switching
    """
     )
]


# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = []

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '#+pk=-v%^)6$dl=2919dh!rcb**1)ihsomvd*tr0+75mnr%9&2'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']
