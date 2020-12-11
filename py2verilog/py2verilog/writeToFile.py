from verilogModule import verilogModule

"""
writeToFile - class for creating/writing the generated SystemVerilog to a .sv file
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
    def writeSubModule(self,module):
        #write module name
        file = open(self.fileName , "a") #open file to append
        file.write("module {name}\n".format(name=module.moduleName))

        #writing parameters
        temp = []
        if module.parameters.items(): #if there is stuff to write, check so we don't write the closing brackets with nothing
            for key,val in module.parameters.items(): #convert dict to list 
                temp.append("{k} = {v}".format(k=key,v=val))
            file.write("\t#({params})\n\n".format(params=",\n".join(temp))) #convert list to string and write

        #writing ports
        temp.clear()
        for key,val in module.ports.items(): #convert dict to list 
            if val == "i":
                temp.append("input logic {}".format(key))
            else: #we check earlier that these have to be "i" or "o" so we can just else here
                temp.append("output logic {}".format(key))
        file.write("\t({ports});\n\n".format(ports=",\n\t".join(temp))) #convert list to string and write

        #writing logic decl.
        temp.clear()
        if module.logics.items(): #if there is stuff to write, check so we don't write the closing brackets with nothing
            for key,val in module.logics.items(): #convert dict to list 
                temp.append("logic {}".format(key))
            file.write("\t{logics};\n\n".format(logics=";\n\t".join(temp))) #convert list to string and write

        #writing comb. logic
        temp.clear()
        if module.combinational.items(): #if there is stuff to write, check so we don't write the closing brackets with nothing
            for key,val in module.combinational.items(): #convert dict to list 
                if key[0:6] == "ASSIGN": #check what kind of statement it is
                    temp.append("assign {l} = {r}".format(l=val[0],r=val[1])) #need to actually look at the bit width if we wanna have wider wires but for RO its fine right now
            file.write("\t{comb};\n\n".format(comb=";\n\t".join(temp))) #convert list to string and write

        #writing generate loops
        temp.clear()
        if module.generate.items(): #if there is stuff to write, check so we don't write the closing brackets with nothing
            file.write("\tgenvar {name};".format(name=val[1]))
            for key,val in module.generate.items(): #convert dict to list 
                continue #waddabaddabingboombam 

        #end
        file.write("endmodule\n\n")
        file.close()

    """
    writeTopModule: writes generated modules into a top_module for synthesis
    modules - generate class, contains lists of module names/ports
    """
    def writeTopModule(self,modules):
        file = open(self.fileName , "a") #open file to append
        file.write("module top_module\n") #write module name

        #topmodule inputs
        temp = []
        for port in modules.inputs: #extract ports from list
            for i in port:
                if i != "pwr" and "input logic {p}".format(p=i) not in temp: #verbose way to check if the port already was written
                    temp.append("input logic {}".format(i))
        file.write("\t({ports},\n".format(ports=",\n\t".join(temp))) #convert list to string and write

        #topmodule outputs
        temp.clear()
        for port in modules.outputs: #extract ports from list
            for i in port:
                if "output logic {p}".format(p=i) not in temp: #verbose way to check if the port already was written
                    temp.append("output logic {}".format(i))
        file.write("\t{ports});\n\n".format(ports=",\n\t".join(temp))) #convert list to string and write
        
        #instantiate modules 
        for i in range(len(modules.modules)):
            file.write("\t{name} inst_{num} (".format(name=modules.modules[i],num=i))
            #not really necessary since the RO just has enable/outClk which is 1 in/1 out but this is for multiple in/outs if wanted 
            temp.clear()
            for j in modules.inputs[i]: #connecting input ports of module
                if j == "pwr":
                    temp.append(".{in_p}(1'b1)".format(in_p=j))
                else:
                    temp.append(".{in_p}({in_p})".format(in_p=j))
            file.write("{inputs},".format(inputs=",".join(temp))) 
            temp.clear()
            for j in modules.outputs[i]: #connecting output ports of module
                temp.append(".{out_p}({out_p})".format(out_p=j))
            file.write("{outputs});\n".format(outputs=",".join(temp)))

        #end
        file.write("\nendmodule\n\n")
        file.close()
