// Connect the generated Chisel ports to the same interface used by the RTL test.
// Compile this adapter INSTEAD OF safety_gate.sv.
module safety_gate(
  input wire clk, reset,
  input wire request, authorized, kill_req,
  output wire allow, stopped
);
  SafetyGate generated(
    .clock(clk), .reset(reset), .io_request(request),
    .io_authorized(authorized), .io_killReq(kill_req),
    .io_allow(allow), .io_stopped(stopped)
  );
endmodule
