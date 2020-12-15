from writeToFile import writeToFile
from generate import generate

"""
    #on chip memory test
    genModules = generate(); #store all names of generated modules
    genModules.onChipMem("d","wren","clk","write_addr","read_addr","q",newFile)
    newFile.writeTopModule(genModules) #connect all generated modules inside a top_module
"""

if __name__ == "__main__":
    """
    ring osc prompt
    """

    #creates new file with name "ro.sv"
    newFile = writeToFile("ro.sv") 
    
    #store all names of generated modules
    genModules = generate(); 
    
    #ask user for number of ring oscillators 
    while True: 
        try:
            c = int(input("Please enter the number of ring oscillators:"))
        except ValueError or c <= 0:
            continue
        else:
            break
            
    #for each ring oscillator, ask user for specifications
    for i in range(int(c)): 
        print("\nRO #{num}:".format(num=str(i + 1)))

        in_port = input("Please enter the name of the enable input port ('pwr' for internal power connection):")
        out_port = input("Please enter the name of the RO output port:")

        #ask user for valid gate selection (0 <= type <= 2)
        while True: 
            try:
                type = int(input("Please enter what kind of gate to use for the RO (0 = NOT, 1 = NAND, 2 = NOR):"))
            except ValueError or type <= -1 or type >= 3:
                continue
            else:
                break

        #ask user for valid stage size (odd number >= 3)
        while True: 
            try:
                n = int(input("Please enter the number of stages (an odd number greater or equal to 3):"))
            except ValueError or n % 2 == 0 or n <= 2:
                continue
            else:
                break

        #generate appropriate RO based on user choice from above, and write to file
        if type == 0: 
            genModules.RO_not(n,in_port,out_port,newFile)
        elif type == 1:
            genModules.RO_nand(n,in_port,out_port,newFile)
        else:
            genModules.RO_nor(n,in_port,out_port,newFile)

    #connect all generated modules inside a top_module
    newFile.writeTopModule(genModules) 
