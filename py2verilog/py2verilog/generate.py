from verilogModule import verilogModule
from writeToFile import writeToFile

"""
generate - class for generating test structures (ring oscillators)
"""
class generate:
    """
    __init__: stores names of all generated modules so that they can be connected in the top module
    self.modules - list of module names (str)
    self.inputs - list of list of module input names (List[List[str]])
    self.outputs - list of list of module output names (List[List[str]])
    """
    def __init__(self):
        self.modules = []
        self.inputs = []
        self.outputs = []

    """
    RO_not_gen: Generates a ring oscillator circuit of size n with NOT gates, where n is a positive odd integer.
    n - number of stages in RO (int)
    in_p - name of input enable port (str)
    out_p - name of output clock port (str)
    """
    def RO_not(self,n,in_p,out_p,newFile):
        moduleName = "RO_not_{stages}_{instance}".format(stages=str(n),instance=str(len(self.modules)))
        ringOsc = verilogModule(moduleName) #create a new verilog module named "RO_not_n_i" where n is number of stages and i is instance number
        ringOsc.port(in_p,"i") #set the input/output ports as defined by the user
        ringOsc.port(out_p,"o")
        ringOsc.logic("a0",1) 
        for i in range(n): #create n number of logic types
            ringOsc.logic("r{num}".format(num=str(i)),1)
        ringOsc.assign("a0","!({input} & r{num})".format(input=in_p,num=str(n - 1))) #set the enable gate, assign default is 1 bit wire, can specify width manually
        ringOsc.assign("r0","!a0")
        for i in range(n - 2): #create n number of inverter stages
            ringOsc.assign("r{num}".format(num=str(i + 1)),"!r{num}".format(num=str(i))) 
        ringOsc.assign(out_p,"r{num}".format(num=str(n - 2)))
        newFile.writeSubModule(ringOsc) #writes module created above to the new file 

        self.modules.append(moduleName) #save name and ports so that they can be connected in top module later
        self.inputs.append([in_p])
        self.outputs.append([out_p])
        print("RO_not of {num} generated".format(num=str(n)))

    """
    RO_nand_gen: Generates a ring oscillator circuit of size n with NAND gates, where n is a positive odd integer.
    n - number of stages in RO (int)
    in_p - name of input enable port (str)
    out_p - name of output clock port (str)
    """
    def RO_nand(self,n,in_p,out_p,newFile):
        moduleName = "RO_nand_{stages}_{instance}".format(stages=str(n),instance=str(len(self.modules)))
        ringOsc = verilogModule(moduleName) #create a new verilog module named "RO_nand_n_i" where n is number of stages and i is instance number
        ringOsc.port(in_p,"i") #set the input/output ports as defined by the user
        ringOsc.port(out_p,"o")
        ringOsc.logic("a0",1) 
        for i in range(n): #create n number of logic types
            ringOsc.logic("r{num}".format(num=str(i)),1)
        ringOsc.assign("a0","!({input} & r{num})".format(input=in_p,num=str(n - 1))) #set the enable gate, assign default is 1 bit wire, can specify width manually
        ringOsc.assign("r0","!(a0 & a0)")
        for i in range(n - 2): #create n number of inverter stages
            ringOsc.assign("r{num}".format(num=str(i + 1)),"!(r{num} & r{num})".format(num=str(i))) 
        ringOsc.assign(out_p,"r{num}".format(num=str(n - 2)))
        newFile.writeSubModule(ringOsc) #writes module created above to the new file 

        self.modules.append(moduleName) #save name and ports so that they can be connected in top module later
        self.inputs.append([in_p])
        self.outputs.append([out_p])
        print("RO_nand of {num} generated".format(num=str(n)))

    """
    RO_nor_gen: Generates a ring oscillator circuit of size n with NOR gates, where n is a positive odd integer.
    n - number of stages in RO (int)
    in_p - name of input enable port (str)
    out_p - name of output clock port (str)
    """
    def RO_nor(self,n,in_p,out_p,newFile):
        moduleName = "RO_nor_{stages}_{instance}".format(stages=str(n),instance=str(len(self.modules)))
        ringOsc = verilogModule(moduleName) #create a new verilog module named "RO_nor_n_i" where n is number of stages and i is instance number
        ringOsc.port(in_p,"i") #set the input/output ports as defined by the user
        ringOsc.port(out_p,"o")
        ringOsc.logic("a0",1) 
        for i in range(n): #create n number of logic types
            ringOsc.logic("r{num}".format(num=str(i)),1)
        ringOsc.assign("a0","!({input} & r{num})".format(input=in_p,num=str(n - 1))) #set the enable gate, assign default is 1 bit wire, can specify width manually
        ringOsc.assign("r0","!(a0 | a0)")
        for i in range(n - 2): #create n number of inverter stages
            ringOsc.assign("r{num}".format(num=str(i + 1)),"!(r{num} | r{num})".format(num=str(i))) 
        ringOsc.assign(out_p,"r{num}".format(num=str(n - 2)))
        newFile.writeSubModule(ringOsc) #writes module created above to the new file 

        self.modules.append(moduleName) #save name and ports so that they can be connected in top module later
        self.inputs.append([in_p])
        self.outputs.append([out_p])
        print("RO_nor of {num} generated".format(num=str(n)))
