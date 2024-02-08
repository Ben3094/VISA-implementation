import pyvisa
import aenum
import enum
from re import match, Match
from pyvisa.resources import Resource
from time import time, sleep
from abc import abstractmethod

def GetProperty(dataType: type, visaGetCommand: str):
	__converter__ = None

	if dataType is float:
		__converter__ = lambda x: float(x)
	elif dataType is int:
		__converter__ = lambda x: int(x)
	elif dataType is bool:
		__converter__ = lambda x: bool(int(x))
	elif dataType is str:
		__converter__ = lambda x: x
	elif issubclass(dataType, aenum.Enum):
		__converter__ = lambda x: dataType(x)
	elif issubclass(dataType, enum.Enum):
		__converter__ = lambda x: dataType(x)
	else:
		raise Exception("No available converter")

	def decorator(func):
		def wrapper(*args, **kwargs):
			kwargs['getMethodReturn'] = __converter__(args[0].Query(visaGetCommand))
			return func(*args, **kwargs)
		return wrapper
	return decorator

def SetProperty(dataType: type, visaSetCommand: str):
	__converter__ = None

	if dataType is float:
		__converter__ = lambda x: str(float(x))
	elif dataType is int:
		__converter__ = lambda x: str(int(x))
	elif dataType is bool:
		__converter__ = lambda x: str(int(bool(x)))
	elif dataType is str:
		__converter__ = lambda x: str(x)
	elif issubclass(dataType, aenum.Enum):
		__converter__ = lambda x: str(dataType(x).value)
	elif issubclass(dataType, enum.Enum):
		__converter__ = lambda x: str(dataType(x).value)
	else:
		raise Exception("No available converter")

	def decorator(func):
		def wrapper(*args, **kwargs):
			args[0].Write(visaSetCommand, __converter__(args[1]))
			if getattr(args[0], func.__name__) != args[1]:
				raise Exception(f"Error while setting \"{func.__name__}\"")
			return func(*args, **kwargs)
		return wrapper
	return decorator

class VirtualResource:
	def __init__(self):
		pass

	@abstractmethod
	def write(self, value:str) -> None:
		pass
	@abstractmethod
	def read(self) -> str:
		pass
	@abstractmethod
	def query(self, value:str) -> str:
		pass

	@property
	@abstractmethod
	def timeout(self) -> float:
		pass
	@timeout.setter
	@abstractmethod
	def timeout(self, value:float):
		pass

# See IVI foundation VXI plug&play System Alliance VPP-9: Instrument Vendor Abbreviations
class VendorAbbreviation(aenum.Enum):
	AQ = "Acqiris"
	AC = "Applicos BV"
	AV = "Advantest Corporation"
	AF = "Aeroflex Laboratories"
	AG = "Agilent Technologies"
	AI = "AIM GmbH"
	AX = "AMETRIX Instruments"
	AM = "AMP Incorporated"
	AN = "Analogic, Corp."
	AD = "Ando Electric Company Limited"
	AU = "Anritsu Company"
	AT = "Astronics Test Systems Inc."
	AO = "AOIP Instrumentation"
	AS = "ASCOR Incorporated"
	AP = "Audio Precision, Inc"
	BB = "B&B Technologies"
	BA = "BAE Systems"
	BK = "Bruel & Kjaer"
	BU = "Bustec Production Ltd."
	CA = "CAL-AV Labs, Inc."
	CI = "Cambridge Instruments"
	CH = "C&H Technologies, Inc."
	CE = "Chyng Hong Electronic Co., Ltd"
	CM = "CMC Labs"
	CC = "Compressor Controls Corporation"
	CY = "CYTEC Corporation"
	DP = "Directed Perceptions Inc."
	DS = "DSP Technology Inc."
	EA = "EA Elektro-Automatik GmbH"
	EI = "EIP Microwave, Inc."
	EX = "EXFO Inc."
	FL = "Fluke Company Inc."
	FO = "fos4X GmbH"
	GR = "GenRad"
	GT = "Giga-tronics, Inc."
	GN = "gnubi communications, Inc."
	HP = "Hewlett-Packard Company"
	HH = "Hoecherl & Hackl GmbH"
	UN = "Holding “Informtest”"
	IS = "Intepro Systems"
	DV = "IBEKO POWER AB"
	IF = "IFR"
	IT = "Instrumental Systems Corporation"
	IE = "Instrumentation Engineering, Inc."
	IC = "Integrated Control Systems"
	KE = "Keithley Instruments"
	KP = "Kepco, Inc."
	KT = "Keysight Technologies"
	KI = "Kikusui Inc."
	LC = "LeCroy"
	LP = "LitePoint Corporation"
	MP = "MAC Panel Company"
	MT = "ManTech Test Systems"
	MI = "Marconi Instruments"
	MS = "Microscan"
	ML = "MIT Lincoln Laboratory"
	NI = "National Instruments Corp."
	NT = "NEUTRIK AG"
	ND = "Newland Design + Associates, Inc."
	NH = "NH Research"
	NA = "North Atlantic Instruments"
	PW = "Pacific MindWorks, Inc."
	PE = "PesMatrix Inc."
	PM = "Phase Metrics"
	PI = "Pickering Interfaces"
	PC = "Picotest"
	PT = "Power-Tek Inc."
	RI = "Racal Instruments, Inc."
	RQ = "Raditeq"
	RA = "Radisys Corp."
	RS = "Rohde & Schwarz GmbH"
	SL = "Schlumberger Technologies"
	SC = "Scicom"
	SR = "Scientific Research Corporation"
	# AU = "Serendipity Systems, Inc."
	SI = "SignalCraft Technologies Inc."
	ST = "Sony/Tektronix Corporation"
	SS = "Spectrum Signal Processing, Inc."
	SP = "Spitzenberger & Spies GmbH"
	TA = "Talon Instruments"
	TK = "Tektronix, Inc."
	TE = "Teradyne"
	TS = "Test & Measurement Systems Inc."
	RF = "ThinkRF Corporation"
	# AT = "Thurlby Thandar Instruments Limited Transmagnetics, Inc."
	TM = "Transmagnetics, Inc."
	TP = "TSE Plazotta"
	TT = "TTI Testron, Inc."
	US = "Universal Switching Corporation"
	VE = "Vencon Technologies Inc."
	XR = "Versatile Power"
	VP = "Virginia Panel, Corp."
	VT = "VXI Technology, Inc."
	VA = "VXIbus Associates, Inc."
	WT = "Wavetek Corp."
	WG = "Wandel & Goltermann"
	WZ = "Welzek"
	YK = "Yokogawa Electric Corporation"
	ZT = "ZTEC"

ADDRESS_GRAMMAR_SEPARATOR:str = "::"

INTERFACE_TYPE_ENTRY_NAME:str = "Interface type"
class InterfaceType(aenum.Enum):
	VXI = 'VXI'
	GPIB_VXI = 'GPIB-VXI'
	GPIB = 'GPIB'
	Serial = 'ASRL' # Means "Asynchronous SeRiaL"
	Ethernet = 'TCPIP'
	USB = 'USB'
	PXI = 'PXI'
INTERFACE_BOARD_ENTRY_NAME:str = "Interface board"
PXI_BUS_ENTRY_NAME:str = "PXI bus"
PXI_INTERFACE_ENTRY_NAME:str = "PXI interface"
def PARSE_INTERFACE_TYPE(value: str) -> tuple[InterfaceType, int]:
	rematch:Match = None
	for interfaceType in InterfaceType:
		for interfaceTypeString in interfaceType.values:
			rematch = match(f"{interfaceTypeString}(\d*)", value)
			if rematch:
				return (interfaceType, int(rematch[1]) if rematch[1] != '' else None)
	raise Exception("Unknown instrument type")
VXI_LOGICAL_ADDRESS_ENTRY_NAME:str = "Logical address"
GPIB_ADDRESS_ENTRY_NAME:str = "GPIB address"
GPIB_SECONDARY_ADDRESS_ENTRY_NAME:str = "GPIB secondary address"
ETHERNET_DEVICE_NAME_ENTRY_NAME:str = "Device name"
ETHERNET_HOST_ADDRESS_ENTRY_NAME:str = "Host address"
ETHERNET_PORT_ENTRY_NAME:str = "Port"
USB_MANUFACTURER_ID_ENTRY_NAME:str = "Manufacturer ID"
USB_MODEL_CODE_ENTRY_NAME:str = "Model code"
USB_SERIAL_NUMBER_ENTRY_NAME:str = "Serial number"
USB_INTERFACE_NUMBER_ENTRY_NAME:str = "Interface number"
PXI_CHASSIS_NUMBER_ENTRY_NAME:str = "Chassis number"

class ResourceType(aenum.Enum):
	Instrument = 'INSTR'
	MemoryAccess = 'MEMACC'
	GPIBBus = 'INTFC'
	Backplane = 'BACKPLANE' # Hosts one or several VXI or PXI instruments
	Servant = 'SERVANT'
	Socket = 'SOCKET'
def PARSE_RESOURCE_TYPE(value) -> ResourceType:
	rematch:Match = None
	for resourceType in ResourceType:
		for resourceTypeString in resourceType.values:
			rematch = match(resourceTypeString, value)
			if rematch:
				return resourceType
	raise Exception("Unknown resource type")

def PARSE_ADDRESS(value:str) -> tuple[InterfaceType, dict[str, object], ResourceType]:
	interfaceProperties:dict[str, object] = dict()
	value = value.split(ADDRESS_GRAMMAR_SEPARATOR)

	interfaceType, interfaceIndex = PARSE_INTERFACE_TYPE(value[0])
	try:
		resourceType = PARSE_RESOURCE_TYPE(value[-1])
		del value[-1]
	except Exception:
		resourceType = ResourceType.Instrument

	match interfaceType:
		case InterfaceType.VXI:
			interfaceProperties[INTERFACE_BOARD_ENTRY_NAME] = interfaceIndex
			match resourceType:
				case ResourceType.MemoryAccess|ResourceType.Servant:
					pass
				case ResourceType.Backplane|ResourceType.Instrument:
					interfaceProperties[VXI_LOGICAL_ADDRESS_ENTRY_NAME] = value[1]
				case _:
					raise Exception("Resource type is not suitable for a VXI interface")
		case InterfaceType.GPIB_VXI:
			interfaceProperties[INTERFACE_BOARD_ENTRY_NAME] = interfaceIndex
			match resourceType:
				case ResourceType.MemoryAccess:
					pass
				case ResourceType.Backplane|ResourceType.Instrument:
					interfaceProperties[VXI_LOGICAL_ADDRESS_ENTRY_NAME] = value[1]
				case _:
					raise Exception("Resource type is not suitable for a GPIB-VXI interface")

		case InterfaceType.GPIB:
			interfaceProperties[INTERFACE_BOARD_ENTRY_NAME] = interfaceIndex
			match resourceType:
				case ResourceType.GPIBBus|ResourceType.Servant:
					pass
				case ResourceType.Instrument:
					interfaceProperties[GPIB_ADDRESS_ENTRY_NAME] = value[1]
					interfaceProperties[GPIB_SECONDARY_ADDRESS_ENTRY_NAME] = value[2]
		case InterfaceType.Serial:
			interfaceProperties[INTERFACE_BOARD_ENTRY_NAME] = interfaceIndex

		case InterfaceType.Ethernet:
			interfaceProperties[INTERFACE_BOARD_ENTRY_NAME] = interfaceIndex
			if resourceType == ResourceType.Servant:
				interfaceProperties[ETHERNET_DEVICE_NAME_ENTRY_NAME] = value[1]
			else:
				interfaceProperties[ETHERNET_HOST_ADDRESS_ENTRY_NAME] = value[1]
				if resourceType == ResourceType.Socket:
					interfaceProperties[ETHERNET_PORT_ENTRY_NAME] = int(value[2])
				else:
					interfaceProperties[ETHERNET_DEVICE_NAME_ENTRY_NAME] = value[2]
					if len(value) > 3:
						interfaceProperties[ETHERNET_PORT_ENTRY_NAME] = int(value[3])	

		case InterfaceType.USB:
			interfaceProperties[INTERFACE_BOARD_ENTRY_NAME] = interfaceIndex
			interfaceProperties[USB_MANUFACTURER_ID_ENTRY_NAME] = value[1]
			interfaceProperties[USB_MODEL_CODE_ENTRY_NAME] = value[2]
			interfaceProperties[USB_SERIAL_NUMBER_ENTRY_NAME] = value[3]
			if len(value) > 4:
				interfaceProperties[USB_INTERFACE_NUMBER_ENTRY_NAME] = value[4]
		case InterfaceType.PXI:
			match resourceType:
				case ResourceType.Backplane:
					interfaceProperties[INTERFACE_BOARD_ENTRY_NAME] = interfaceIndex
					interfaceProperties[PXI_CHASSIS_NUMBER_ENTRY_NAME] = value[1]
				case ResourceType.MemoryAccess:
					interfaceProperties[INTERFACE_BOARD_ENTRY_NAME] = interfaceIndex
				case ResourceType.Instrument:
					raise NotImplementedError()

	return interfaceType, interfaceProperties, resourceType

DEFAULT_RESOURCE_MANAGER = pyvisa.ResourceManager('@py')

class Instrument:
	DEFAULT_VISA_TIMEOUT = 2000

	Id:str = None
	Vendor:str = None
	Model:str = None
	Firmware:str = None

	def __init__(self, address: str=None, visaTimeout:int=DEFAULT_VISA_TIMEOUT):
		self.__address__ = None
		self.__isConnected__ = False
		self.__timeout__ = visaTimeout
		self.__resource__:Resource|VirtualResource = None
		self.__interfaceType__:InterfaceType = None
		self.__interfaceProperties__:dict[str, object] = dict()
		self.__resourceType__:ResourceType = None
		self.Address = address

	@property
	def Resource(self):
		return self.__resource__
	@Resource.setter
	def Resource(self, value):
		isConnected = self.IsConnected
		if isConnected:
			self.Disconnect()
		self.__resource__ = value
		if isConnected:
			self.Connect()

	# See "VPP-4.3: The VISA Library" at 4.3.1.1 section
	@property
	def Address(self) -> str:
		return self.__address__
	@Address.setter
	def Address(self, value: str) -> str:
		if value != self.Address:
			self.__address__ = str(value)
			self.__interfaceType__, self.__interfaceProperties__, self.__resourceType__ = PARSE_ADDRESS(value)
			if self.IsConnected:
				self.Disconnect()
				self.Connect()
		return self.__address__
	
	@property
	def InterfaceType(self):
		return self.__interfaceType__
	@property
	def InterfaceProperties(self) -> dict[str, object]:
		return self.__interfaceProperties__
	@property
	def ResourceType(self):
		return self.__resourceType__

	@property
	def Timeout(self) -> int:
		return self.__timeout__
	@Timeout.setter
	def Timeout(self, value: int):
		if value != self.__timeout__:
			self.__timeout__ = int(value)
			if self.IsConnected:
				self.Disconnect()
				self.Connect()

	@property
	def IsConnected(self) -> bool:
		return self.__isConnected__
		
	def Connect(self) -> bool:
		self.__isConnected__ = True
		try:
			if self.__resource__ is VirtualResource:
				self.__resource__ = self.__resource__
			else:
				self.__resource__ = DEFAULT_RESOURCE_MANAGER.open_resource(self.Address)
			self.__resource__.timeout = self.Timeout
			self.Id = self.__updateId__()
			self.Vendor = self.__updateVendor__()
			self.Model, self.Firmware = self.__updateModelAndFirmware__()
		except Exception as e:
			self.__isConnected__ = False
			raise e
		return self.__isConnected__

	def Disconnect(self) -> bool:
		self.__resource__.close()
		self.__isConnected__ = False
		return self.__isConnected__
	def close(self) -> None:
		self.Disconnect()
			
	# See IVI fundation SCPI Volume 1: Syntax and Style
	def Write(self, command: str, args:str=''):
		args = str(args)
		if self.IsConnected:
			return self.__resource__.write(command + ((' ' + args) if args != '' else ''))
		else:
			raise Exception("The instrument is not connected")

	def Query(self, command: str, args:str=''):
		args = str(args)
		if self.IsConnected:
			return str(self.__resource__.query(command + '?' + ((' ' + args) if args != '' else ''))).strip('\n').strip('\r').strip('"').lstrip(':').removeprefix(command).strip()
		else:
			raise Exception("The instrument is not connected")

	def Read(self) -> str:
		if self.IsConnected:
			return str(self.__resource__.read()).strip('\n')
		else:
			raise Exception("The instrument is not connected")

	def __updateId__(self) -> str:
		if self.IsConnected:
			return self.__resource__.query('*IDN?')
		else:
			raise Exception("The instrument is not connected")
	
	def __updateVendor__(self, check=False) -> VendorAbbreviation or str:
		rematch:Match = None
		for vendorAbbreviation in VendorAbbreviation:
			for value in vendorAbbreviation.values:
				rematch = match(value, self.Id)
				if rematch:
					return vendorAbbreviation
		if check:
			raise Exception("Unknown manufacturer")
		return self.Id.split(',')[0]
		
	def __updateModelAndFirmware__(self):
		modelAndFirmware = self.Id.removeprefix(self.Vendor.value).rstrip().rstrip('\n').split(',', 2)
		return modelAndFirmware[1], modelAndFirmware[2]
	
	def Wait(self, delay:float=0.01, timeout:float=5):
		startTime:float = time()
		stopTime = startTime+timeout
		while (time() < stopTime) & (self.Query('*OPC') != '1'):
			sleep(delay)

	def SelfTest(self):
		if self.IsConnected:
			if not bool(int(self.__resource__.query('*TST?'))):
				raise Exception('Error in the self test')
		else:
			raise Exception("The instrument is not connected")
	
	def Reset(self):
		if self.IsConnected:
			self.__resource__.write('*RST')
		else:
			raise Exception("The instrument is not connected")

class Source(Instrument):
	def __abort__(self):
		self.Reset()

	def __init__(self, address, visaTimeout=Instrument.DEFAULT_VISA_TIMEOUT):
		Instrument.__init__(self, address, visaTimeout)
		self.Abort = self.__abort__

def RECURSIVE_SUBCLASSES(type:type) -> list[type]:
	currentLevelSubclasses = type.__subclasses__()
	deeperLevelSubclasses:list = list()
	for currentLevelSubclass in currentLevelSubclasses:
		deeperLevelSubclasses = deeperLevelSubclasses + RECURSIVE_SUBCLASSES(currentLevelSubclass)
	return currentLevelSubclasses + deeperLevelSubclasses