EU_COUNTRY = "EU27"

TREND_OPTIONS = [
    ("x", "unknown"),
    ("0", "stable"),
    ("+", "increase"),
    ("-", "decrease"),
    ("F", "fluctuating"),
    ("empty", "not reported"),
]

TREND_OPTIONS_EU = TREND_OPTIONS[:-1] + [
    ("u", "uncertain"),
    ("n", "not applicable"),
]

TREND_CLASSES = {
    "+": "inc",
    "-": "dec",
    "0": "eq",
    "=": "eq",
    "x": "xx",
    "F": "f",
    "n": "n",
    "u": "u",
}

SEASON_FIELDS = [
    "filled_population",
    "percentage_population_mean_size",
    "percentage_population_maximum_size",
    "percentage_population_minimum_size",
    "population_minimum_size",
    "population_maximum_size",
    "population_size_unit",
    "population_quality",
    "population_trend",
    "population_trend_period",
    "population_trend_magnitude_min",
    "population_trend_magnitude_max",
    "population_trend_quality",
    "population_trend_additional_info",
    "population_trend_long",
    "population_trend_long_period",
    "population_trend_long_magnitude_min",
    "population_trend_long_magnitude_max",
    "population_trend_long_quality",
    "conclusion_population",
]

SEASON_FIELDS_CONVERT = [
    "population_minimum_size",
    "population_maximum_size",
    "percentage_population_mean_size",
]

CONTRIB_OPTIONS = [
    ("A", "Secure population status"),
    ("B", "Improving"),
    ("C", "Not improving"),
    ("E", "Unknown population status"),
]

STATUS_CLASSES = {
    "Secure": "secure",
    "Threatened": "threat",
    "Near Threatened": "near",
    "Declining": "declining",
    "Depleted": "depleted",
    "Unknown": "unknown",
}
