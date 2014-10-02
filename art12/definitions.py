EU_COUNTRY = 'EU27'

TREND_OPTIONS = [
    ('x', 'unknown'),
    ('=', 'stable'),
    ('+', 'increase'),
    ('-', 'decrease'),
    ('N/A', 'not reported'),
]

TREND_CLASSES = {
    '+': 'inc',
    '-': 'dec',
    '0': 'eq',
    'x': 'xx',
    'F': 'f',
}

SEASON_FIELDS = [
    'filled_population',
    'percentage_population_mean_size',

    'percentage_population_maximum_size',
    'percentage_population_minimum_size',

    'population_minimum_size',
    'population_maximum_size',

    'population_size_unit',
    'population_quality',

    'population_trend',
    'population_trend_period',
    'population_trend_magnitude_min',
    'population_trend_magnitude_max',
    'population_trend_quality',
    'population_trend_additional_info',

    'population_trend_long',
    'population_trend_long_period',
    'population_trend_long_magnitude_min',
    'population_trend_long_magnitude_max',
    'population_trend_long_quality',

    'conclusion_population',
]
