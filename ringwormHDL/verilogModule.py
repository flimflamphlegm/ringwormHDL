class verilogModule:
    """
    verilogModule - class for generating SystemVerilog modules
    """
    
    def __init__(self, moduleName:str) -> None:
        """
        __init__: takes string "name" and instantiates a Verilog/SystemVerilog module with that name
        *dicts are ordered in python 3.6+, use OrderedDict if older version*
        self.parameters - a dict of all the module parameters
        self.ports - a dict of all the module ports, where 0 = input and 1 = output
        self.sequential - a list of llists of all sequential logic, where the 0th element in each list of lists is the first command executed in the sequential (always) block
        self.logic - a dict of all logic defines (wire/regs), where the order is based on input order
        self.combinational - a dict of all combinational logic, where can be synthesized with parameters like /*synthesis keep*/ to avoid optimization
        self.generate - a dict of all generate loops, which can contail sequential or combinational logic (this might need changing, also WIP)
        """
        self.moduleName = moduleName
        self.parameters = {} 
        self.ports = {}
        self.sequential = []
        self.logics = {}
        self.combinational = {}
        #self.generate = {} WIP

    def parameter(self, newParam:str, i:int) -> str:
        """
        parameter: takes parameter name, value, and adds them to the module
        returns dict key, "error" if could not add
        newParam - name of parameter (str)
        i - value of parameter (int)
        """
        if newParam not in self.parameters:
            self.parameters[newParam] = i;
        else: 
            print("Parameter {} already exists!".format(newParam))      #can't update the value of a parameter as it has to be a constant
            return "error"
        return newParam

    def port(self, newPort:str, dir:str, w:int=1) -> str:
        """
        ports: takes port name, direction, and adds them to the module
        returns dict key, "error" if could not add
        p - name of port (str)
        dir - direction of port, use "i" to designate input, and "o" to designate output (str)
        w - width of port (int)
        """
        if newPort not in self.ports:
            if dir == "i" or dir == "o":                                #make sure it's a valid direction
                self.ports[newPort] = (dir,w)
        else: 
            print("Port {} already exists!".format(newPort))            #cannot redefine port that already exists
            return "error"
        return newPort

    
    def logic(self, newLogic:str, width:int=1, synthParam:str="") -> str:
        """
        logic: use to create a logic (wire/reg) "w" bits wide
        returns dict key, "error" if could not add
        newLogic - name (str)
        width - width (int)
        synthParam - synthesis parameter (str)
        """
        if newLogic not in self.logics:
            if width > 0:                                               
                self.logics[newLogic] = (newLogic,width,synthParam)
            else:
                print("Can't have a 0 width wire/reg")                  #can't have a 0 width logic type
                return "error"
        else: 
            print("Logic {} already exists!".format(newLogic))          #cannot redefine logic that already exists 
            return "error"
        return newLogic

    def assign(self, l:str, r:str, lw:int=0, lwd:int=0, rw:int=0, rwd:int=0, synthParam:str="") -> str:  
        """
        assign: takes lhs and rhs values, along with their bit widths, and creates an assign statement
        default to 1 bit wire, can specify width manually
        returns dict key /*synthesis keep*/, or "error" if not valid
        l - lh WIRE ONLY (str)
        r - rh wire/reg (str)
        lw - left bit [_:0] (int)
        lwd - right bit [7:_] (int)
        rw - left bit [_:0] (int)
        rwd - right bit [7:_] (int)
        synthParam - synthesis parameter (str)
        """
        if l != r:                                                      
            temp = "ASSIGN" + str(len(self.combinational) + 1)          #get new dict key
            self.combinational[temp] = (l,r,lw,lwd,rw,rwd,synthParam)   #store params in dict for generation later
        else:
            print("LHS cannot be the same as RHS!")
            return "error"
        return temp

    def notGate(self, a:str, b:str, synthParam:str="") -> str:
        """
        notGate: creates a NOT gate with synthesis parameter
        returns dict key
        a - input port (str)
        b - output port (str)
        synthParam - synthesis parameter (str)
        """
        temp = "NOT{n}".format(n=str(len(self.combinational) + 1))      #get new dict key
        self.combinational[temp] = (a,b,synthParam)                     #store params in dict for generation later
        return temp

    def andGate(self, o:str, a:str, b:str, synthParam:str="") -> str:
        """
        andGate: creates an AND gate with synthesis parameter
        returns dict key
        o - output port (str)
        a - input port 1 (str)
        b - input port 2 (str)
        synthParam - synthesis parameter (str)
        """
        temp = "AND{n}".format(n=str(len(self.combinational) + 1))      #get new dict key
        self.combinational[temp] = (o,a,b,synthParam)                   #store params in dict for generation later
        return temp

    def nandGate(self, o:str, a:str, b:str, synthParam:str="") -> str:
        """
        nandGate: creates a NAND gate with synthesis parameter
        returns dict key
        o - output port (str)
        a - input port 1 (str)
        b - input port 2 (str)
        synthParam - synthesis parameter (str)
        """
        temp = "NAND{n}".format(n=str(len(self.combinational) + 1))     #get new dict key
        self.combinational[temp] = (o,a,b,synthParam)                   #store params in dict for generation later
        return temp

    def norGate(self, o:str, a:str, b:str, synthParam:str="") -> str:
        """
        norGate: creates a NOR gate with synthesis parameter
        returns dict key
        o - output port (str)
        a - input port 1 (str)
        b - input port 2 (str)
        synthParam - synthesis parameter (str)
        """
        temp = "NOR{n}".format(n=str(len(self.combinational) + 1))      #get new dict key
        self.combinational[temp] = (o,a,b,synthParam)                   #store params in dict for generation later
        return temp

    def alwaysSequential(self, signals:dict={}) -> int:
        """
        alwaysSequential: creates a sequential always block with input edge conditions
        returns index in sequential list that all commands for this always block should be input in
        signals: name of signals and "p/n" for posedge/negedge, leave empty for * wild card (dict)
        """
        self.sequential.append(signals)                                 #store params in list for generation later          
        return len(self.sequential) - 1

    def nbAssign(self, i:int, l:str, r:str) -> int: 
        """
        nbAssign: creates non blocking assignment statement for use in sequential always blocks
        for now, default to lhs bit width == rhs bit width
        returns index of command in list of list
        i - index of sequential always block (int)
        l - lhs (str)
        r - rhs (str)
        """
        if l != r:
            self.sequential[i].append(("NB",l,r))                       #store params in dict inside list for generation later
        else:
            print("LHS cannot be the same as RHS!")
            return "error"
        return len(self.sequential) - 1

    def ifStatement(self, i:int, cond:str, cmd:str) -> int:
        """
        ifStatement: generates an if statement for use in a sequential always block
        returns index of command in list of list
        i - index of sequential always block (int)
        cond - condition for if statement (str)
        cmd - command to execute if condition is true (str)
        """
        if i > len(self.sequential) - 1:                                #list indices have to be positive 
            print ("Invalid index!")
            return "error"
        else:
            self.sequential[i].append(("IF",cond,cmd))                  #store the condition and command
        return len(self.sequential[i]) - 1

    def elseStatement(self, i:int, cmd:str) -> int:
        """
        elseStatement: generates an if statement for use in a sequential always block
        returns index of command in list of list
        i - index of sequential always block (int)
        cmd - command to execute (str)
        """
        if i > len(self.sequential) - 1:                                #list indices have to be positive 
            print ("Invalid index!")
            return "error"
        else:
            self.sequential[i].append("ELSE",cmd)                       #store the condition and command
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
    

    