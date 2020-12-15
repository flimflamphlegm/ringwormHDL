# ringwormHDL
if you like it you should've put a ring oscillator on it

![ring oscillator with enable](https://github.com/flimflamphlegm/ringwormHDL/blob/main/ro.png)

## Functions
- Create ring oscillators with user-specified input/output ports, so that they can be connected to I/O or power internally
- Can chain ring oscillators/have them in parallel with user-specified number of stages
- Generate on-chip memory block (M10K) for testing

## How to use
There is a basic script setup to prompt the user to input the desired RO parameters, but different outputs can be manually configured:

1. Create a new file

`newFile = writeToFile("ro.sv");`
	
2. Create a generate class to store all the submodules

`genModules = generate();`
	
3. Create submodule(s)

`genModules.RO_not(n,in_port,out_port,newFile)`
	
4. Create the top module to link everything

`newFile.writeTopModule(genModules)`	
