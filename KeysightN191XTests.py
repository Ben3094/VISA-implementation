from pyVirtualLab.Instruments.KeysightN191X import KeysightN191X
import pandas

powerMeter = KeysightN191X('TCPIP0::k-n1913a-80021.ies.univ-montp2.fr::inst0::INSTR')
powerMeter.Connect()
cal = pandas.read_csv("V8486A calibration.csv")
cal = dict(zip(cal['Frequency (Hz)'], cal['Calibration factor (%)']))
powerMeter.CalibrationFactorsSets['V8486B'] = cal
sensor = powerMeter.Sensors[1]
sensor.AssociatedCalibrationFactorsSetName = 'V8486B'
for freq in cal.keys():
	sensor.Frequency = freq
	print(sensor.Power)