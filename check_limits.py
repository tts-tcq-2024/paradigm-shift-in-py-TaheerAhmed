# Language translations
translations = {
    'en': {
        'LOW_SOC_BREACH': 'State of Charge is too low!',
        'LOW_SOC_WARNING': 'Warning: State of Charge is approaching the lower limit!',
        'HIGH_SOC_WARNING': 'Warning: State of Charge is approaching the upper limit!',
        'HIGH_SOC_BREACH': 'State of Charge is too high!',
        'LOW_TEMP_BREACH': 'Temperature is too low!',
        'LOW_TEMP_WARNING': 'Warning: Temperature is approaching the lower limit!',
        'HIGH_TEMP_WARNING': 'Warning: Temperature is approaching the upper limit!',
        'HIGH_TEMP_BREACH': 'Temperature is too high!',
        'HIGH_CHARGE_RATE_WARNING': 'Warning: Charge rate is approaching the upper limit!',
        'HIGH_CHARGE_RATE_BREACH': 'Charge rate is too high!',
        'NORMAL': 'Parameter is within normal range.'
    },
    'de': {
        'LOW_SOC_BREACH': 'Der Ladezustand ist zu niedrig!',
        'LOW_SOC_WARNING': 'Warnung: Der Ladezustand nähert sich dem unteren Grenzwert!',
        'HIGH_SOC_WARNING': 'Warnung: Der Ladezustand nähert sich dem oberen Grenzwert!',
        'HIGH_SOC_BREACH': 'Der Ladezustand ist zu hoch!',
        'LOW_TEMP_BREACH': 'Die Temperatur ist zu niedrig!',
        'LOW_TEMP_WARNING': 'Warnung: Die Temperatur nähert sich dem unteren Grenzwert!',
        'HIGH_TEMP_WARNING': 'Warnung: Die Temperatur nähert sich dem oberen Grenzwert!',
        'HIGH_TEMP_BREACH': 'Die Temperatur ist zu hoch!',
        'HIGH_CHARGE_RATE_WARNING': 'Warnung: Die Laderate nähert sich dem oberen Grenzwert!',
        'HIGH_CHARGE_RATE_BREACH': 'Die Laderate ist zu hoch!',
        'NORMAL': 'Parameter ist innerhalb des normalen Bereichs.'
    }
}

# Define ranges for each parameter
SOC_RANGES = {
    'LOW_SOC_BREACH': (0, 20),
    'LOW_SOC_WARNING': (21, 24),
    'NORMAL': (25, 75),
    'HIGH_SOC_WARNING': (76, 80),
    'HIGH_SOC_BREACH': (81, 100)
}

TEMP_RANGES = {
    'LOW_TEMP_BREACH': (-100, 0),  # Assuming temperature cannot be lower than -100 for safety
    'LOW_TEMP_WARNING': (1, 5),
    'NORMAL': (6, 40),
    'HIGH_TEMP_WARNING': (41, 45),
    'HIGH_TEMP_BREACH': (46, 100)  # Assuming temperature cannot be higher than 100 for safety
}

CHARGE_RATE_RANGES = {
    'NORMAL': (0, 0.76),
    'HIGH_CHARGE_RATE_WARNING': (0.77, 0.8),
    'HIGH_CHARGE_RATE_BREACH': (0.81, 1)  # Assuming charge rate cannot be higher than 1 for safety
}

# Global variable for language
language = 'en'

def map_to_condition(value, ranges):
    for condition, (lower, upper) in ranges.items():
        if lower <= value <= upper:
            return condition
    return 'UNKNOWN'  # If value does not fit in any range

def map_soc_to_condition(soc):
    return map_to_condition(soc, SOC_RANGES)

def map_temp_to_condition(temperature):
    return map_to_condition(temperature, TEMP_RANGES)

def map_charge_rate_to_condition(charge_rate):
    return map_to_condition(charge_rate, CHARGE_RATE_RANGES)

def translate_condition_to_message(condition):
    return translations[language].get(condition, 'Unknown condition.')

def is_breach(condition):
    return 'BREACH' in condition

def is_warning(condition):
    return 'WARNING' in condition

def assess_battery_status(soc_condition, temp_condition, charge_rate_condition):
    if any(is_breach(condition) for condition in [soc_condition, temp_condition, charge_rate_condition]):
        return 'Battery status: CRITICAL'
    if any(is_warning(condition) for condition in [soc_condition, temp_condition, charge_rate_condition]):
        return 'Battery status: WARNING'
    return 'Battery status: NORMAL'

def compute_overall_status(temperature, soc, charge_rate):
    soc_condition = map_soc_to_condition(soc)
    temp_condition = map_temp_to_condition(temperature)
    charge_rate_condition = map_charge_rate_to_condition(charge_rate)

    return assess_battery_status(soc_condition, temp_condition, charge_rate_condition)

def check_battery_status(temperature, soc, charge_rate):
    soc_condition = map_soc_to_condition(soc)
    temp_condition = map_temp_to_condition(temperature)
    charge_rate_condition = map_charge_rate_to_condition(charge_rate)

    soc_message = translate_condition_to_message(soc_condition)
    temp_message = translate_condition_to_message(temp_condition)
    charge_rate_message = translate_condition_to_message(charge_rate_condition)

    print(soc_message)
    print(temp_message)
    print(charge_rate_message)

    overall_status = compute_overall_status(temperature, soc, charge_rate)
    print(overall_status)

    return all(condition in ['NORMAL', 'UNKNOWN'] for condition in [soc_condition, temp_condition, charge_rate_condition])

if __name__ == '__main__':
    language = 'en'
    assert(check_battery_status(25, 70, 0.7) is True)
    assert(check_battery_status(50, 85, 0) is False)

    language = 'de'
    assert(check_battery_status(25, 70, 0.7) is True)
    assert(check_battery_status(50, 85, 0) is False)
