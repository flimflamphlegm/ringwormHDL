"""
verilogModule - class for generating SystemVerilog modules
"""
class verilogModule:
    """
    __init__: takes string "name" and instantiates a Verilog/SystemVerilog module with that name
    *dicts are ordered in python 3.6+, use OrderedDict if older version*
    self.parameters - a dict of all the module parameters
    self.ports - a dict of all the module ports, where 0 = input and 1 = output
    self.sequential - a list of all sequential logic, where the 0th element is the first command executed in the sequential (always) block
    self.logic - a dict of all logic defines (wire/regs), where the order is based on input order
    self.combinational - a dict of all combinational logic, where all are syntehsized with the tag /*synthesis keep*/ to avoid optimization
    """
    def __init__(self,moduleName):
        self.moduleName = moduleName
        self.parameters = {} 
        self.ports = {}
        self.sequential = []
        self.logics = {}
        self.combinational = {}
        self.generate = {}

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
    returns a tuple of type and index in combinational dict /*synthesis keep*/ 
    l - lh WIRE ONLY (str)
    r - rh wire/reg (str)
    lw - left bit [_:0] (int)
    lwd - right bit [7:_] (int)
    rw - left bit [_:0] (int)
    rwd - right bit [7:_] (int)
    """
    def assign(self,l,r,lw=0,lwd=0,rw=0,rwd=0): #default to 1 bit wire, can specify width manually
        if l != r:
            temp = "ASSIGN" + str(len(self.combinational) + 1) #get new dict key
            self.combinational[temp] = (l,r,lw,lwd,rw,rwd)
        else:
            print("LHS cannot be the same as RHS!")
            return ("error")
        return ("ASSIGN",temp)

    """
    notGate: creates a NOT gate with /*synthesis keep*/ 
    returns type of gate + i/o
    a - input port (str)
    b - output port (str)
    """
    def notGate(self,a,b):
        temp = "NOT{n}".format(n=str(len(self.combinational) + 1))
        self.combinational[temp] = (a,b)
        return("NOT",a,b)

    """
    nandGate: creates a NAND gate with /*synthesis keep*/ 
    returns type of gate + i/o
    o - output port (str)
    a - input port 1 (str)
    b - input port 2 (str)
    """
    def nandGate(self,o,a,b):
        temp = "NAND{n}".format(n=str(len(self.combinational) + 1))
        self.combinational[temp] = (o,a,b)
        return("NAND",o,a,b)

    """
    norGate: creates a NOR gate with /*synthesis keep*/ 
    returns type of gate + i/o
    o - output port (str)
    a - input port 1 (str)
    b - input port 2 (str)
    """
    def norGate(self,o,a,b):
        temp = "NOR{n}".format(n=str(len(self.combinational) + 1))
        self.combinational[temp] = (o,a,b)
        return("NOR",o,a,b)

    """
    not don
    generateLoop: Generate for loop with given command
    n - number of times loop should execute (int)
    genvar - name of generate variable
    cmd - command to execute in loop (tuple)

    example:
        module = verilogModule(test)
        generateLoop(2,i,module.assign(x[i],1,1,i,1,1))
    becomes:
        genvar i;        
        generate        
        for (i = 0; i < 2 ; i++) {        
          assign x[i] = i;}        
        endgenerate 
    """
    def generateLoop(n,genvar,cmd):
        if n > 0:
            temp = len(self.generate) + 1 #get new dict key
            self.generate[temp] = (n,genvar,cmd)   
        else: #need to loop at least once
            print("Invalid loop length!")
            return ("error")
        return ("GENLOOP",n,cmd)

    """
    genvar: creates a genvar, which is exclusively used in generate for loops
    returns tuple of name/type, ("error") if could not create
    p - name of genvar (str)
    """
    def genvar(self,p):
        if p not in self.logics:
            self.logics[p] = "g"
        else: #cannot redefine logic that already exists
            print("{} already exists!".format(p))
            return ("error")
        return ("GENVAR",p)