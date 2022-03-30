from interpolations import *


inboundPackets = {
  # [1..59] Sent by Flight Computer
  0: [
    ['firmwareCommitHash', asASCIIString],
  ],
  1: [
    ['flightBattVoltage', DataType.FLOAT],
    ['flightBattCurrent', DataType.FLOAT],
    ['flightBattPower', DataType.FLOAT]
  ],
  2: [
    ['flightSupply12Voltage', DataType.FLOAT],
    ['flightSupply12Current', DataType.FLOAT],
    ['flightSupply12Power', DataType.FLOAT]
  ],
  3: [
    ['flightSupply8Voltage', DataType.FLOAT],
    ['flightSupply8Current', DataType.FLOAT],
    ['flightSupply8Power', DataType.FLOAT]
  ],
  4: [
    ['qW', DataType.FLOAT],
    ['qX', DataType.FLOAT],
    ['qY', DataType.FLOAT],
    ['qZ', DataType.FLOAT],
    ['accelX', DataType.FLOAT],
    ['accelY', DataType.FLOAT],
    ['accelZ', DataType.FLOAT],
  ],
  5: [
    ['baroAltitude', DataType.FLOAT],
    ['baroPressure', DataType.FLOAT],
    ['baroTemperature', DataType.FLOAT],
  ],
  6: [
    ['gpsLatitude', DataType.FLOAT],
    ['gpsLongitude', DataType.FLOAT],
    ['gpsAltitude', DataType.FLOAT],
    ['gpsSpeed', DataType.FLOAT]
  ],
  9: [
    ['pressurantPTROC', DataType.FLOAT],
  ],
  # [10..59] Sent by Flight Computer
  10: [
    ['loxTankPT', DataType.FLOAT],
    ['fuelTankPT', DataType.FLOAT],
    ['loxInjectorPT', DataType.FLOAT],
    ['fuelInjectorPT', DataType.FLOAT],
    ['pressurantPT', DataType.FLOAT],
    ['loxDomePT', DataType.FLOAT],
    ['fuelDomePT', DataType.FLOAT]
  ],

  20: [
    ['engineTC1', DataType.FLOAT],
  ],
  21: [
    ['engineTC2', DataType.FLOAT],
  ],
  22: [
    ['engineTC3', DataType.FLOAT],
  ],
  23: [
    ['engineTC4', DataType.FLOAT],
  ],

  28: [
    ['loxGemsVoltage', DataType.FLOAT],
    ['loxGemsCurrent', DataType.FLOAT],
  ],
  29: [
    ['fuelGemsVoltage', DataType.FLOAT],
    ['fuelGemsCurrent', DataType.FLOAT],
  ],
  30: [
    ['armValveVoltage', DataType.FLOAT],
    ['armValveCurrent', DataType.FLOAT],
  ],
  31: [
    ['igniterVoltage', DataType.FLOAT],
    ['igniterCurrent', DataType.FLOAT],
  ],
  32: [
    ['loxMainValveVoltage', DataType.FLOAT],
    ['loxMainValveCurrent', DataType.FLOAT],
  ],
  33: [
    ['fuelMainValveVoltage', DataType.FLOAT],
    ['fuelMainValveCurrent', DataType.FLOAT],
  ],
  34: [
    ['breakwireVoltage', DataType.FLOAT],
    ['breakwireCurrent', DataType.FLOAT],
  ],

  35: [
    ['loxTankBottomHtrVoltage', DataType.FLOAT],
    ['loxTankBottomHtrCurrent', DataType.FLOAT],
  ],
  36: [
    ['loxTankMidHtrVoltage', DataType.FLOAT],
    ['loxTankMidHtrCurrent', DataType.FLOAT],
  ],
  37: [
    ['loxTankTopHtrVoltage', DataType.FLOAT],
    ['loxTankTopHtrCurrent', DataType.FLOAT],
  ],
  38: [
    ['igniterEnableVoltage', DataType.FLOAT],
    ['igniterEnableCurrent', DataType.FLOAT],
  ],
  39: [
    ['breakwire1', DataType.FLOAT],
    ['breakwire2', DataType.FLOAT],
  ],
  40: [
    ['armValveState', DataType.UINT8],
  ],
  41: [
    ['igniterState', DataType.UINT8],
  ],
  42: [
    ['loxMainValveState', DataType.UINT8],
  ],
  43: [
    ['fuelMainValveState', DataType.UINT8],
  ],
  45: [
    ['loxTankBottomHtrState', DataType.UINT8],
  ],
  46: [
    ['loxTankMidHtrState', DataType.UINT8],
  ],
  47: [
    ['loxTankTopHtrState', DataType.UINT8],
  ],
  48: [
    ['igniterEnableState', DataType.UINT8],
  ],

  49: [
    ['actuatorStates', DataType.UINT8],
  ],

  50: [
    ['flowState', DataType.UINT8],
  ],
  51: [
    ['autoVentStatus', DataType.UINT8],
  ],
  52: [
    ['loxGemsValveState', DataType.UINT8],
  ],
  53: [
    ['fuelGemsValveState', DataType.UINT8],
  ],
  55: [
    ['vehicleMode', DataType.UINT8],
  ],
  56: [
    ['radioRSSI', DataType.FLOAT],
  ], 

  152: [
    ['autoLoxLead', DataType.UINT32],
    ['autoBurnTime', DataType.UINT32],
    ['autoIgniterAbortEnabled', DataType.UINT8],
    ['autoBreakwireAbortEnabled', DataType.UINT8],
    ['autoThrustAbortEnabled', DataType.UINT8],
  ],
  158: [
    ['apogeeTime', DataType.UINT32],
    ['mainChuteDeployTime', DataType.UINT32],
  ],

  # [60:89] ACTUATOR CONTROLLERS
  61: [
    ['acBattVoltage', DataType.FLOAT],
    ['acBattCurrent', DataType.FLOAT],
  ],
  62: [
    ['acSupply12Voltage', DataType.FLOAT],
    ['acSupply12Current', DataType.FLOAT],
  ],
  70: [
    ['acLinAct1State', DataType.UINT8],
    ['acLinAct1Voltage', DataType.FLOAT],
    ['acLinAct1Current', DataType.FLOAT],
  ],
  71: [
    ['acLinAct2State', DataType.UINT8],
    ['acLinAct2Voltage', DataType.FLOAT],
    ['acLinAct2Current', DataType.FLOAT],
  ],
  72: [
    ['acLinAct3State', DataType.UINT8],
    ['acLinAct3Voltage', DataType.FLOAT],
    ['acLinAct3Current', DataType.FLOAT],
  ],
  73: [
    ['acLinAct4State', DataType.UINT8],
    ['acLinAct4Voltage', DataType.FLOAT],
    ['acLinAct4Current', DataType.FLOAT],
  ],
  74: [
    ['acLinAct5State', DataType.UINT8],
    ['acLinAct5Voltage', DataType.FLOAT],
    ['acLinAct5Current', DataType.FLOAT],
  ],
  75: [
    ['acLinAct6State', DataType.UINT8],
    ['acLinAct6Voltage', DataType.FLOAT],
    ['acLinAct6Current', DataType.FLOAT],
  ],
  76: [
    ['acLinAct7State', DataType.UINT8],
    ['acLinAct7Voltage', DataType.FLOAT],
    ['acLinAct7Current', DataType.FLOAT],
  ],

  80: [
    ['acHeater1Voltage', DataType.FLOAT],
    ['acHeater1Current', DataType.FLOAT],
  ],
  81: [
    ['acHeater2Voltage', DataType.FLOAT],
    ['acHeater2Current', DataType.FLOAT],
  ],
  82: [
    ['acHeater3Voltage', DataType.FLOAT],
    ['acHeater3Current', DataType.FLOAT],
  ],
  83: [
    ['acHeater4Voltage', DataType.FLOAT],
    ['acHeater4Current', DataType.FLOAT],
  ],

  # [100:129] DAQs
  100: [
    ['daqBattVoltage', DataType.FLOAT],
    ['daqBattCurrent', DataType.FLOAT],
  ],

  101: [
    ['daqADC0', DataType.FLOAT],
    ['daqADC1', DataType.FLOAT],
    ['daqADC2', DataType.FLOAT],
    ['daqADC3', DataType.FLOAT],
    ['daqADC4', DataType.FLOAT],
    ['daqADC5', DataType.FLOAT],
    ['daqADC6', DataType.FLOAT],
    ['daqADC7', DataType.FLOAT],
  ],

  110: [
    ['daqTC1', DataType.FLOAT],
  ],
  111: [
    ['daqTC2', DataType.FLOAT],
  ],
  112: [
    ['daqTC3', DataType.FLOAT],
  ],
  113: [
    ['daqTC4', DataType.FLOAT],
  ],

  120: [
    ['loadCell1', DataType.FLOAT],
    ['loadCell2', DataType.FLOAT],
    ['loadCellSum', DataType.FLOAT],
  ],
  121: [
    ['fastLoadCell1', DataType.FLOAT],
    ['fastLoadCell2', DataType.FLOAT],
    # ['fastLoadCellSum', DataType.FLOAT],
  ],
  220: [
    ['capacitor', DataType.FLOAT],
  ],
}

outboundPackets = {
  # Windows enable port packet
  0: [DataType.UINT8],
  # [130..169] Sent to Flight Computer
  126: [DataType.UINT8], # Lox gems
  127: [DataType.UINT8], # Fuel gems
  128: [DataType.UINT8], # Lox gems toggle
  129: [DataType.UINT8], # Fuel gems toggle
  130: [DataType.UINT8],
  131: [DataType.UINT8],
  132: [DataType.UINT8],
  133: [DataType.UINT8],
  135: [DataType.UINT8],
  136: [DataType.UINT8],
  137: [DataType.UINT8],
  138: [DataType.UINT8],

  140: [DataType.UINT8],

  150: [],
  151: [],
  152: [],

  # [170..199] Sent to Actuator Controller
  170: [DataType.UINT8, DataType.UINT32],
  171: [DataType.UINT8, DataType.UINT32],
  172: [DataType.UINT8, DataType.UINT32],
  173: [DataType.UINT8, DataType.UINT32],
  174: [DataType.UINT8, DataType.UINT32],
  175: [DataType.UINT8, DataType.UINT32],
  176: [DataType.UINT8, DataType.UINT32],
  180: [DataType.UINT8],
  181: [DataType.UINT8],
  182: [DataType.UINT8],
  183: [DataType.UINT8],
}

packTypeMapping = {
    'inbound': inboundPackets,
    'outbound': outboundPackets,
}