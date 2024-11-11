module pipelinedprocessor(input clk,output [7:0] D_opcode,output [7:0] D_rArB,output [63:0] D_valC,output [63:0] D_valP,output [1:0] D_stat,
output [7:0] E_opcode,output [63:0] E_valA,output [63:0] E_valB,output [63:0] E_valC,output [3:0] E_dstE,output [3:0] E_dstM,output [3:0] E_srcA,output [3:0] E_srcB,
output [1:0] E_stat,
output [3:0] M_icode,output M_Cnd,output [63:0] M_valA,output [63:0] M_valE,output [3:0] M_dstE,output [3:0] M_dstM,output [1:0] M_stat,
output [3:0] W_icode,output [63:0] W_valM,output [63:0] W_valE,output [3:0] W_dstE,output [3:0] W_dstM,output [1:0] W_stat,
output e_Cnd,output [3:0] e_dstE,output [63:0] e_valE,output [3:0] d_srcA,output [3:0] d_srcB);



  wire [63:0] f_predPC,F_predPC,m_valM,d_valC,d_valA,d_valB,e_valA,d_valP,f_valP,f_valC,m_valE;
  wire [1:0] d_stat,e_stat,f_stat,m_stat;
  wire [7:0] d_opcode,d_rArB,f_opcode,f_rArB;
  wire [3:0] d_dstE,d_dstM,e_dstM,m_dstM,m_dstE,m_icode,e_icode;

  wire [3:0] D_icode;
  assign D_icode=D_opcode[7:4];
  wire [3:0] E_icode;
  assign E_icode=E_opcode[7:4];


  F inst_F(clk,f_predPC,F_predPC);

 fetch inst_fetch(clk,M_icode,M_Cnd,M_valA,W_icode,W_valM,F_predPC,F_stall,
D_stall,D_valP,D_opcode,D_rArB,D_valC,D_stat,D_bubble,
f_valP,f_opcode,f_rArB,f_valC,f_stat,f_predPC);

 D inst_D(clk,f_stat,f_opcode,f_rArB,f_valP,f_valC,F_stall,
D_stat,D_opcode,D_rArB,D_valC,D_valP);

 decode inst_decode (
  D_opcode,D_rArB,D_valC,D_valP,D_stat,E_bubble,
  e_dstE,e_valE,M_dstE,M_valE,M_dstM,m_valM,W_dstM,W_valM,
  W_dstE,W_valE,
  d_stat,d_opcode,d_valC,d_valA,d_valB,d_dstE,d_dstM,d_srcA,
  d_srcB
); 

 E inst_E(clk,d_stat,d_opcode,d_valA,d_valB,d_valC,d_dstE,d_dstM,
d_srcA,d_srcB,
E_stat,E_opcode,E_valA,E_valB,E_valC,E_dstE,
E_dstM,E_srcA,E_srcB);

 execute inst_execute(E_stat,E_opcode,E_valA,E_valB,E_valC,E_dstE,E_dstM,
E_srcA,E_srcB,
e_stat,e_icode,e_valE,e_valA,e_dstM,e_Cnd,e_dstE);

 M inst_M(clk,e_stat,e_icode,e_Cnd,e_valE,e_valA,e_dstE,e_dstM,
M_stat,M_icode, M_Cnd,M_valE,M_valA,M_dstE,
M_dstM);

 memorywrite inst_memorywrite(M_stat,M_icode,M_Cnd,M_dstE,M_dstM,M_valA,M_valE,
m_stat,m_icode,m_valE,m_valM,m_dstE,m_dstM);

 W inst_W(clk,m_stat,m_icode,m_valE,m_valM,m_dstE,m_dstM,
W_stat,W_icode,W_valE,W_valM,W_dstE,
W_dstM);

 Pipelinecontrllogic inst_controllogic(E_icode,D_icode,M_icode,E_dstM,d_srcA,d_srcB,e_Cnd,
F_stall,D_stall,D_bubble,E_bubble);

endmodule