`include "registerwrite.v"
`include "register.v"
module registerwrite_tb;
  reg [7:0] opcode,rArB;
  reg [63:0] valA,valE,valP;
  wire regerr;
  reg [63:0] valM;
  reg [63:0] datamemory;
  reg clk;
  wire reset;
  wire [3:0] registernumber1;
  wire [3:0] registernumber2;
  wire [63:0] val_write1,val_write2;
  reg wrEn;
  reg reEn;
 wire [63:0] val_read1,val_read2;
 initial begin
    reEn=0;
 end
 wire [3:0] temp1,temp2;

  registerwrite DUT1(.opcode(opcode),.rArB(rArB),.valE(valE),.valM(valM),.reset(reset),.registernumber1(registernumber1),.registernumber2(registernumber2),.val_write1(val_write1),.val_write2(val_write2));
 register DUT2(.reset(reset),.registernumber1_read(temp1),.registernumber2_read(temp2),.registernumber1_write(registernumber1),
  .registernumber2_write(registernumber2),.val_write1(val_write1),.val_write2(val_write2),.wrEn(wrEn),.reEn(reEn),.val_read1(val_read1),.val_read2(val_read2),.regerr(regerr));
  initial begin
    reEn=0;
    wrEn=1;
    opcode=8'b10100000;
    rArB=8'b00110000;
    valA=64'd80;
    valE=64'd1023;
    valP=64'd80;
    #5; $display("%d %d %d %d %d",registernumber2,val_write1,val_write2,regerr);
    #15 opcode=8'b01010100;
    wrEn=1;
    rArB=8'b01000000;
    valA=64'd20;
    valM=64'd120;
    valP=64'd90;
    #15 $display("%d %d %d %d %d",registernumber1,registernumber2,val_write1,val_write2,regerr);
    #40 $finish;
end
endmodule