from pyVirtualLab.Instruments.AgilentN5183B import AgilentN5183B, OutSignal

scr = AgilentN5183B('TCPIP0::169.254.189.231::inst0::INSTR')
scr.Connect()
print(scr.SweepOutSignal)
print(scr.Tigger1OutSignal)
print(scr.Tigger2OutSignal)
scr.SweepOutSignal = OutSignal.SweepEnd
scr.Tigger1OutSignal = OutSignal.PulseVideo
scr.Tigger2OutSignal = OutSignal.PulseVideo
print(scr.SweepOutSignal)
print(scr.Tigger1OutSignal)
print(scr.Tigger2OutSignal)

scr.IsLowFrequencyOutputEnabled = False
print(scr.IsLowFrequencyOutputEnabled)
scr.IsLowFrequencyOutputEnabled = True
print(scr.IsLowFrequencyOutputEnabled)