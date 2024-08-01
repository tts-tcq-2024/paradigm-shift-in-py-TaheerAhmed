# Define thresholds and tolerance
LOW_SOC = 20
HIGH_SOC = 80
SOC_WARNING_TOLERANCE = 5  # 5% of the upper limit

LOW_TEMP = 0
HIGH_TEMP = 45
TEMP_WARNING_TOLERANCE = 2.25  # 5% of the upper limit

MAX_CHARGE_RATE = 0.8
CHARGE_RATE_WARNING_TOLERANCE = 0.04  # 5% of the max charge rate

# Map values to conditions based on boundaries
def map_to_condition(value, low, high, tolerance):
    if value < low:
        return 'BREACH_LOW'
    elif low <= value < low + tolerance:
        return 'WARNING_LOW'
    elif high - tolerance <= value <= high:
        return 'WARNING_HIGH'
    elif value > high:
        return 'BREACH_HIGH'
    else:
        return 'NORMAL'

# Specific mapping functions for each parameter
def map_soc_to_condition(soc):
    return map_to_condition(soc, LOW_SOC, HIGH_SOC, SOC_WARNING_TOLERANCE)

def map_temp_to_condition(temperature):
    return map_to_condition(temperature, LOW_TEMP, HIGH_TEMP, TEMP_WARNING_TOLERANCE)

def map_charge_rate_to_condition(charge_rate):
    return map_to_condition(charge_rate, 0, MAX_CHARGE_RATE, CHARGE_RATE_WARNING_TOLERANCE)

# Translate condition to message
def translate_condition_to_message(condition, parameter, language='EN'):
    messages = {
        'BREACH_LOW': {
            'EN': f'{parameter} is too low!',
            'DE': f'{parameter} ist zu niedrig!'
        },
        'WARNING_LOW': {
            'EN': f'{parameter} is approaching low limit!',
            'DE': f'{parameter} nähert sich dem unteren Grenzwert!'
        },
        'NORMAL': {
            'EN': f'{parameter} is normal.',
            'DE': f'{parameter} ist normal.'
        },
        'WARNING_HIGH': {
            'EN': f'{parameter} is approaching high limit!',
            'DE': f'{parameter} nähert sich dem oberen Grenzwert!'
        },
        'BREACH_HIGH': {
            'EN': f'{parameter} is too high!',
            'DE': f'{parameter} ist zu hoch!'
        }
    }
    return messages[condition][language]

# Assess the battery status and print messages
def assess_battery_status(temperature, soc, charge_rate, language='EN'):
    conditions = {
        'Temperature': map_temp_to_condition(temperature),
        'State of Charge': map_soc_to_condition(soc),
        'Charge Rate': map_charge_rate_to_condition(charge_rate)
    }
    
    for parameter, condition in conditions.items():
        print(translate_condition_to_message(condition, parameter, language))
    
    return conditions

# Determine overall battery status
def compute_overall_status(conditions):
    if any(cond.startswith('BREACH') for cond in conditions.values()):
        return 'Battery is NOT OK!'
    elif any(cond.startswith('WARNING') for cond in conditions.values()):
        return 'Battery is in WARNING state!'
    else:
        return 'Battery is OK!'

# Main function to check battery status
def check_battery_status(temperature, soc, charge_rate, language='EN'):
    conditions = assess_battery_status(temperature, soc, charge_rate, language)
    overall_status = compute_overall_status(conditions)
    print(overall_status)
    return overall_status == 'Battery is OK!'

if __name__ == '__main__':
    assert check_battery_status(25, 70, 0.7) is True
    assert check_battery_status(50, 85, 0, 'DE') is False
