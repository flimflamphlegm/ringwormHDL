from verilogModule import verilogModule

class writeToFile:
    """
    writeToFile - class for creating/writing the generated SystemVerilog to a .sv file
    """
    
    def __init__(self, fileName:str) -> None:
        """
        initialization: creates new file with specified file name
        fileName: name of SystemVerilog file (str)
        """
        self.fileName = fileName
        file = open(fileName,"w")                                           #overwrites existing copy of file, start from blank file
        file.close()
    
    def writeSubModule(self, module:verilogModule) -> None:
        """
        writeSubModule: writes the module to the file, takes file name from writeToFile instance
        generation format:
        module <name> 
            #(<parameters>)
            (<ports>);
            <logic decl.>;
            <combinational logic>;
            <sequential logic>;
        endmodule
        module - verilogModule object
        """
        #write module name
        file = open(self.fileName , "a")                                    #open file to append
        file.write("module {name}\n".format(name=module.moduleName))

        #writing parameters
        temp = []                                                           #keep list of all parameters to go in #() parentheses
        if module.parameters.items():                                       #if there is stuff to write, check so we don't write the closing brackets with nothing
            for key,val in module.parameters.items():                       #convert dict to list 
                temp.append("{k} = {v}".format(k=key,v=val))
            file.write("\t#({params})\n\n".format(params=",\n".join(temp))) #convert list to string and write into parentheses

        #writing ports
        temp.clear()                                                        #keep list of all ports to go in (); parentheses
        for key,val in module.ports.items():                                #convert dict to list 
            if val[0] == "i":
                if val[1] == 1:                                             #if the port is 1 bit wide no need to specify [x:y]
                    temp.append("input logic {}".format(key))
                else:                                                       #specify how wide the port is if it's wider than 1 bit
                    temp.append("input logic [{n}:0] {k}".format(n=val[1]-1,k=key))
            else:                                                           #we check earlier that these have to be "i" or "o" so we can just else here
                if val[1] == 1:
                    temp.append("output logic {}".format(key))
                else:
                    temp.append("output logic [{n}:0] {k}".format(n=val[1]-1,k=key))
        file.write("\t({ports});\n\n".format(ports=",\n\t".join(temp)))     #convert list to string and write

        #writing logic decl.
        temp.clear()                                                        #keep list of all logic statements to write
        if module.logics.items():                                           #if there is stuff to write, check so we don't write the closing brackets with nothing
            for key,val in module.logics.items():                           #convert dict to list 
                tempStr = ""
                if val[1] == 1:                                             #if 1 bit wide no need to specify width
                    tempStr += ("logic {}".format(key))
                else:                                                       #else specify how wide it is
                    tempStr += ("logic [{n}:0] {k}".format(n=val[1]-1,k=key))
                if val[2]:                                                  #if the synthesis parameter exists, put it in
                    tempStr += " /*{synth}*/".format(synth=val[2])
                temp.append(tempStr)    
            file.write("\t{logics};\n\n".format(logics=";\n\t".join(temp))) #convert list to string and write

        #writing comb. logic
        temp.clear()
        if module.combinational.items():                                    #if there is stuff to write, check so we don't write the ending ; for nothing
            for key,val in module.combinational.items():                    #convert dict to list 
                tempStr = ""
                if key[0:3] == "NOT":                                       #check what kind of statement it is
                    tempStr += ("not({a},{b})".format(a=val[0],b=val[1]))
                elif key[0:3] == "NOR":
                    tempStr += ("nor({o},{a},{b})".format(o=val[0],a=val[1],b=val[2]))
                elif key[0:3] == "AND":
                    tempStr += ("and({o},{a},{b})".format(o=val[0],a=val[1],b=val[2]))
                elif key[0:4] == "NAND":
                    tempStr += ("nand({o},{a},{b})".format(o=val[0],a=val[1],b=val[2]))
                elif key[0:6] == "ASSIGN": 
                    tempStr += ("assign {l} = {r}".format(l=val[0],r=val[1]))
                if val[-1]:                                                 #get synthesis parameter if it exists
                    tempStr += " /*{synth}*/".format(synth=val[-1])
                temp.append(tempStr)
            file.write("\t{comb};\n\n".format(comb=";\n\t".join(temp)))     #convert list to string and write

        #writing sequential logic
        temp.clear()
        tempStr = ""
        if module.sequential:
            for i in module.sequential:                                     #for each always block
                tempStr += "always @("                                      #first index is the dict with always block conditions
                if i[0] == {}:                                              #if empty, wild card in sensitivity list
                    tempStr += "*" 
                else:                                                       #else get the signals to trigger on
                    temp2 = []
                    for key,val in i[0].items():
                        if val == "p":                                      #p for posedge signal
                            temp2.append("posedge {k}".format(k=key))
                        else:                                               #n for negedge signal
                            temp2.append("negedge {k}".format(k=key))
                    tempStr += " or ".join(temp2)                           #it assumes all signals are ored together right now, maybe put in an option to choose and/or later
                tempStr += ") begin"
                temp.append(tempStr)
                for j in range(1,len(i)):                                   #look at the sequential commands of this always block in order
                    tempStr = "\t"
                    if i[j][0] == "IF":                                     #check what statement it is
                        tempStr += ("if ({cond}) begin {cmd}; end".format(cond=i[j][1],cmd=i[j][2]))
                    elif i[j][0] == "ELSE":
                        tempStr += ("else begin {cmd}; end".format(cmd=i[j][1]))
                    elif i[j][0] == "NB":
                        tempStr += ("{lhs} <= {rhs};".format(lhs=i[j][1],rhs=i[j][2]))
                    temp.append(tempStr)
                temp.append("end")
                file.write("\t{cmd}\n\n".format(cmd="\n\t".join(temp)))     #convert list to string and write

        """
        #writing generate loops - maybe do this if we want like 69 stages then the file doesn't have to be 138 lines long
        temp.clear()
        if module.generate.items(): #if there is stuff to write, check so we don't write the closing brackets with nothing
            file.write("\tgenvar {name};".format(name=val[1]))
            for key,val in module.generate.items(): #convert dict to list 
                continue #waddabaddabingboombam 
        """

        #end
        file.write("endmodule\n\n")
        file.close()

    def writeTopModule(self, modules:verilogModule) -> None:
        """
        writeTopModule: writes generated modules into a top_module for synthesis
        generation format:
        module <name> 
            (<ports>);
            <module instantiations>;
        endmodule
        modules - generate object, from which we take the lists of module names/ports
        """
        file = open(self.fileName , "a")                                    #open file to append
        file.write("module top_module\n")                                   #write module name

        #topmodule inputs
        temp = []
        for port in modules.inputs:                                         #extract ports from list
            for i in port:
                if i != "pwr" and "input logic {p}".format(p=i) not in temp:#verbose way to check if the port already was written
                    temp.append("input logic {}".format(i))
        file.write("\t({ports},\n".format(ports=",\n\t".join(temp)))        #convert list to string and write

        #topmodule outputs
        temp.clear()
        for port in modules.outputs: #extract ports from list
            for i in port:
                if "output logic {p}".format(p=i) not in temp:              #verbose way to check if the port already was written
                    temp.append("output logic {}".format(i))
        file.write("\t{ports});\n\n".format(ports=",\n\t".join(temp)))      #convert list to string and write
        
        #instantiate modules 
        for i in range(len(modules.modules)):
            file.write("\t{name} inst_{num} (".format(name=modules.modules[i],num=i))
            temp.clear()
            for j in modules.inputs[i]:                                     #connecting input ports of module
                if j == "pwr":                                              #if 'pwr' connect enable to power internally
                    temp.append(".{in_p}(1'b1)".format(in_p=j))     
                else:                                                       #else connect enable to input port
                    temp.append(".{in_p}({in_p})".format(in_p=j))
            file.write("{inputs},".format(inputs=",".join(temp))) 
            temp.clear()
            for j in modules.outputs[i]:                                    #connecting output ports of module
                temp.append(".{out_p}({out_p})".format(out_p=j))
            file.write("{outputs});\n".format(outputs=",".join(temp)))

        #end
        file.write("\nendmodule\n\n")
        file.close()
