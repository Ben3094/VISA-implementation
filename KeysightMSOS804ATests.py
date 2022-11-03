# import os
# os.add_dll_directory('C:\\Program Files\\Keysight\\IO Libraries Suite\\bin')
from KeysightMSOS804A import AddFunction, FFTMagnitudeFunction, KeysightMSOS804A

osc = KeysightMSOS804A("TCPIP0::k-msos804a-30101.ies.univ-montp2.fr::inst0::INSTR")
osc.Connect()
osc.Functions[1].ChangeFunction(AddFunction, [osc.Channels[1], osc.Channels[2]])
channel1 = next((channel for channel in osc.Channels if channel.Address == 1), None)
#print(osc)
# print(channel1.GetMaximum())
# print(channel1.GetMinimum())
# print(channel1.GetAverage())
# print(channel1.GetRange())
# print(channel1.GetFrequency())
# print(channel1.GetPeriod())
# print(channel1.GetRiseTime())
# print(osc.GetAnalogData())
print(channel1.GetFFTPeaksMagnitudes())