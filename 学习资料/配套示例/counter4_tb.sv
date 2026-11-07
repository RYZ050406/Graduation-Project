`timescale 1ns/1ps
module counter4_tb;
  reg clk = 0;
  reg reset = 0;
  reg enable = 0;
  wire [3:0] count;
  integer i;
  counter4 dut(.clk(clk), .reset(reset), .enable(enable), .count(count));
  always #5 clk = ~clk;
  task tick(input reg r, input reg e, input reg [3:0] expected);
    begin
      @(negedge clk); reset = r; enable = e;
      @(posedge clk); #1;
      if (count !== expected) $fatal(1, "counter mismatch");
      $display("reset=%b enable=%b count=%0d", r, e, count);
    end
  endtask
  initial begin
    $dumpfile("counter4.vcd");
    $dumpvars(0, counter4_tb);
    tick(1, 1, 0);
    tick(0, 1, 1);
    tick(0, 0, 1);
    tick(0, 1, 2);
    for (i = 3; i <= 15; i = i + 1) tick(0, 1, i);
    tick(0, 1, 0);
    tick(1, 0, 0);
    $display("PASS counter4: reset/hold/increment/wrap");
    $finish;
  end
endmodule
