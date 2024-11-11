`include "memorywrite.v"
`include "dataMem.v"
module memorywrite_tb;
  reg [7:0] opcode,rArB;
  reg [63:0] valA,valE,valP;
  wire memerror;
  wire [63:0] valM;
  reg [63:0] datamemory;
  reg clk;
  wire reset;
  wire [63:0] addr,val_write;
  wire wrEn,reEn;
 wire [63:0] val_read;
  memorywrite DUT1(.opcode(opcode),.rArB(rArB),.valA(valA),.valE(valE),.valP(valP),.reset(reset),.addr(addr),.val_write(val_write),.wrEn(wrEn),.reEn(reEn));
  dataMem DUT2(.reset(reset),.addr(addr),.val_write(val_write),.wrEn(wrEn),.reEn(reEn),.val_read(val_read),.memerror(memerror));
  initial begin
    opcode=8'b10100000;
    rArB=8'b10001111;
    valA=64'd80;
    valE=64'd1000;
    valP=64'd80;
    #5; $display("%d %d %d %d %d %d %d",reset,addr,val_write,val_read,wrEn,reEn,val_read,memerror);
    #15 opcode=8'b10110000;
    rArB=8'b10000000;
    valA=64'd1000;
    valE=64'd1000;
    valP=64'd90;
    #30 $display("%d %d %d %d %d %d %d",reset,addr,val_write,val_read,wrEn,reEn,val_read,memerror);
    #40 $finish;
end
endmodule