`include "registerwrite.v"
`include "register.v"
`include "decode.v"


module registerwritedecode_tb;
  reg [7:0] opcode, rArB;
  reg [63:0] valA, valE, valP;
  wire regerr;
  reg [63:0] valM;
  reg [63:0] datamemory;
  reg clk;
  wire reset;
  wire [3:0] registernumber1;
  wire [3:0] registernumber2;
  wire [3:0] registernumber1_write;
  wire [3:0] registernumber2_write;
   wire [3:0] registernumber1_read;
  wire [3:0] registernumber2_read;
  wire [63:0] val_write1, val_write2;
  reg wrEn;
  reg reEn;
  wire [63:0] val_read1, val_read2;
  reg [3:0] op_read,op_write;
  wire [63:0] valC;



  registerwrite DUT1 (
    .opcode(opcode),
    .rArB(rArB),
    .valE(valE),
    .valM(valM),
    .reset(reset),
    .registernumber1(registernumber1_write),
    .registernumber2(registernumber2_write),
    .val_write1(val_write1),
    .val_write2(val_write2)
  );

  register DUT2 (
    .reset(reset),
    .registernumber1_read(registernumber1_read),
    .registernumber2_read(registernumber2_read),
    .registernumber1_write(registernumber1_write),
    .registernumber2_write(registernumber2_write),
    .val_write1(val_write1),
    .val_write2(val_write2),
    .wrEn(wrEn),
    .reEn(reEn),
    .val_read1(val_read1),
    .val_read2(val_read2),
    .regerr(regerr)
  );

  decode DUT3 (
    .opcode(opcode),
    .rArB(rArB),
    .valC(valC),
    .error(error),
    .registernumber1(registernumber1_read),
    .registernumber2(registernumber2_read)
  );

  initial begin
    opcode = 8'b10100000;
    rArB = 8'b10000110;
    wrEn=1;
    reEn=0;
    valA = 64'd80;
    valE = 64'd100;
    valP = 64'd80;
    #5;
    $display("%d %d %d %d %d %d %d %d", registernumber1_write, registernumber2_write, val_write1, val_write2, regerr,registernumber1_read,registernumber2_read,val_write1,val_write2);
    #15;
    opcode = 8'b10110100;
    reEn=1;
    wrEn=0;
    rArB = 8'b01100000;
    valA = 64'd20;
    valM = 64'd120;
    valP = 64'd90;
    #15;
    $display("%d %d %d %d %d %d %d %d ", registernumber1_write, registernumber2_write, val_write1, val_write2, regerr, registernumber1_read , registernumber2_read,val_write1,val_write2 );
    #40;
    $finish;
  end
endmodule
