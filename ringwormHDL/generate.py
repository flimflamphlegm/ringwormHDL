from verilogModule import verilogModule
from writeToFile import writeToFile


class generate:
    """
    generate - class for generating test structures (ring oscillators)
    """
    
    def __init__(self) -> None:
        """
        __init__: stores names of all generated modules so that they can be connected in the top module
        self.modules - list of module names (List[str])
        self.inputs - list of list of module input names (List[List[str]]), where the index = module number
        self.outputs - list of list of module output names (List[List[str]]), where the index = module number
        """
        self.modules = []
        self.inputs = []
        self.outputs = []


    def RO_not(self, n:int, in_p:str, out_p:str, newFile:writeToFile) -> str:
        """
        RO_not: Generates a ring oscillator circuit of size n with NOT gates, where n is a positive odd integer.
        Writes module to file specified, returns module name
        n - number of stages in RO (int)
        in_p - name of input enable port (str)
        newFile - writeToFile object
        """
        moduleName = "RO_not_{stages}_{instance}".format(stages=str(n),instance=str(len(self.modules)))
        ringOsc = verilogModule(moduleName)                                         #create a new verilog module named "RO_not_n_i" where n is number of stages and i is instance number
        ringOsc.port(in_p,"i")                                                      #set the input enable port as defined by the user
        ringOsc.port(out_p,"o")                                                     #set the output port as defined by the user
        ringOsc.logic("a0",1,"synthesis keep")                                      #create "logic" data types for connecting gates   
        for i in range(n - 1):                                                      
            ringOsc.logic("r{num}".format(num=str(i)),1,"synthesis keep")           #the /*synthesis keep*/ tag tells Quartus to not optimize it out
        ringOsc.nandGate("a0",in_p,"r{n}".format(n=str(n - 2)),"synthesis keep")    #set the enable gate
        ringOsc.notGate("r0","a0","synthesis keep")
        for i in range(n - 2):                                                      #create n number of inverter stages
            ringOsc.notGate("r{num}".format(num=str(i + 1)),"r{num}".format(num=str(i)),"synthesis keep") 
        ringOsc.assign(out_p,"r{num}".format(num=str(n - 2)),"synthesis keep")      #assign bit width is adjustable
        newFile.writeSubModule(ringOsc)                                             #writes module created above to the new file 

        self.modules.append(moduleName)                                             #save name and ports so that they can be connected in top module later
        self.inputs.append([in_p])
        self.outputs.append([out_p])
        print("RO_not of {num} generated".format(num=str(n)))
        return moduleName


    def RO_nand(self, n:int, in_p:str, out_p:str, newFile:writeToFile) -> str:
        """
        RO_nand: Generates a ring oscillator circuit of size n with NAND gates, where n is a positive odd integer.
        Writes module to file specified, returns module name
        n - number of stages in RO (int)
        in_p - name of input enable port (str)
        out_p - name of output clock port (str)
        newFile - writeToFile object
        """
        moduleName = "RO_nand_{stages}_{instance}".format(stages=str(n),instance=str(len(self.modules)))
        ringOsc = verilogModule(moduleName)                                         #create a new verilog module named "RO_nand_n_i" where n is number of stages and i is instance number
        ringOsc.port(in_p,"i")                                                      #set the input enable port as defined by the user
        ringOsc.port(out_p,"o")                                                     #set the output port as defined by the user
        ringOsc.logic("a0",1,"synthesis keep")                                      #create "logic" data types for connecting gates   
        for i in range(n - 1):                                                      
            ringOsc.logic("r{num}".format(num=str(i)),1,"synthesis keep")           #the /*synthesis keep*/ tag tells Quartus to not optimize it out
        ringOsc.nandGate("a0",in_p,"r{n}".format(n=str(n - 2)),"synthesis keep")    #set the enable gate
        ringOsc.nandGate("r0","a0","a0","synthesis keep")
        for i in range(n - 2):                                                      #create n number of inverter stages
            ringOsc.nandGate("r{num}".format(num=str(i + 1)),"r{num}".format(num=str(i)),"r{num}".format(num=str(i)),"synthesis keep") 
        ringOsc.assign(out_p,"r{num}".format(num=str(n - 2)),"synthesis keep")
        newFile.writeSubModule(ringOsc)                                             #writes module created above to the new file 

        self.modules.append(moduleName)                                             #save name and ports so that they can be connected in top module later
        self.inputs.append([in_p])
        self.outputs.append([out_p])
        print("RO_nand of {num} generated".format(num=str(n)))
        return moduleName

    
    def RO_nor(self, n:int, in_p:str, out_p:str, newFile:writeToFile) -> str:
        """
        RO_nor: Generates a ring oscillator circuit of size n with NOR gates, where n is a positive odd integer.
        Writes module to file specified, returns module name
        n - number of stages in RO (int)
        in_p - name of input enable port (str)
        out_p - name of output clock port (str)
        newFile - writeToFile object
        """
        moduleName = "RO_nor_{stages}_{instance}".format(stages=str(n),instance=str(len(self.modules)))
        ringOsc = verilogModule(moduleName)                                         #create a new verilog module named "RO_nor_n_i" where n is number of stages and i is instance number
        ringOsc.port(in_p,"i")                                                      #set the input enable port as defined by the user
        ringOsc.port(out_p,"o")                                                     #set the output port as defined by the user
        ringOsc.logic("a0",1,"synthesis keep")                                      #create "logic" data types for connecting gates
        for i in range(n - 1):                                                      
            ringOsc.logic("r{num}".format(num=str(i)),1,"synthesis keep")           #the /*synthesis keep*/ tag tells Quartus to not optimize it out
        ringOsc.nandGate("a0",in_p,"r{n}".format(n=str(n - 2)),"synthesis keep")    #set the enable gate
        ringOsc.norGate("r0","a0","a0","synthesis keep")
        for i in range(n - 2):                                                      #create n number of inverter stages
            ringOsc.norGate("r{num}".format(num=str(i + 1)),"r{num}".format(num=str(i)),"r{num}".format(num=str(i)),"synthesis keep")  
        ringOsc.assign(out_p,"r{num}".format(num=str(n - 2)),"synthesis keep")
        newFile.writeSubModule(ringOsc)                                             #writes module created above to the new file 

        self.modules.append(moduleName)                                             #save name and ports so that they can be connected in top module later
        self.inputs.append([in_p])
        self.outputs.append([out_p])
        print("RO_nor of {num} generated".format(num=str(n)))
        return moduleName

    
    """
    Verilog that is generated based on code from Prof. Land @ Cornell: 
    https://people.ece.cornell.edu/land/courses/ece5760/DE1_SOC/Memory/index.html
    """
    def onChipMem(self, d:str, wren:str, clk:str, write_addr:str, read_addr:str, q:str, newFile:writeToFile) -> str:
        """
        onChipMem: Generates M10K on chip memory (for DE1-SoC, may need to be tweaked depending on which FPGA board is used)
        returns module name
        d - input data signal (str)
        wren - write enable signal (str)
        clk - clock signal (str)
        write_addr - write address (str)
        read_addr - read address (str)
        q - output (str)
        newFile - writeToFile object
        """
        moduleName = "mem_M10K_{instance}".format(instance=str(len(self.modules)))
        memory = verilogModule(moduleName)                                         #create a new Verilog module named "mem_M10K_i" where i is instance number
        memory.port(d,"i",32)                                                      #input data signal
        memory.port(wren,"i")                                                      #input write enable
        memory.port(clk,"i")                                                       #input clock
        memory.port(write_addr,"i",8)                                              #input write address
        memory.port(read_addr,"i",8)                                               #input read address
        memory.port(q,"o",32)                                                      #output data
        memory.logic("mem [255:0]",32,'synthesis ramstyle = "no_rw_check, M10K"')  #add synthesis parameter to force M10K 
        i = memory.alwaysSequential([{clk:"p"}])                                   #always @(posedge clk) begin
        memory.ifStatement(i,wren,"mem[{w_a}] <= {din}".format(w_a=write_addr,din=d))
        memory.nbAssign(i,q,"mem[{r_a}]".format(r_a=read_addr))
        newFile.writeSubModule(memory)                                             #writes module created above to the new file 

        self.modules.append(moduleName)                                            #save name and ports so that they can be connected in top module later
        self.inputs.append([d,wren,clk,write_addr,read_addr])
        self.outputs.append([q])
        print("M10K memory block generated")
        return moduleName
