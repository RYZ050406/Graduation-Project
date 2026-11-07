`timescale 1ns/1ps
module safety_gate_tb;
  reg clk = 0;
  reg reset = 0;
  reg request = 0;
  reg authorized = 0;
  reg kill_req = 0;
  wire allow, stopped;
  safety_gate dut(.*);
  always #5 clk = ~clk;
  task tick(input reg r, input reg q, input reg a, input reg k,
            input reg expected_stopped, input reg expected_allow);
    begin
      @(negedge clk);
      reset = r; request = q; authorized = a; kill_req = k;
      @(posedge clk); #1;
      if (stopped !== expected_stopped || allow !== expected_allow)
        $fatal(1, "gate mismatch");
    end
  endtask
  initial begin
    tick(1, 0, 0, 0, 0, 0);
    tick(0, 1, 0, 0, 0, 0);
    tick(0, 1, 1, 0, 0, 1);
    tick(0, 1, 1, 1, 1, 0);
    tick(0, 1, 1, 0, 1, 0);
    tick(0, 0, 1, 0, 1, 0);
    tick(1, 1, 1, 1, 0, 1);
    tick(0, 1, 1, 1, 1, 0);
    $display("PASS safety_gate: policy/latch/reset priority");
    $finish;
  end
endmodule
