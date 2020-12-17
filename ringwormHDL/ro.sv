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

