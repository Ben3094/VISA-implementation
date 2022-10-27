from time import sleep
from KeysightN6705C import KeysightN6705C

scr = KeysightN6705C("TCPIP0::k-n6705c-05944::inst0::INSTR")
scr.Connect()
channel1 = next((channel for channel in scr.Outputs if channel.Address == 1), None)
print(channel1.Model)
print(channel1.Options)
print(channel1.SerialNumber)
print(channel1.Conditions)
channel1.MaxVoltage = 5
print(channel1.MaxVoltage)
channel1.MaxCurrent = 1.5
print(channel1.MaxCurrent)
channel1.IsEnabled = True
sleep(1)
print(channel1.Conditions)