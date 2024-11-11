`include "fetch.v"
`include "checkpc.v"
`include "decode.v"
`include "register.v"
`include "execute.v"
`include "ALU.v"
`include "ADD_64.v"
`include "SUB_64.v"
`include "AND_64.v"
`include "XOR_64.v"
`include "fulladder.v"
`include "memorywrite.v"
`include "dataMem.v"
`include "registerwrite.v"
`include "PCupdate.v"
`include "sequentialprocessor.v"
`include "statusupdate.v"


module sequentialprocessor_tb;
  wire [7:0] opcode, rArB;
  wire [63:0] valA, valB,valC,valE, valM;
  wire [1:0] status;
  wire [2:0] cc;
  wire [63:0] pc;
  reg clk;
    initial begin
    clk=0;
    reboot=1;
  end

always begin
    #10 clk=~clk;
end
reg reboot;
initial begin
      $dumpfile("sequentialprcoessor_tb.vcd");
      $dumpvars(0,sequentialprocessor_tb);
end


sequentialprocessor DUT(.clk(clk),.reboot(reboot),.opcode(opcode),.rArB(rArB),.valA(valA),.valB(valB),.valC(valC),.valE(valE),
.valM(valM),.pc1(pc),.cc1(cc),.status1(status));//reboot is initially one when processor is off and becomes 0 after.Instructions are executed in posedge and update of
//pc,cc,registerwrite,memorywrite,status happens in negedge

initial begin
   #11  reboot=0;
end
always @(*) begin
  if(status!=0) begin
    #1
    $finish;
      end
end
initial begin
  
//    #11 $display("%d %d %d %d %d %d %d  ", opcode,rArB,valA, valB,valC,valE,valM); 
//    #10 $display("%d %d %d",pc,cc,status);
//    #10 $display("%d %d %d %d %d %d %d  ", opcode,rArB,valA, valB,valC,valE,valM);
//    #10 $display("%d %d %d",pc,cc,status);
//    #10 $display("%d %d %d %d %d %d %d  ", opcode,rArB,valA, valB,valC,valE,valM);
//    #10 $display("%d %d %d",pc,cc,status);
//    #10 $display("%d %d %d %d %d %d %d  ", opcode,rArB,valA, valB,valC,valE,valM);//remove files condition.v,status.v,instrctionmem.v
//    #10 $display("%d %d %d",pc,cc,status);
//    #10 $display("%d %d %d %d %d %d %d  ", opcode,rArB,valA, valB,valC,valE,valM);
//    #10 $display("%d %d %d",pc,cc,status);
//    #10 $display("%d %d %d %d %d %d %d  ", opcode,rArB,valA, valB,valC,valE,valM);
//    #10 $display("%d %d %d",pc,cc,status);
//    #10 $display("%d %d %d %d %d %d %d  ", opcode,rArB,valA, valB,valC,valE,valM);
//    #10 $display("%d %d %d",pc,cc,status);
//    #10 $display("%d %d %d %d %d %d %d  ", opcode,rArB,valA, valB,valC,valE,valM);
//    #10 $display("%d %d %d",pc,cc,status);
//    #10 $display("%d %d %d %d %d %d %d  ", opcode,rArB,valA, valB,valC,valE,valM);
//    #10 $display("%d %d %d",pc,cc,status);
//     #10 $display("%d %d %d %d %d %d %d  ", opcode,rArB,valA, valB,valC,valE,valM);
//    #10 $display("%d %d %d",pc,cc,status);
//    #10 $display("%d %d %d %d %d %d %d  ", opcode,rArB,valA, valB,valC,valE,valM);
//    #10 $display("%d %d %d",pc,cc,status);
//    #10 $display("%d %d %d %d %d %d %d  ", opcode,rArB,valA, valB,valC,valE,valM);
//    #10 $display("%d %d %d",pc,cc,status);
//    #10 $display("%d %d %d %d %d %d %d  ", opcode,rArB,valA, valB,valC,valE,valM);
//    #10 $display("%d %d %d",pc,cc,status);
//    #10 $display("%d %d %d %d %d %d %d  ", opcode,rArB,valA, valB,valC,valE,valM);
//    #10 $display("%d %d %d",pc,cc,status);
//     #10 $display("%d %d %d %d %d %d %d  ", opcode,rArB,valA, valB,valC,valE,valM);
//    #10 $display("%d %d %d",pc,cc,status);
//    #10 $display("%d %d %d %d %d %d %d  ", opcode,rArB,valA, valB,valC,valE,valM);
//    #10 $display("%d %d %d",pc,cc,status);
//    #10 $display("%d %d %d %d %d %d %d  ", opcode,rArB,valA, valB,valC,valE,valM);
//    #10 $display("%d %d %d",pc,cc,status);
//    #10 $display("%d %d %d %d %d %d %d  ", opcode,rArB,valA, valB,valC,valE,valM);
//    #10 $display("%d %d %d",pc,cc,status);
//     #10 $display("%d %d %d %d %d %d %d  ", opcode,rArB,valA, valB,valC,valE,valM);
//    #10 $display("%d %d %d",pc,cc,status);

//  #10 $display("%d %d %d %d %d %d %d  ", opcode,rArB,valA, valB,valC,valE,valM);
//    #10 $display("%d %d %d",pc,cc,status);

//  #10 $display("%d %d %d %d %d %d %d  ", opcode,rArB,valA, valB,valC,valE,valM);
//    #10 $display("%d %d %d",pc,cc,status);
//    #10 $display("%d %d %d %d %d %d %d  ", opcode,rArB,valA, valB,valC,valE,valM);
//    #10 $display("%d %d %d",pc,cc,status);
//    #10 $display("%d %d %d %d %d %d %d  ", opcode,rArB,valA, valB,valC,valE,valM);
//    #10 $display("%d %d %d",pc,cc,status);
//    #10 $display("%d %d %d %d %d %d %d  ", opcode,rArB,valA, valB,valC,valE,valM);
//    #10 $display("%d %d %d",pc,cc,status);
//    #10 $display("%d %d %d %d %d %d %d  ", opcode,rArB,valA, valB,valC,valE,valM);
//    #10 $display("%d %d %d",pc,cc,status);
//    #10 $display("%d %d %d %d %d %d %d  ", opcode,rArB,valA, valB,valC,valE,valM);
//    #10 $display("%d %d %d",pc,cc,status);
//    #10 $display("%d %d %d %d %d %d %d  ", opcode,rArB,valA, valB,valC,valE,valM);
//    #10 $display("%d %d %d",pc,cc,status);

//    #10 $display("%d %d %d %d %d %d %d  ", opcode,rArB,valA, valB,valC,valE,valM);
//    #10 $display("%d %d %d",pc,cc,status);
//    #10 $display("%d %d %d %d %d %d %d  ", opcode,rArB,valA, valB,valC,valE,valM);
//    #10 $display("%d %d %d",pc,cc,status);
//    #10 $display("%d %d %d %d %d %d %d  ", opcode,rArB,valA, valB,valC,valE,valM);
//    #10 $display("%d %d %d",pc,cc,status);
//    #10 $display("%d %d %d %d %d %d %d  ", opcode,rArB,valA, valB,valC,valE,valM);
//    #10 $display("%d %d %d",pc,cc,status);
//    #10 $display("%d %d %d %d %d %d %d  ", opcode,rArB,valA, valB,valC,valE,valM);
//    #10 $display("%d %d %d",pc,cc,status);
//    #10 $display("%d %d %d %d %d %d %d  ", opcode,rArB,valA, valB,valC,valE,valM);
//    #10 $display("%d %d %d",pc,cc,status);
//    #10 $display("%d %d %d %d %d %d %d  ", opcode,rArB,valA, valB,valC,valE,valM);
//    #10 $display("%d %d %d",pc,cc,status);
 


 
   

     
     
   
// $finish;
end
   




 

endmodule
