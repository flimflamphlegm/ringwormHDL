from verilogModule import verilogModule
from writeToFile import writeToFile

"""
generate - class for generating test structures (ring oscillators)
"""
class generate:
    """
    RO_not_gen: Generates a ring oscillator circuit of size n with NOT gates, where n is a positive odd integer.
    n - number of stages in RO (int)
    in_p - name of input enable port (str)
    out_p - name of output clock port (str)
    """
    def RO_not(n,in_p,out_p,newFile):
        ringOsc = verilogModule("RO_not_" + str(n)) #create a new verilog module named "RO_not_n" where n is number of stages
        ringOsc.port(in_p,"i") #set the input/output ports as defined by the user
        ringOsc.port(out_p,"o")
        ringOsc.logic("a0",1) 
        for i in range(n): #create n number of logic types
            ringOsc.logic("r" + str(i),1)
        ringOsc.assign("a0",1,0,in_p + " & r" + str(n - 1),1,0) #set the enable gate
        ringOsc.assign("r0",1,0,"!a0",1,0)
        for i in range(n - 1): #create n number of inverter stages
            ringOsc.assign("r" + str(i + 1),1,0,"!r" + str(i),1,0)
        ringOsc.assign(out_p,1,0,"r" + str(n - 1),1,0)
        newFile.writeModule(ringOsc) #writes module created above to the new file 

        print("RO_not of " + str(n) + " generated")

    """
    RO_nand_gen: Generates a ring oscillator circuit of size n with NAND gates, where n is a positive odd integer.
    n - number of stages in RO (int)
    in_p - name of input enable port (str)
    out_p - name of output clock port (str)
    """
    def RO_nand(n,in_p,out_p,newFile):
        ringOsc = verilogModule("RO_nand_" + str(n)) #create a new verilog module named "RO_nand_n" where n is number of stages
        ringOsc.port(in_p,"i") #set the input/output ports as defined by the user
        ringOsc.port(out_p,"o")
        ringOsc.logic("a0",1) 
        for i in range(n): #create n number of logic types
            ringOsc.logic("r" + str(i),1)
        ringOsc.assign("a0",1,0,in_p + " & r" + str(n - 1),1,0) #set the enable gate
        ringOsc.assign("r0",1,0,"!(a0 & a0)",1,0)
        for i in range(n - 1): #create n number of inverter stages
            ringOsc.assign("r" + str(i + 1),1,0,"!(r" + str(i) + " & r" + str(i) + ")",1,0)
        ringOsc.assign(out_p,1,0,"r" + str(n - 1),1,0)
        newFile.writeModule(ringOsc) #writes module created above to the new file 

        print("RO_nand of " + str(n) + " generated")

    """
    RO_nor_gen: Generates a ring oscillator circuit of size n with NOR gates, where n is a positive odd integer.
    n - number of stages in RO (int)
    in_p - name of input enable port (str)
    out_p - name of output clock port (str)
    """
    def RO_nor(n,in_p,out_p,newFile):
        ringOsc = verilogModule("RO_nor_" + str(n)) #create a new verilog module named "RO_nand_n" where n is number of stages
        ringOsc.port(in_p,"i") #set the input/output ports as defined by the user
        ringOsc.port(out_p,"o")
        ringOsc.logic("a0",1) 
        for i in range(n): #create n number of logic types
            ringOsc.logic("r" + str(i),1)
        ringOsc.assign("a0",1,0,in_p + " & r" + str(n - 1),1,0) #set the enable gate
        ringOsc.assign("r0",1,0,"!(a0 | a0)",1,0)
        for i in range(n - 1): #create n number of inverter stages
            ringOsc.assign("r" + str(i + 1),1,0,"!(r" + str(i) + " | r" + str(i) + ")",1,0)
        ringOsc.assign(out_p,1,0,"r" + str(n - 1),1,0)
        newFile.writeModule(ringOsc) #writes module created above to the new file 

        print("RO_nor of " + str(n) + " generated")
