// Compile INSTEAD OF syntax_basics.sv when checking generated Chisel RTL.
module syntax_basics(
  input wire clk, reset, enable,
  input wire [7:0] a, b,
  input wire [1:0] op,
  output wire [7:0] y,
  output wire [8:0] sum_full,
  output wire [3:0] count
);
  SyntaxBasics generated(
    .clock(clk), .reset(reset), .io_enable(enable),
    .io_a(a), .io_b(b), .io_op(op), .io_y(y),
    .io_sumFull(sum_full), .io_count(count)
  );
endmodule
