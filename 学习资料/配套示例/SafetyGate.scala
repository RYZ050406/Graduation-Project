import chisel3._
import circt.stage.ChiselStage

class SafetyGate extends Module {
  val io = IO(new Bundle {
    val request = Input(Bool())
    val authorized = Input(Bool())
    val killReq = Input(Bool())
    val allow = Output(Bool())
    val stopped = Output(Bool())
  })
  val stopped = RegInit(false.B)
  when(io.killReq) {
    stopped := true.B
  }
  io.stopped := stopped
  io.allow := io.request && io.authorized && !stopped
}

object EmitSafetyGate extends App {
  println(ChiselStage.emitSystemVerilog(
    new SafetyGate,
    firtoolOpts = Array("-disable-all-randomization")
  ))
}
