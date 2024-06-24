
def temp_ok(tmp):
  if temperature < 0 or temperature > 45:
    return False
  return True
def soc_ok(soc):
  if soc < 20 or soc > 80:
    return False
  return True
def charge_ok(charge_rate):
  if charge_rate > 0.8:
    return False
  return True


def battery_is_ok(temperature, soc, charge_rate):
  # if temperature < 0 or temperature > 45:
  #   return False
  # elif soc < 20 or soc > 80:
  #   return False
  # elif charge_rate > 0.8:
  #   return False
  if(temp_ok(temperature)and charge_ok(charge_rate) and soc_ok(soc)):
    return True
  else:
    return False


if __name__ == '__main__':
  assert(battery_is_ok(25, 70, 0.7) is True)
  assert(battery_is_ok(50, 85, 0) is False)
