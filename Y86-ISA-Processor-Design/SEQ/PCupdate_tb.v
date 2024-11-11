`include "PCupdate.v"
module PCupdate_tb;
  reg [7:0] opcode;
  reg [63:0] valP,valM,valC;
  wire [63:0] finalval_PC;
  reg clk;
  reg Cnd;
  PCupdate DUT(.opcode(opcode),.valP(valP),.valM(valM),.valC(valC),.Cnd(Cnd),.finalval_PC(finalval_PC));
  always begin
    #10 clk=~clk;
  end
  integer i;
  initial begin
    clk<=0;
  end
  initial begin
    opcode=8'b01110100;
    valP=10000;
    valM=64'd20;
    valC=64'd90;
    Cnd=0;
    #5; $display("%d",finalval_PC);
    #15  opcode=8'b01110100;
    valP=100010;
    valM=64'd20;
    valC=64'd90;
    Cnd=1;
    #5 $display("%d",finalval_PC);
    #15  opcode=8'b00100000;
    valP=890;
    valM=64'd30;
    valC=64'd91;
    Cnd=0;
    #5 $display("%d",finalval_PC);
     #15  opcode=8'b10010000;
    valP=910;
    valM=64'd25;
    valC=64'd95;
    Cnd=1;
    #5 $display("%d",finalval_PC);
     #15  opcode=8'b01110100;
    valP=2000;
    valM=30;
    valC=100;
    Cnd=0;
    #5 $display("%d",finalval_PC);
    #20 $finish;
end
endmodule