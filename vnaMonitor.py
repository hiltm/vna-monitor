import pyvisa

vna = 'TCPIP0::localhost::hislip0::INSTR'
rm = pyvisa.ResourceManager()
inst = rm.open_resource(vna)
inst.timeout = 20000
 
print(inst.query("*IDN?"))
