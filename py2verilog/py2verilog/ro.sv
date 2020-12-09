module RO_not_3
	(input logic en1,
	output logic outClk1);
	logic a0;
	logic r0;
	logic r1;
	logic r2;
	assign a0 = en1 & r2;
	assign r0 = !a0;
	assign r1 = !r0;
	assign r2 = !r1;
	assign outClk1 = r2;
endmodule

module RO_nand_5
	(input logic en2,
	output logic outClk2);
	logic a0;
	logic r0;
	logic r1;
	logic r2;
	logic r3;
	logic r4;
	assign a0 = en2 & r4;
	assign r0 = !(a0 & a0);
	assign r1 = !(r0 & r0);
	assign r2 = !(r1 & r1);
	assign r3 = !(r2 & r2);
	assign r4 = !(r3 & r3);
	assign outClk2 = r4;
endmodule

module RO_nor_7
	(input logic en3,
	output logic outClk3);
	logic a0;
	logic r0;
	logic r1;
	logic r2;
	logic r3;
	logic r4;
	logic r5;
	logic r6;
	assign a0 = en3 & r6;
	assign r0 = !(a0 | a0);
	assign r1 = !(r0 | r0);
	assign r2 = !(r1 | r1);
	assign r3 = !(r2 | r2);
	assign r4 = !(r3 | r3);
	assign r5 = !(r4 | r4);
	assign r6 = !(r5 | r5);
	assign outClk3 = r6;
endmodule

