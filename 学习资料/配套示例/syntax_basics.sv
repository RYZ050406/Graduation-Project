// A small circuit used by the Verilog and Chisel syntax supplements.
module syntax_basics(
  input wire clk, reset, enable,
  input wire [7:0] a, b,
  input wire [1:0] op,
  output reg [7:0] y,
  output wire [8:0] sum_full,
  output reg [3:0] count
);
  assign sum_full = {1'b0, a} + {1'b0, b};
  always @(*) begin
    y = 8'd0;
    case (op)
      2'd0: y = a + b;
      2'd1: y = a & b;
      2'd2: y = {a[3:0], b[3:0]};
      default: y = 8'd0;
    endcase
  end
  always @(posedge clk) begin
    if (reset) count <= 4'd0;
    else if (enable) count <= count + 4'd1;
  end
endmodule
