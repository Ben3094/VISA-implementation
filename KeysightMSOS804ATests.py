# import os
# os.add_dll_directory('C:\\Program Files\\Keysight\\IO Libraries Suite\\bin')
from KeysightMSOS804A import KeysightMSOS804A

osc = KeysightMSOS804A("TCPIP0::k-msos804a-30101::inst0::INSTR")
channel1 = next((channel for channel in osc.Channels if channel.Address == 1), None)
# print(channel1.GetMaximum())
# print(channel1.GetMinimum())
# print(channel1.GetAverage())
# print(channel1.GetRange())
# print(channel1.GetFrequency())
# print(channel1.GetPeriod())
# print(channel1.GetRiseTime())
# print(osc.GetAnalogData())
print(channel1.GetFFTPeaksMagnitudes())