from pyVirtualLab.Instruments.KeysightMSOS804A import AddFunction, FFTMagnitudeFunction, KeysightMSOS804A, SubtractFunction

osc = KeysightMSOS804A("TCPIP0::k-msos804a-30101.ies.univ-montp2.fr::inst0::INSTR")
print(osc)
osc.Connect()
osc.AnalogChannels[1].IsEnabled = True
osc.Functions[1].ChangeFunction(AddFunction)
osc.Functions[1].Operand1 = osc.AnalogChannels[3]
osc.WaveformMemoryChannels[1].Save(osc.AnalogChannels[1])
osc.WaveformMemoryChannels[1].IsEnabled = True
subtractFunction:SubtractFunction = osc.Functions[2]
subtractFunction.ChangeFunction(SubtractFunction)
subtractFunction.FirstOperand = osc.AnalogChannels[1]
subtractFunction.SecondOperand = osc.WaveformMemoryChannels[1]
subtractFunction.IsEnabled = True
print(subtractFunction.GetArea())
osc.AnalogChannels[1].IsEnabled = False
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