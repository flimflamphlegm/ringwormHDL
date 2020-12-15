from writeToFile import writeToFile
from generate import generate

if __name__ == "__main__":
    newFile = writeToFile("ro.sv") #creates new file with name "ro.sv"
    """
    #on chip memory test
    genModules = generate(); #store all names of generated modules
    genModules.onChipMem("d","wren","clk","write_addr","read_addr","q",newFile)
    newFile.writeTopModule(genModules) #connect all generated modules inside a top_module
    """
    #ring osc prompts
    while True: #ask user for number of ring oscillators 
        try:
            c = int(input("Please enter the number of ring oscillators:"))
        except ValueError or c <= 0:
            continue
        else:
            break
    
    genModules = generate(); #store all names of generated modules

    for i in range(int(c)): #for each ring oscillator, ask user for specifications
        print("\nRO #{num}:".format(num=str(i + 1)))

        in_port = input("Please enter the name of the enable input port ('pwr' for internal power connection):")
        out_port = input("Please enter the name of the RO output port:")

        while True: #ask user for valid gate selection (0 <= type <= 2)
            try:
                type = int(input("Please enter what kind of gate to use for the RO (0 = NOT, 1 = NAND, 2 = NOR):"))
            except ValueError or type <= -1 or type >= 3:
                continue
            else:
                break

        while True: #wait for valid stage size (odd number >= 3)
            try:
                n = int(input("Please enter the number of stages (an odd number greater or equal to 3):"))
            except ValueError or n % 2 == 0 or n <= 2:
                continue
            else:
                break

        if type == 0: #generate appropriate RO based on user choice from above, and write to file
            genModules.RO_not(n,in_port,out_port,newFile)
        elif type == 1:
            genModules.RO_nand(n,in_port,out_port,newFile)
        else:
            genModules.RO_nor(n,in_port,out_port,newFile)

    newFile.writeTopModule(genModules) #connect all generated modules inside a top_module
