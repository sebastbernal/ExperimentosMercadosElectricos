from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1,
    participation_fee=15000,
    doc=""
)

SESSION_CONFIGS = [

    dict(
        name='mercadoElectrico',
        display_name="Mercado Eléctrico de Energía Convencional",
        num_demo_participants=5,
        app_sequence=['mercadoElectrico']
    ),
]

# see the end of this file for the inactive session configs


# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'es'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'COP'
USE_POINTS = -True

ROOMS = [
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Bienvenido, seleccione el experimento en el que desea participar.
"""

# don't share this with anybody.
SECRET_KEY = '=&yh1hw^c-$8d6^pwc+&!fj3ugaovom4_rs87c6+wf2-y8emq%'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']

# inactive session configs
### dict(name='trust', num_demo_participants=2, app_sequence=['trust']),
### dict(name='prisoner', num_demo_participants=2, app_sequence=['prisoner']),
### dict(name='ultimatum', num_demo_participants=2, app_sequence=['ultimatum']),
### dict(name='ultimatum_strategy', num_demo_participants=2, app_sequence=['ultimatum'], use_strategy_method=True),
### dict(name='ultimatum_non_strategy', num_demo_participants=2, app_sequence=['ultimatum'], use_strategy_method=False),
### dict(name='vickrey_auction', num_demo_participants=3, app_sequence=['vickrey_auction']),
### dict(name='volunteer_dilemma', num_demo_participants=3, app_sequence=['volunteer_dilemma']),
### dict(name='cournot', num_demo_participants=2, app_sequence=['cournot']),
### dict(name='principal_agent', num_demo_participants=2, app_sequence=['principal_agent']),
### dict(name='dictator', num_demo_participants=2, app_sequence=['dictator']),
### dict(name='matching_pennies', num_demo_participants=2, app_sequence=['matching_pennies']),
### dict(name='traveler_dilemma', num_demo_participants=2, app_sequence=['traveler_dilemma']),
### dict(name='bargaining', num_demo_participants=2, app_sequence=['bargaining']),
### dict(name='common_value_auction', num_demo_participants=3, app_sequence=['common_value_auction']),
### dict(name='bertrand', num_demo_participants=2, app_sequence=['bertrand']),
### dict(name='real_effort', num_demo_participants=1, app_sequence=['real_effort']),
### dict(name='lemon_market', num_demo_participants=3, app_sequence=['lemon_market']),
### dict(name='public_goods_simple', num_demo_participants=3, app_sequence=['public_goods_simple']),
### dict(name='trust_simple', num_demo_participants=2, app_sequence=['trust_simple']),
