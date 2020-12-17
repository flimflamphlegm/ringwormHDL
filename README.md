
# ringwormHDL
A Python script that generates SystemVerilog files to synthesize ring oscillators
Doxygen PDF manual *("refman.pdf")*

![ring oscillator with enable](https://github.com/flimflamphlegm/ringwormHDL/blob/main/ro.png)

## Functions
- Create ring oscillators with user-specified input/output ports, so that they can be connected to I/O or power internally
- Can chain ring oscillators/have them in parallel with user-specified number of stages
- Generate on-chip memory block (M10K) for testing

## How to use
There is a basic script setup to prompt the user to input the desired RO parameters, but different outputs can be manually configured:

*Example: Creating two NOT-gate-based ring oscillators with parallel enable (named "en"), one with 3 stages (output named "outClk1"), and one with 5 stages (output named "outClk2")*

1. Create a new file, named "ro.sv"

`newFile = writeToFile("ro.sv");`
	
2. Create a generate object to store all the submodules

`genModules = generate();`
	
3. Create submodule(s)

`genModules.RO_not(3,"en","outClk1",newFile);`
`genModules.RO_not(5,"en","outClk2",newFile);`
	
4. Create the top module to link everything

`newFile.writeTopModule(genModules);`	

*This will generate the following SystemVerilog:*

	module RO_not_3_0
		(input logic en,
		output logic outClk1);

		logic a0 /*synthesis keep*/;
		logic r0 /*synthesis keep*/;
		logic r1 /*synthesis keep*/;

		nand(a0,en,r1) /*synthesis keep*/;
		not(r0,a0) /*synthesis keep*/;
		not(r1,r0) /*synthesis keep*/;
		assign outClk1 = r1;

	endmodule

	module RO_not_5_1
		(input logic en,
		output logic outClk2);

		logic a0 /*synthesis keep*/;
		logic r0 /*synthesis keep*/;
		logic r1 /*synthesis keep*/;
		logic r2 /*synthesis keep*/;
		logic r3 /*synthesis keep*/;

		nand(a0,en,r3) /*synthesis keep*/;
		not(r0,a0) /*synthesis keep*/;
		not(r1,r0) /*synthesis keep*/;
		not(r2,r1) /*synthesis keep*/;
		not(r3,r2) /*synthesis keep*/;
		assign outClk2 = r3;

	endmodule

	module top_module
		(input logic en,
		output logic outClk1,
		output logic outClk2);

		RO_not_3_0 inst_0 (.en(en),.outClk1(outClk1));
		RO_not_5_1 inst_1 (.en(en),.outClk2(outClk2));

	endmodule



