`timescale 1ns/1ps
module mux2_tb;
  reg a, b, sel;
  wire y;
  integer i;
  mux2 dut(.a(a), .b(b), .sel(sel), .y(y));
  initial begin
    for (i = 0; i < 8; i = i + 1) begin
      {sel, b, a} = i;
      #1;
      if (y !== (sel ? b : a)) $fatal(1, "mux mismatch");
    end
    $display("PASS mux2: 8 combinations");
    $finish;
  end
endmodule
