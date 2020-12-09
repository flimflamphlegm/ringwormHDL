"""
stuff2ad:
    random test stuffs from:
        An On-die Digital Aging Monitor against HCI and xBTI in 16 nm Fin-FET Bulk CMOS Technology
        Fast Characterization of PBTI and NBTI Induced Frequency Shifts under a Realistic Recovery Bias Using a Ring Oscillator Based Circuit
        Reliability monitoring ring oscillator structures for isolated/combined NBTI and PBTI measurement in high-k metal gate technologies
        A Ring-Oscillator-Based Reliability Monitor for Isolated Measurement of NBTI and PBTI in High-k/Metal Gate Technology
        A fWLR test structure and method for device reliability monitoring using product relevant circuits
        PBTI/NBTI monitoring ring oscillator circuits with on-chip Vt characterization and high frequency AC stress capability
    different logic gate ROs?
    on-chip memory?
    various RO lengths
    class functions for ROs in parallel
    class functions for ROs connected to IO vs. power interally
"""

class writeToFile:
    """
    initialization creates new file with specified file name
    """
    def __init__(self,fileName):
        self.fileName = fileName
        file = open(fileName,"w") #overwrites existing copy of file, start from blank file
        file.close()
    """
    writeModule: writes the module to the file, takes file name from writeToFile instance
    module - verilogModule class instance
    """
    def writeModule(self,module):
        file = open(self.fileName , "a") #open file to append
        file.write("module " + module.moduleName + "\n")
        #writing parameters
        temp = []
        for key,val in module.parameters.items(): #convert dict to list 
            temp.append("{k} = {v}".format(k=key,v=val))
        file.write("\t#(" + ",\n".join(temp) + ")\n") #convert list to string and write
        #writing ports
        temp.clear()
        for key,val in module.ports.items(): #convert dict to list 
            if val == "i":
                temp.append("input logic {}".format(key))
            else: #we check earlier that these have to be "i" or "o" so we can just else here
                temp.append("output logic {}".format(key))
        file.write("\t(" + ",\n\t".join(temp) + ");\n") #convert list to string and write
        #writing logic decl.
        temp.clear()
        for key,val in module.logics.items(): #convert dict to list 
            temp.append("logic {}".format(key))
        file.write("\t" + ",\n\t".join(temp) + "\n") #convert list to string and write
        #writing comb. logic
        temp.clear()
        for key,val in module.combinational.items(): #convert dict to list 
            if key[0:6] == "ASSIGN": #check what kind of statement it is
                temp.append("assign {l} = {r}".format(l=val[0],r=val[3]))
        file.write("\t" + ";\n\t".join(temp) + "\n") #convert list to string and write
        #end
        file.write("endmodule\n\n")
        file.close()

class verilogModule:
    """
    sequential logic 
    """
    def ifStatement(self):
        pass
    def elseStatement(self):
        pass
    def elifStatement(self):
        pass
    def forLoop(self):
        pass
    """
    __init__: takes string "name" and instantiates a Verilog/SystemVerilog module with that name
    *dicts are ordered in python 3.6+, use OrderedDict if older version*
    self.parameters - a dict of all the module parameters
    self.ports - a dict of all the module ports, where 0 = input and 1 = output
    self.sequential - a list of all sequential logic, where the 0th element is the first command executed in the sequential (always) block
    self.logic - a dict of all logic defines (wire/regs), where the order is based on input order
    self.combinational - a dict of all combinational logic, where the order is irrelevant (since it's combinational logic)
    """
    def __init__(self,moduleName):
        self.moduleName = moduleName
        self.parameters = {} 
        self.ports = {}
        self.sequential = []
        self.logics = {}
        self.combinational = {}
    """
    parameter: takes parameter name, value, and adds them to the module
    returns tuple of type,name,value ("error") if could not add
    p - name of parameter (str)
    i - value of parameter (int)
    """
    def parameter(self,p,i):
        if p not in self.parameters:
            self.parameters[p] = i;
        else: #can't update the value of a parameter as it has to be a constant
            print("Parameter {} already exists!".format(p))
            return ("error")
        return ("PARAMETER",p,i) 
    """
    ports: takes port name, direction, and adds them to the module
    returns tuple of type,name,direction, ("error") if could not add
    p - name of port (str)
    dir - direction of port, use "i" to designate input, and "o" to designate output (str)
    """
    def port(self,p,dir):
        if p not in self.ports:
            if dir == "i" or dir == "o": #make sure it's a valid direction
                self.ports[p] = dir
        else: #cannot redefine port that already exists
            print("Port {} already exists!".format(p))
            return ("error")
        return ("PORT",p,dir)
    """
    logic: use to create a logic (wire/reg) "w" bits wide
    returns tuple of name/type/width, ("error") if could not add
    p - name (str)
    w - width (int)
    """
    def logic(self,p,w):
        if p not in self.logics:
            if w > 0: #can't have a 0 width wire/reg
                self.logics[p] = w
        else: #cannot redefine logic that already exists
            print("Logic {} already exists!".format(p))
            return ("error")
        return ("LOGIC",p,w)

    """
    assign: takes lhs and rhs values, along with their bit widths, and creates an assign statement
    returns a tuple of type and index in combinational dict
    l - lh WIRE ONLY
    lw - left bit [_:0]
    lwd - right bit [7:_]
    l - rh wire/reg
    rw - left bit [_:0]
    rwd - right bit [7:_]
    """
    def assign(self,l,lw,lwd,r,rw,rwd):
        if lw != lwd and rw != rwd: #can't have a 0 width wire
            temp = "ASSIGN" + str(len(self.combinational) + 1) #get new dict key
            self.combinational[temp] = (l,lw,lwd,r,rw,rwd)
        else:
            print("Can't have a 0 width wire!")
            return ("error")
        return ("ASSIGN",temp)
class generate:
    """
    gen: Generates a ring oscillator circuit of size n, where n is a positive odd integer.
    n - number of stages in RO (int)
    in_p - name of input enable port (str)
    out_p - name of output clock port (str)
    """
    def RO(n,in_p,out_p):
        if n % 2 == 0 or n <= 2: #need at least 3 stages, and has to be an odd number of stages
            return -1
        ringOsc = verilogModule("RO_" + str(n)) #create a new verilog module named "RO_n" where n is number of stages
        ringOsc.parameter("n",8)
        ringOsc.port(in_p,"i") #set the input/output ports as defined by the user
        ringOsc.port(out_p,"o")
        ringOsc.logic("a0",1) 
        for i in range(n): #create n number of logic types
            ringOsc.logic("r" + str(i),1)
        ringOsc.assign("a0",1,0,str(in_p) + " & r" + str(n - 1),1,0) #set the enable gate
        ringOsc.assign("r0",1,0,"!a1",1,0)
        for i in range(n - 1):
            ringOsc.assign("r" + str(i + 1),1,0,"!r" + str(i),1,0)
        ringOsc.assign("outClk",1,0,"r" + str(n - 1),1,0)
        newFile.writeModule(ringOsc) #writes module created above to the new file 

        print("RO of " + str(n) + " generated")
        return 0

if __name__ == "__main__":
    newFile = writeToFile("ro.sv") #creates new file with name "ro.sv"
    print("Please enter the number of ring oscillators:")
    c = input()
    for i in range(int(c)):
        print("RO #" + str(i + 1) + ":")
        print("Please enter the name of the enable input port:")
        in_port = input()
        print("Please enter the name of the RO output port:")
        out_port = input()
        print("Please enter the number of stages (an odd number greater or equal to 3):")
        n = input()
        while (generate.RO(int(n),in_port,out_port) == -1):
            print("Invalid, please enter an odd number greater or equal to 3:")
            n = input()