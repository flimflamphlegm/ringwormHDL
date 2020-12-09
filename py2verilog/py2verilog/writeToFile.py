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
    def writeModule(self,module):
        #write module name
        file = open(self.fileName , "a") #open file to append
        file.write("module " + module.moduleName + "\n")

        #writing parameters
        temp = []
        if module.parameters.items(): #if there is stuff to write
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
        file.write("\t" + ";\n\t".join(temp) + ";\n") #convert list to string and write

        #writing comb. logic
        temp.clear()
        for key,val in module.combinational.items(): #convert dict to list 
            if key[0:6] == "ASSIGN": #check what kind of statement it is
                temp.append("assign {l} = {r}".format(l=val[0],r=val[3]))
        file.write("\t" + ";\n\t".join(temp) + ";\n") #convert list to string and write

        #end
        file.write("endmodule\n\n")
        file.close()
