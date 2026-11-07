module safety_gate(
  input wire clk, reset,
  input wire request, authorized, kill_req,
  output wire allow,
  output reg stopped
);
  always @(posedge clk) begin
    if (reset) stopped <= 1'b0;
    else if (kill_req) stopped <= 1'b1;
  end
  assign allow = request && authorized && !stopped;
endmodule
