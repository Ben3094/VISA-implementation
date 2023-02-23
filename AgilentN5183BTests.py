from pyVirtualLab.Instruments.AgilentN5183B import AgilentN5183B, OutSignal, TriggerSource
from pandas import read_csv
from io import StringIO
from aenum import Enum

scr = AgilentN5183B('TCPIP::A-N5183B-250181.ies.univ-montp2.fr::inst0::INSTR')
scr.Connect()
print(scr.SweepOutSignal)
print(scr.Tigger1OutSignal)
print(scr.Tigger2OutSignal)
scr.SweepOutSignal = OutSignal.SweepEnd
scr.Tigger1OutSignal = OutSignal.PulseVideo
scr.Tigger2OutSignal = OutSignal.PulseVideo
print(scr.SweepOutSi<gnal)
print(scr.Tigger1OutSignal)
print(scr.Tigger2OutSignal)

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