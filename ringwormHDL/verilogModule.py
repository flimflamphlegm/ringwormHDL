"""
verilogModule - class for generating SystemVerilog modules
"""
class verilogModule:
    """
    __init__: takes string "name" and instantiates a Verilog/SystemVerilog module with that name
    *dicts are ordered in python 3.6+, use OrderedDict if older version*
    self.parameters - a dict of all the module parameters
    self.ports - a dict of all the module ports, where 0 = input and 1 = output
    self.sequential - a list of llists of all sequential logic, where the 0th element in each list of lists is the first command executed in the sequential (always) block
    self.logic - a dict of all logic defines (wire/regs), where the order is based on input order
    self.combinational - a dict of all combinational logic, where all are syntehsized with the tag /*synthesis keep*/ to avoid optimization
    self.generate - a dict of all generate loops, which can contail sequential or combinational logic (this might need changing, also WIP)
    """
    def __init__(self,moduleName):
        self.moduleName = moduleName
        self.parameters = {} 
        self.ports = {}
        self.sequential = []
        self.logics = {}
        self.combinational = {}
        #self.generate = {} WIP

    """
    parameter: takes parameter name, value, and adds them to the module
    returns dict key, "error" if could not add
    p - name of parameter (str)
    i - value of parameter (int)
    """
    def parameter(self,p,i):
        if p not in self.parameters:
            self.parameters[p] = i;
        else: #can't update the value of a parameter as it has to be a constant
            print("Parameter {} already exists!".format(p))
            return "error"
        return p

    """
    ports: takes port name, direction, and adds them to the module
    returns dict key, "error" if could not add
    p - name of port (str)
    dir - direction of port, use "i" to designate input, and "o" to designate output (str)
    w - width of port (int)
    """
    def port(self,p,dir,w=1):
        if p not in self.ports:
            if dir == "i" or dir == "o": #make sure it's a valid direction
                self.ports[p] = (dir,w)
        else: #cannot redefine port that already exists
            print("Port {} already exists!".format(p))
            return "error"
        return p

    """
    logic: use to create a logic (wire/reg) "w" bits wide
    returns dict key, "error" if could not add
    p - name (str)
    w - width (int)
    synthParam - synthesis parameter (str)
    """
    def logic(self,p,w=1,synthParam=""):
        if p not in self.logics:
            if w > 0: #can't have a 0 width wire/reg
                self.logics[p] = (p,w,synthParam)
            else:
                print("Can't have a 0 width wire/reg")
                return "error"
        else: #cannot redefine logic that already exists
            print("Logic {} already exists!".format(p))
            return "error"
        return p

    """
    assign: takes lhs and rhs values, along with their bit widths, and creates an assign statement
    returns dict key /*synthesis keep*/, or "error" if not valid
    l - lh WIRE ONLY (str)
    r - rh wire/reg (str)
    lw - left bit [_:0] (int)
    lwd - right bit [7:_] (int)
    rw - left bit [_:0] (int)
    rwd - right bit [7:_] (int)
    synthParam - synthesis parameter (str)
    """
    def assign(self,l,r,lw=0,lwd=0,rw=0,rwd=0,synthParam=""): #default to 1 bit wire, can specify width manually
        if l != r:
            temp = "ASSIGN" + str(len(self.combinational) + 1) #get new dict key
            self.combinational[temp] = (l,r,lw,lwd,rw,rwd,synthParam) #store params in dict for generation later
        else:
            print("LHS cannot be the same as RHS!")
            return "error"
        return temp

    """
    notGate: creates a NOT gate with /*synthesis keep*/ 
    returns dict key
    a - input port (str)
    b - output port (str)
    synthParam - synthesis parameter (str)
    """
    def notGate(self,a,b,synthParam=""):
        temp = "NOT{n}".format(n=str(len(self.combinational) + 1)) #get new dict key
        self.combinational[temp] = (a,b,synthParam) #store params in dict for generation later
        return temp

    """
    andGate: creates an AND gate with /*synthesis keep*/ 
    returns dict key
    o - output port (str)
    a - input port 1 (str)
    b - input port 2 (str)
    synthParam - synthesis parameter (str)
    """
    def andGate(self,o,a,b,synthParam=""):
        temp = "AND{n}".format(n=str(len(self.combinational) + 1)) #get new dict key
        self.combinational[temp] = (o,a,b,synthParam) #store params in dict for generation later
        return temp

    """
    nandGate: creates a NAND gate with /*synthesis keep*/ 
    returns dict key
    o - output port (str)
    a - input port 1 (str)
    b - input port 2 (str)
    synthParam - synthesis parameter (str)
    """
    def nandGate(self,o,a,b,synthParam=""):
        temp = "NAND{n}".format(n=str(len(self.combinational) + 1)) #get new dict key
        self.combinational[temp] = (o,a,b,synthParam) #store params in dict for generation later
        return temp

    """
    norGate: creates a NOR gate with /*synthesis keep*/ 
    returns dict key
    o - output port (str)
    a - input port 1 (str)
    b - input port 2 (str)
    synthParam - synthesis parameter (str)
    """
    def norGate(self,o,a,b,synthParam=""):
        temp = "NOR{n}".format(n=str(len(self.combinational) + 1)) #get new dict key
        self.combinational[temp] = (o,a,b,synthParam) #store params in dict for generation later
        return temp

    """
    alwaysSequential: creates a sequential always block with input edge conditions
    returns index in sequential list that all commands for this always block should be input in
    signals: name of signals and "p/n" for posedge/negedge, leave empty for * wild card (comma seperated string)
    """
    def alwaysSequential(self,signals=""):
        self.sequential.append(signals)
        return len(self.sequential) - 1

    """
    nbAssign: creates non blocking assignment statement for use in sequential always blocks
    returns index of command in list of list
    i - index of sequential always block (int)
    l - lhs (str)
    r - rhs (str)
    """
    def nbAssign(self,i,l,r): #default to 1 bit wire, can specify width manually
        if l != r:
            self.sequential[i].append(("NB",l,r)) #store params in dict for generation later
        else:
            print("LHS cannot be the same as RHS!")
            return "error"
        return len(self.sequential) - 1

    """
    ifStatement: generates an if statement for use in a sequential always block
    returns index of command in list of list
    i - index of sequential always block (int)
    _cond - condition for if statement (str)
    _cmd - command to execute if condition is true (str)
    """
    def ifStatement(self,i,cond,cmd):
        if i > len(self.sequential) - 1:
            print ("Invalid index!")
            return "error"
        else:
            self.sequential[i].append(("IF",cond,cmd)) #store the condition and command
        return len(self.sequential[i]) - 1

    """
    elseStatement: generates an if statement for use in a sequential always block
    returns index of command in list of list
    i - index of sequential always block (int)
    _cmd - command to execute (str)
    """
    def elseStatement(self,i,cmd):
        if i > len(self.sequential) - 1:
            print ("Invalid index!")
            return "error"
        else:
            self.sequential[i].append("ELSE",cmd) #store the condition and command
        return len(self.sequential[i]) - 1

    """
    WIP
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
    
    def generateLoop(n,genvar,cmd):
        if n > 0:
            temp = len(self.generate) + 1 #get new dict key
            self.generate[temp] = (n,genvar,cmd)   
        else: #need to loop at least once
            print("Invalid loop length!")
            return "error"
        return temp    
   
    genvar: creates a genvar, which is exclusively used in generate for loops
    returns tuple of name/type, ("error") if could not create
    p - name of genvar (str)

    def genvar(self,p):
        if p not in self.logics:
            self.logics[p] = "g"
        else: #cannot redefine logic that already exists
            print("{} already exists!".format(p))
            return "error"
        return "some placeholder"   
        
    """
    

    