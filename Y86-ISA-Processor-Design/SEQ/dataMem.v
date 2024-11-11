module dataMem(input clk,input reset,input [63:0] addr,input [63:0] val_write,input wrEn,input reEn,output reg [63:0] val_read,output reg memerror);
  wire temp1;
  wire temp2;
  and(temp1, wrEn, reEn);
  or(temp2, wrEn, reEn);
  integer i;
  reg memerror1,memerror2;
  reg [7:0] datamemory[1023:0];
  reg [9:0] addr_temp;
  initial begin
    for(i=0;i<1024;i=i+1)begin
      datamemory[i]=0; 
    end
    datamemory[200]=100;
    datamemory[208]=60; //initialising values for testbench
    datamemory[216]=80;
    datamemory[224]=50;
  end

   wire err;
   always @(negedge clk) begin
    addr_temp=addr[9:0];
    if(addr>1016) begin
      memerror=1;
    end
   
   else  if(wrEn) begin
      datamemory[addr_temp+7]=val_write[63:56];datamemory[addr_temp+6]=val_write[55:48];datamemory[addr_temp+5]=val_write[47:40];
      datamemory[addr_temp+4]=val_write[39:32];datamemory[addr_temp+3]=val_write[31:24];datamemory[addr_temp+2]=val_write[23:16];
      datamemory[addr_temp+1]=val_write[15:8];datamemory[addr_temp]=val_write[7:0]; //writes into memory based on inputs from memory write on negative edge of clock
      memerror=1'b0;
     end
    end
    always @(*) begin
  if(reset)begin
  for (i=0;i<1024;i=i+1) begin //reset data
    datamemory[i]=0;
  end
  memerror<=1'b0;
  val_read<=64'hFFFFFFFFFFFFFFFF;
  end
  
  else begin
    addr_temp=addr[9:0];
  if ((addr > 1016) || (temp1 == 1'b1)) begin //checks for invalid address and case when both read and write are enabled
    memerror1 <= 1'b1;
    memerror2<=1'b0;
  end
  else if (temp2 == 1'b0) begin //both read and write disabled
    memerror1 <= 1'b0;
    memerror2 <= 1'b0;
  end
  else begin
    memerror1 = 1'b0;
    
      val_read[63:56]=datamemory[addr_temp+7]; 
      val_read[55:48]=datamemory[addr_temp+6]; 
      val_read[47:40]=datamemory[addr_temp+5]; 
      val_read[39:32]=datamemory[addr_temp+4];
        val_read[31:24]=datamemory[addr_temp+3]; 
        val_read[23:16]=datamemory[addr_temp+2]; 
        val_read[15:8]=datamemory[addr_temp+1]; 
        val_read[7:0]=datamemory[addr_temp]; //reads value based on address provided by memory write
      memerror2=0;
  
  end
  memerror=memerror1|memerror2; 
end
  end
endmodule
