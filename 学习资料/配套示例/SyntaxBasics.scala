import chisel3._
import chisel3.util._
import _root_.circt.stage.ChiselStage

class SyntaxBasics extends Module {
  val io = IO(new Bundle {
    val enable = Input(Bool())
    val a = Input(UInt(8.W))
    val b = Input(UInt(8.W))
    val op = Input(UInt(2.W))
    val y = Output(UInt(8.W))
    val sumFull = Output(UInt(9.W))
    val count = Output(UInt(4.W))
  })
  val y = WireDefault(0.U(8.W))
  switch(io.op) {
    is(0.U) { y := io.a + io.b }
    is(1.U) { y := io.a & io.b }
    is(2.U) { y := Cat(io.a(3, 0), io.b(3, 0)) }
  }
  io.y := y
  io.sumFull := io.a +& io.b
  val count = RegInit(0.U(4.W))
  when(io.enable) { count := count + 1.U }
  io.count := count
}

object EmitSyntaxBasics extends App {
  println(ChiselStage.emitSystemVerilog(
    new SyntaxBasics,
    firtoolOpts = Array("-disable-all-randomization")
  ))
}
