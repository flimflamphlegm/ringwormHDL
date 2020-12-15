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

module RO_nand_5_1
	(input logic en,
	output logic outClk2);

	logic a0 /*synthesis keep*/;
	logic r0 /*synthesis keep*/;
	logic r1 /*synthesis keep*/;
	logic r2 /*synthesis keep*/;
	logic r3 /*synthesis keep*/;

	nand(a0,en,r3) /*synthesis keep*/;
	nand(r0,a0,a0) /*synthesis keep*/;
	nand(r1,r0,r0) /*synthesis keep*/;
	nand(r2,r1,r1) /*synthesis keep*/;
	nand(r3,r2,r2) /*synthesis keep*/;
	assign outClk2 = r3;

endmodule

module RO_nor_7_2
	(input logic en,
	output logic outClk3);

	logic a0 /*synthesis keep*/;
	logic r0 /*synthesis keep*/;
	logic r1 /*synthesis keep*/;
	logic r2 /*synthesis keep*/;
	logic r3 /*synthesis keep*/;
	logic r4 /*synthesis keep*/;
	logic r5 /*synthesis keep*/;

	nand(a0,en,r5) /*synthesis keep*/;
	nor(r0,a0,a0) /*synthesis keep*/;
	nor(r1,r0,r0) /*synthesis keep*/;
	nor(r2,r1,r1) /*synthesis keep*/;
	nor(r3,r2,r2) /*synthesis keep*/;
	nor(r4,r3,r3) /*synthesis keep*/;
	nor(r5,r4,r4) /*synthesis keep*/;
	assign outClk3 = r5;

endmodule

module top_module
	(input logic en,
	output logic outClk1,
	output logic outClk2,
	output logic outClk3);

	RO_not_3_0 inst_0 (.en(en),.outClk1(outClk1));
	RO_nand_5_1 inst_1 (.en(en),.outClk2(outClk2));
	RO_nor_7_2 inst_2 (.en(en),.outClk3(outClk3));

endmodule

