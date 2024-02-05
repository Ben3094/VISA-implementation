from pyVirtualLab.Instruments.AgilentN5183B.AgilentN5183B import AgilentN5183B, OutSignal, TriggerSource, PulseType
from pandas import read_csv
from io import StringIO

scr = AgilentN5183B('TCPIP::A-N5183B-250181.ies.univ-montp2.fr::inst0::INSTR')
scr.Connect()

print(scr.SweepOutSignal)
print(scr.Trigger1OutSignal)
print(scr.Trigger2OutSignal)
scr.SweepOutSignal = OutSignal.SweepEnd
scr.Trigger1OutSignal = OutSignal.PulseVideo
scr.Trigger2OutSignal = OutSignal.PulseVideo
print(scr.SweepOutSignal)
print(scr.Trigger1OutSignal)
print(scr.Trigger2OutSignal)

scr.IsLowFrequencyOutputEnabled = False
print(scr.IsLowFrequencyOutputEnabled)
scr.IsLowFrequencyOutputEnabled = True
print(scr.IsLowFrequencyOutputEnabled)

scr.SweepTriggerSource = TriggerSource.Trigger1
scr.SweepPointTriggerSource = TriggerSource.Immediate
sweepPoints = """Frequency,Power,DwellTime
36000000000, -20, 0.580
36000000000, -10, 0.005
36000000000, -20, 0.005
36000000000, -10, 0.005
36000000000, -20, 0.005
36000000000, -10, 0.005
36000000000, -20, 0.005
36000000000, -10, 0.005
36000000000, -20, 0.005
36000000000, -10, 0.005
36000000000, -20, 0.005
36000000000, -10, 0.005
36000000000, -20, 0.005
36000000000, -10, 0.005
36000000000, -20, 0.005
"""
sweepPoints = read_csv(StringIO(sweepPoints))
scr.SweepPoints = [(frequency, power, dwellTime) for frequency, power, dwellTime in zip(sweepPoints['Frequency'], sweepPoints['Power'], sweepPoints['DwellTime'])]
print(f"Sweep points: {scr.SweepPoints}")
scr.IsSweepReversed = True
print(f"Sweep{'' if scr.IsSweepReversed else ' not'} reversed")
scr.IsSweepReversed = False
print(f"Sweep{'' if scr.IsSweepReversed else ' not'} reversed")
scr.IsPowerSweepEnabled = True
print(f"Power sweep{'' if scr.IsPowerSweepEnabled else ' not'} enabled")
scr.IsPowerSweepEnabled = False
print(f"Power sweep{'' if scr.IsPowerSweepEnabled else ' not'} enabled")
scr.IsFrequencySweepEnabled = True
print(f"Frequency sweep{'' if scr.IsFrequencySweepEnabled else ' not'} enabled")
scr.IsFrequencySweepEnabled = False
print(f"Frequency sweep{'' if scr.IsFrequencySweepEnabled else ' not'} enabled")

scr.IsPulseEnabled = False
for pulseType in PulseType:
	scr.PulseTypeSet = pulseType
	try:
		scr.PulseDelay = 1
	except Exception as e:
		print(e)
	try:
		scr.PulsePeriod = 2
	except Exception as e:
		print(e)
	try:
		scr.PulseWidth = 1
	except Exception as e:
		print(e)
scr.IsPulseEnabled = True