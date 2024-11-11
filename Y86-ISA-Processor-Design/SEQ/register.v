module register(input clk,input reset,input [3:0] registernumber1_read,input [3:0] registernumber2_read,input [3:0] registernumber1_write,input [3:0] registernumber2_write,
input [63:0] val_write1,input [63:0] val_write2,
input wrEn,input reEn,output reg [63:0] val_read1,output reg [63:0] val_read2,output reg regerr);
  reg [63:0] registers [14:0];
  wire temp1;
  wire temp2;
  and(temp1, wrEn, reEn);
  or(temp2, wrEn, reEn);
  integer i;
  initial begin
    for(i=0;i<15;i=i+1) begin
      registers[i]=0;
    end
    registers[4]=1024;//Bottom most address.Initially no elememt.When first elemts is added it will be added to 1023 and so on.addresses from 970 to 1023 is reserved for stack
  end
  always @(*) begin
  val_read1 = registers[registernumber1_read];
  val_read2 = registers[registernumber2_read];
  if(wrEn) begin
     if(registernumber1_write!=15) begin
        registers[registernumber1_write] = val_write1;
        end
        if(registernumber2_write!=15) begin
        registers[registernumber2_write] = val_write2;
        end
  end
  end
  // initial
  //   begin
  //       $monitor("rax = %d ,rcx = %d, rdx = %d, rbx = %d, rsp = %d, rbp = %d, rsi = %d, rdi = %d, r8 = %d, r9 = %d, r10 = %d, r11 = %d, r12 = %d, r13 = %d, r14 = %d",registers[0],registers[1],registers[2],registers[3],registers[4],registers[5],registers[6],registers[7],registers[8],registers[9],registers[10],registers[11],registers[12],registers[13],registers[14]);
  //   end
  
endmodule
