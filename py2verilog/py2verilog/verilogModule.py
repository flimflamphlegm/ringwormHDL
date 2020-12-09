"""
verilogModule - class for generating SystemVerilog modules
"""
class verilogModule:
    """
    sequential logic 
    """
    def ifStatement(self,condition,execute):
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
    l - lh WIRE ONLY (str)
    lw - left bit [_:0] (int)
    lwd - right bit [7:_] (int)
    l - rh wire/reg (str)
    rw - left bit [_:0] (int)
    rwd - right bit [7:_] (int)
    """
    def assign(self,l,lw,lwd,r,rw,rwd):
        if lw != lwd and rw != rwd: #can't have a 0 width wire
            temp = "ASSIGN" + str(len(self.combinational) + 1) #get new dict key
            self.combinational[temp] = (l,lw,lwd,r,rw,rwd)
        else:
            print("Can't have a 0 width wire!")
            return ("error")
        return ("ASSIGN",temp)
