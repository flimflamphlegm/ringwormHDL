module RO_3
	#(n = 8)
	(input logic en,
	output logic outClk1);
	logic a0,
	logic r0,
	logic r1,
	logic r2
	assign a0 = en & r2;
	assign r0 = !a1;
	assign r1 = !r0;
	assign r2 = !r1;
	assign outClk = r2
endmodule

module RO_5
	#(n = 8)
	(input logic en,
	output logic outClk2);
	logic a0,
	logic r0,
	logic r1,
	logic r2,
	logic r3,
	logic r4
	assign a0 = en & r4;
	assign r0 = !a1;
	assign r1 = !r0;
	assign r2 = !r1;
	assign r3 = !r2;
	assign r4 = !r3;
	assign outClk = r4
endmodule

