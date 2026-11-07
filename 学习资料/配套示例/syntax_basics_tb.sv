`timescale 1ns/1ps
module syntax_basics_tb;
  reg clk = 0;
  reg reset = 0;
  reg enable = 0;
  reg [7:0] a = 0, b = 0;
  reg [1:0] op = 0;
  wire [7:0] y;
  wire [8:0] sum_full;
  wire [3:0] count;
  integer i, j, k;
  reg [7:0] expected_y;
  syntax_basics dut(.*);
  always #5 clk = ~clk;

  task tick(input reg r, input reg e, input reg [3:0] expected);
    begin
      @(negedge clk); reset = r; enable = e;
      @(posedge clk); #1;
      if (count !== expected) $fatal(1, "count mismatch");
    end
  endtask

  initial begin
    $dumpfile("syntax_basics.vcd");
    $dumpvars(0, syntax_basics_tb);
    tick(1, 1, 0);
    tick(0, 1, 1);
    tick(0, 0, 1);
    for (i = 2; i <= 15; i = i + 1) tick(0, 1, i);
    tick(0, 1, 0);
    tick(1, 0, 0);
    a = 8'hF0; b = 8'h3C; op = 0; #1;
    if (y !== 8'd44 || sum_full !== 9'd300) $fatal(1, "width mismatch");
    op = 1; #1;
    if (y !== 8'h30) $fatal(1, "AND mismatch");
    op = 2; #1;
    if (y !== 8'h0C) $fatal(1, "concatenation mismatch");
    op = 3; #1;
    if (y !== 8'd0) $fatal(1, "default mismatch");
    // Keep the wave short; then sweep all input pairs without recording them.
    $dumpoff;
    for (i = 0; i < 256; i = i + 1) begin
      for (j = 0; j < 256; j = j + 1) begin
        for (k = 0; k < 4; k = k + 1) begin
          a = i; b = j; op = k; #1;
          case (k)
            0: expected_y = i + j;
            1: expected_y = i & j;
            2: expected_y = ((i & 15) << 4) | (j & 15);
            default: expected_y = 0;
          endcase
          if (y !== expected_y || sum_full !== (i + j))
            $fatal(1, "combinational mismatch a=%0d b=%0d op=%0d", i, j, k);
        end
      end
    end
    $display("PASS syntax_basics: 262144 combinations plus counter checks");
    $finish;
  end
endmodule
