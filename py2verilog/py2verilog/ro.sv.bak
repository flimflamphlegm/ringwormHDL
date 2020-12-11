module RO_nand_3_0
	(input logic pwr,
	output logic outClk1);

	logic a0;
	logic r0;
	logic r1;
	logic r2;

	assign a0 = !(pwr & r2);
	assign r0 = !(a0 & a0);
	assign r1 = !(r0 & r0);
	assign outClk1 = r1;

endmodule

module RO_nor_3_1
	(input logic en,
	output logic outClk2);

	logic a0;
	logic r0;
	logic r1;
	logic r2;

	assign a0 = !(en & r2);
	assign r0 = !(a0 | a0);
	assign r1 = !(r0 | r0);
	assign outClk2 = r1;

endmodule

module top_module
	(input logic en,
	output logic outClk1,
	output logic outClk2);

	RO_nand_3_0 inst_0 (.pwr(1'b1),.outClk1(outClk1));
	RO_nor_3_1 inst_1 (.en(en),.outClk2(outClk2));

endmodule

