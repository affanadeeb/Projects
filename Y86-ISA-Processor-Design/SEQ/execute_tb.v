`include "execute.v"
`include "ALU.v"
`include "ADD_64.v"
`include "SUB_64.v"
`include "AND_64.v"
`include "XOR_64.v"
`include "fulladder.v"


module execute_tb;
  reg [7:0] opcode,rArB;
  reg [63:0] valC,valA,valB;
  reg clk;
  reg [2:0] cc;// have to be added in sequential processor-condition flags
  wire [63:0] valE;
  wire [7:0] rArB_execute;
  wire Cnd;
  wire [2:0] cc_out;
  execute DUT1(.opcode(opcode), .rArB(rArB), .valA(valA), .valB(valB), .valC(valC),.cc(cc),.valE(valE),.rArB_execute(rArB_execute),.Cnd(Cnd),.cc_out(cc_out));
  always begin
    #10 clk=~clk;
  end
  always @(*) begin
    cc=cc_out;
  end
  initial begin
    cc<=3'b0;
    clk<=0;
  end
  initial begin
    opcode=8'b01100000;
    rArB=8'b10000000;
    valA=64'd7;
    valB=64'd68;
    valC=64'd100;
    #5 $display("%d %d %d %d",valE,rArB_execute,Cnd,cc);
    #15 opcode=8'b00100000;
    rArB=8'b10000000;
    valA=64'd7;
    valB=64'd68;
    valC=64'd100;
    #5 $display("%d %d %d %d",valE,rArB_execute,Cnd,cc);
    #15 opcode=8'b01100001;
    rArB=8'b10000000;
    valA=79;
    valB=98;
    valC=201;
    #5$display("%d %d %d %d",valE,rArB_execute,Cnd,cc);
    #15 opcode=8'b10100000;
    rArB=8'b10000000;
    valA=200;
    valB=78;
    valC=200;
    #5$display("%d %d %d %d",valE,rArB_execute,Cnd,cc);
    #15 opcode=8'b10110000;
    rArB=8'b10000001;
    valA=99;
    valB=80;
    valC=110;
    #5$display("%d %d %d %d",valE,rArB_execute,Cnd,cc);
    #20 $finish;
end
endmodule