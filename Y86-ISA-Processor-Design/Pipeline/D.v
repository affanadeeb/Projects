module D(input clk,input [1:0] f_stat,input [7:0] f_opcode,input [7:0] f_rArB,input [63:0] f_valP,input [63:0] f_valC,input F_stall,
output reg [1:0] D_stat,output reg [7:0] D_opcode,output reg [7:0] D_rArB,output reg [63:0] D_valC,output reg [63:0] D_valP);
   reg count;
   initial begin 
      count=1;
   end
   always @(posedge clk) begin
    if(count==0) begin
    D_opcode=f_opcode;
    D_rArB=f_rArB;
    D_valP=f_valP;
    D_valC=f_valC;
    D_stat=f_stat;
    end
    else begin
      count=count-1;
    end
   end
endmodule