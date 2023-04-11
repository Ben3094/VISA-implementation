from pyVirtualLab.Instruments.KeysightMSOS804A import AddFunction, FFTMagnitudeFunction, KeysightMSOS804A

osc = KeysightMSOS804A("TCPIP0::k-msos804a-30101.ies.univ-montp2.fr::inst0::INSTR")
print(osc)
osc.Connect()
osc.Functions[1].ChangeFunction(AddFunction)
osc.Functions[1].Operand1 = osc.AnalogChannels[3]
channel1 = osc.AnalogChannels[1]
channel1.Offset = 1
channel1.Scale = 0.5
osc.TimeScale = 0.005
print(channel1.GetRMS())
# print(channel1.GetMaximum())
# print(channel1.GetMinimum())
# print(channel1.GetAverage())
# print(channel1.GetRange())
# print(channel1.GetFrequency())
# print(channel1.GetPeriod())
# print(channel1.GetRiseTime())
# print(osc.GetAnalogData())