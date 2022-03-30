
def gen_packet_config(cfg):
  '''
  Creates a dictionary in which each unique packetId has a list of the indices
  of the associated sensors in the sensors config list
    ex: packets[0] = [0,3,4]
        this indicates that the sensors that are a part of packetId 0 are at
        indices 0, 3, & 4 of config["sensors"]
  '''
  # replace single quotes with double quotes
  cfg = cfg.replace("'",'"')
  cfg = cfg.replace('null','None')
  searching = True
  colons = []
  search_str = cfg
  prev_total = 0
  while searching:
     if ':' not in search_str:
         searching = False
     else:
         pos = search_str.index(':')
  
         colons.append(pos + prev_total)
         prev_total += pos + 1
         search_str = search_str[pos+1:]
  res = ''
  search_str = cfg
  for num in reversed(colons):
      start = end = num
      while not cfg[start].isspace():
          start -= 1
      start += 1
      while cfg[end] != '\n':
          end += 1
      d_str = cfg[num+1:end]
      s_str = cfg[start:num]
      
      if '{' not in d_str and '"' not in d_str:
          if d_str[-1] == ',':
              d_str = f' "{d_str[1:-1]}",'
          else:
              d_str = f' "{d_str[1:]}"'
      print(s_str, s_str.isnumeric())
      s_str = f'"{s_str}"'
      res = s_str + ':' + d_str + search_str[end:] + res
      search_str = search_str[:start]
  res = cfg[:colons[0]-1] + res
  print("--------")
  print(res)
  print("--------")
  print(res.split('\n')[54])
  
  import json
  out = json.loads(res)
  print(out)

config_str = """
{
  0: {
    0: {
      field: 'loxTankPTTemp',
      interpolation: null
    },
    1: {
      field: 'loxTankPTHeater',
      interpolation: null
    },
    2: {
      field: 'loxTankPTHeaterCurrent',
      interpolation: null
    },
    3: {
      field: 'loxTankPTHeaterVoltage',
      interpolation: null
    },
    4: {
      field: 'loxTankPTHeaterOvercurrentFlag',
      interpolation: Interpolation.interpolateErrorFlags
    }
  },
  1: {
    0: {
      field: 'loxTankPT',
      interpolation: null
    },
    1: {
      field: 'fuelTankPT',
      interpolation: null
    },
    2: {
      field: 'loxInjectorPT',
      interpolation: null
    },
    3: {
      field: 'fuelInjectorPT',
      interpolation: null
    },
    4: {
      field: 'pressurantPT',
      interpolation: null
    },
    5: {
      field: 'loxDomePT',
      interpolation: null
    },
    6: {
      field: 'fuelDomePT',
      interpolation: null
    },
  },
  2: {
    0: {
      field: 'flightVoltage',
      interpolation: null
    },
    1: {
      field: 'flightPower',
      interpolation: null
    },
    2: {
      field: 'flightCurrent',
      interpolation: null
    },
  },
  4: {
    0: {
      field: 'fuelTankMidTC',
      interpolation: null
    },
    1: {
      field: 'loxTankBottomTC',
      interpolation: null
    },
    2: {
      field: 'fuelTankTopTC',
      interpolation: null
    },
    3: {
      field: 'fuelTankBottomTC',
      interpolation: null
    },
  },
  16: {
    0: {
      field: 'fuelTankPTTemp',
      interpolation: null
    },
    1: {
      field: 'fuelTankPTHeater',
      interpolation: null
    },
    2: {
      field: 'fuelTankPTHeaterCurrent',
      interpolation: null
    },
    3: {
      field: 'fuelTankPTHeaterVoltage',
      interpolation: null
    },
    4: {
      field: 'fuelTankPTHeaterOvercurrentFlag',
      interpolation: Interpolation.interpolateErrorFlags
    },
  },
  17: {
    0: {
      field: 'loxExpectedStatic',
      interpolation: null
    },
    1: {
      field: 'fuelExpectedStatic',
      interpolation: null
    },
  },
  18: {
    0: {
      field: 'flowType',
      interpolation: null
    },
    1: {
      field: 'flowState',
      interpolation: null
    },
  },
  19: {
    0: {
      field: 'loxInjectorPTTemp',
      interpolation: null
    },
    1: {
      field: 'loxInjectorPTHeater',
      interpolation: null
    },
    2: {
      field: 'loxInjectorPTHeaterCurrent',
      interpolation: null
    },
    3: {
      field: 'loxInjectorPTHeaterVoltage',
      interpolation: null
    },
    4: {
      field: 'loxInjectorPTHeaterOvercurrentFlag',
      interpolation: Interpolation.interpolateErrorFlags
    },
  },
  20: {
    0: {
      field: 'armValve',
      interpolation: null
    },
    1: {
      field: 'igniter',
      interpolation: null
    },
    2: {
      field: 'loxMainValve',
      interpolation: null
    },
    3: {
      field: 'fuelMainValve',
      interpolation: null
    },
    4: {
      field: 'breakwire',
      interpolation: null
    },
    5: {
      field: 'led2',
      interpolation: null
    },
    6: {
      field: 'HPS',
      interpolation: null
    },
    7: {
      field: 'HPSEnable',
      interpolation: null
    },
  },
  21: {
    0: {
      field: 'armValveCurrent',
      interpolation: null
    },
    1: {
      field: 'igniterCurrent',
      interpolation: null
    },
    2: {
      field: 'loxMainValveCurrent',
      interpolation: null
    },
    3: {
      field: 'fuelMainValveCurrent',
      interpolation: null
    },
    4: {
      field: 'breakwireCurrent',
      interpolation: null
    },
    5: {
      field: 'led2Current',
      interpolation: null
    },
    6: {
      field: 'HPSCurrent',
      interpolation: null
    },
    7: {
      field: 'overcurrentTriggeredSols',
      interpolation: Interpolation.interpolateSolenoidErrors
    },
  },
  22: {
    0: {
      field: 'armValveVoltage',
      interpolation: null
    },
    1: {
      field: 'igniterVoltage',
      interpolation: null
    },
    2: {
      field: 'loxMainValveVoltage',
      interpolation: null
    },
    3: {
      field: 'fuelMainValveVoltage',
      interpolation: null
    },
    4: {
      field: 'breakwireVoltage',
      interpolation: null
    },
    5: {
      field: 'led2Voltage',
      interpolation: null
    },
    6: {
      field: 'HPSVoltage',
      interpolation: null
    },
    7: {
      field: 'HPSSupplyVoltage',
      interpolation: null
    },
  },
  57: {
    0: {
      field: 'fcEvent',
      interpolation: Interpolation.interpolateCustomEvent
    }
  },
  58: {
    0: {
      field: 'fcEventEnable',
      interpolation: null
    }
  },
  60: {
    0: {
      field: 'fuelInjectorPTTemp',
      interpolation: null
    },
    1: {
      field: 'fuelInjectorPTHeater',
      interpolation: null
    },
    2: {
      field: 'fuelInjectorPTHeaterCurrent',
      interpolation: null
    },
    3: {
      field: 'fuelInjectorPTHeaterVoltage',
      interpolation: null
    },
    4: {
      field: 'fuelInjectorPTHeaterOvercurrentFlag',
      interpolation: Interpolation.interpolateErrorFlags
    },
  },
  65: {
    0: {
      field: 'thermocoupleReadEnable',
      interpolation: null
    }
  }
}
"""
  
gen_packet_config(config_str)
