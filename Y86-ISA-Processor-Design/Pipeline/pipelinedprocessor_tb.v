`include "fetch.v"
`include "decode.v"
`include "execute.v"
`include "memorywrite.v"
`include "F.v"
`include "D.v"
`include "E.v"
`include "M.v"
`include "W.v"
`include "Pipelinecontrollogic.v"
`include "ALU.v"
`include "ADD_64.v"
`include "SUB_64.v"
`include "AND_64.v"
`include "XOR_64.v"
`include "fulladder.v"
`include "pipelinedprocessor.v"


module pipelinedprocessor_tb;

  reg clk;
  wire [7:0] D_opcode,D_rArB,E_opcode;
  wire [63:0] D_valC,D_valP,E_valA,E_valB,E_valC,M_valA,M_valE,W_valM,W_valE,e_valE;
  wire [1:0] D_stat,E_stat,W_stat,M_stat;
  wire [3:0] E_dstE,E_dstM,E_srcA,E_srcB,M_icode,M_dstE,M_dstM,W_icode,W_dstE,W_dstM,e_dstE,d_srcA,d_srcB;
  wire M_Cnd,e_Cnd;

    initial begin
    clk=0;
  end

always begin
    #10 clk=~clk;
end
reg reboot;
initial begin
      $dumpfile("pipelinedprocessor_tb.vcd");
      $dumpvars(0,pipelinedprocessor_tb);
end


pipelinedprocessor DUT(clk,D_opcode,D_rArB, D_valC,D_valP,D_stat,
E_opcode,E_valA,E_valB,E_valC,E_dstE,E_dstM,E_srcA,E_srcB,
E_stat,M_icode,M_Cnd,M_valA,M_valE,M_dstE,M_dstM,M_stat,
W_icode,W_valM,W_valE,W_dstE,W_dstM, W_stat,e_Cnd,e_dstE,e_valE,d_srcA,d_srcB);


always @(*) begin
  if((W_stat!=0)) begin
    #1
    $finish;
      end
end




 

endmodule
