module E(input clk,input [1:0] d_stat,input [7:0] d_opcode,input [63:0] d_valA,input [63:0] d_valB,input [63:0] d_valC,input [3:0] d_dstE,input [3:0] d_dstM,
input [3:0] d_srcA,input [3:0] d_srcB,
output reg [1:0] E_stat,output reg [7:0] E_opcode,output reg [63:0] E_valA,output reg [63:0] E_valB,output reg [63:0] E_valC,output reg [3:0] E_dstE,
output reg [3:0] E_dstM,output reg [3:0] E_srcA,output reg [3:0] E_srcB);
   always @(posedge clk) begin
    E_stat=d_stat;
    E_opcode=d_opcode;
    E_valA=d_valA;
    E_valB=d_valB;
    E_valC=d_valC;
    E_dstE=d_dstE;
    E_dstM=d_dstM;
    E_srcA=d_srcA;
    E_srcB=d_srcB;
   end
endmodule