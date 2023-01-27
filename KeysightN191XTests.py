from pyVirtualLab.Instruments.KeysightN191X import KeysightN191X, CalibrationFactorsSet
import pandas

powerMeter = KeysightN191X('TCPIP0::k-n1913a-80021.ies.univ-montp2.fr::inst0::INSTR')
powerMeter.Connect()
powerMeter.CalibrationFactorsSets['V8486A'] = CalibrationFactorsSet(powerMeter, 'V8486A')
cal = pandas.read_csv("V8486A calibration.csv")
cal = dict(zip(cal['Frequency (Hz)'], cal['Calibration factor (%)']))
powerMeter.CalibrationFactorsSets['CUSTOM_0'].CalibrationFactors = cal
powerMeter.CalibrationFactorsSets['CUSTOM_0'].Name = 'V8486A'