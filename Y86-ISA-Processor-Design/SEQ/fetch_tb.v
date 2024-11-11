`include "fetch.v"
`include "checkpc.v"

module fetch_tb;
  reg [63:0] pc;
  wire [63:0] valP;
  wire [7:0] opcode;
  wire [7:0] rArB;
  wire [63:0] valC;
  wire [1:0] status;
  reg reset,reEn,wrEn;
  reg clk;
  fetch dut1_inst(.clk(clk),.pc(pc), .valP(valP), .opcode(opcode), .rArB(rArB), .valC(valC),.status(status));
   
 always begin
  #20 pc=valP;
 end
  always begin
    #10 clk=~clk;
  end
  initial begin
    clk=0;
    pc=0;
    #11$display("%d %d %d %d %d",opcode,rArB,valC,valP,status); pc=valP;
    #20$display("%d %d %d %d %d",opcode,rArB,valC,valP,status);pc=valP;
    #20$display("%d %d %d %d %d",opcode,rArB,valC,valP,status);pc=valP; 
    #20$display("%d %d %d %d %d",opcode,rArB,valC,valP,status); pc=valP;
    #20$display("%d %d %d %d %d",opcode,rArB,valC,valP,status); pc=valP;
    #20$display("%d %d %d %d %d",opcode,rArB,valC,valP,status); pc=valP;
    #20$display("%d %d %d %d %d",opcode,rArB,valC,valP,status); pc=valP;
    #20$display("%d %d %d %d %d",opcode,rArB,valC,valP,status);pc=valP;
    #20$display("%d %d %d %d %d",opcode,rArB,valC,valP,status);pc=valP;
    #20$display("%d %d %d %d %d",opcode,rArB,valC,valP,status);pc=valP;
    #20$display("%d %d %d %d %d",opcode,rArB,valC,valP,status);pc=valP;
    #20$display("%d %d %d %d %d",opcode,rArB,valC,valP,status);pc=valP;
    #20$display("%d %d %d %d %d",opcode,rArB,valC,valP,status);pc=valP;
    #20$display("%d %d %d %d %d",opcode,rArB,valC,valP,status);pc=valP;
    #20$display("%d %d %d %d %d",opcode,rArB,valC,valP,status);pc=valP;
     



    #400 $finish;
end
endmodule