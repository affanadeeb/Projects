`include "decode.v"
`include "register.v"
module decode_tb;
  reg [7:0] opcode,rArB;
  reg [63:0] valA,valE,valC;
  wire error;//error for invalid write in future in register write
  reg [63:0] valM;
  reg [63:0] datamemory;
  reg clk;
  wire reset;
  wire [3:0] registernumber1;
  wire [3:0] registernumber2;
  wire [63:0] val_write1,val_write2;
  wire wrEn;
  reg reEn;
  wire finalerror;
  wire regerr;
 wire [63:0] val_read1,val_read2;
 initial begin
    reEn=1;
 end
 wire [3:0] temp1,temp2;
  assign finalerror = error | regerr;
 //val_read1 =valA,val_read2=valB
  decode DUT1(.opcode(opcode),.rArB(rArB),.valC(valC),.error(error),.registernumber1(registernumber1),.registernumber2(registernumber2));
  register DUT2(.reset(reset),.registernumber1_read(registernumber1),.registernumber2_read(registernumber2),.registernumber1_write(temp1),
  .registernumber2_write(temp2),.val_write1(val_write1),.val_write2(val_write2),.wrEn(wrEn),.reEn(reEn),.val_read1(val_read1),.val_read2(val_read2),.regerr(regerr));
  initial begin
    opcode=8'b00100000;
    rArB=8'b11110000;
    valC=64'd80;
    #5; $display("%d %d %d %d %d",registernumber1,registernumber2,val_read1,val_read2,finalerror);
    #15 opcode=8'b00100100;
    rArB=8'b01001111;
    valC=64'd20;
    #5 $display("%d %d %d %d %d",registernumber1,registernumber2,val_read1,val_read2,finalerror);
    #15 opcode=8'b01100000;
    rArB=8'b01001111;
    valC=64'd20;
    #5 $display("%d %d %d %d %d",registernumber1,registernumber2,val_read1,val_read2,finalerror);
    #15 opcode=8'b01100011;
    rArB=8'b01001111;
    valC=64'd20;
    #5 $display("%d %d %d %d %d",registernumber1,registernumber2,val_read1,val_read2,finalerror);
    #15 opcode=8'b00100000;
    rArB=8'b01001111;
    valC=64'd20;
    #5 $display("%d %d %d %d %d",registernumber1,registernumber2,val_read1,val_read2,finalerror);
    #15 opcode=8'b10000000;
    rArB=8'b01001111;
    valC=64'd20;
    #5 $display("%d %d %d %d %d",registernumber1,registernumber2,val_read1,val_read2,finalerror);
    #20 $finish;
end
endmodule