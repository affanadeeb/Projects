module PC(input reset,input wrEn,input reEn,input [63:0] val_write,output [63:0] val_read)
   reg [63:0] PC;
   if(reset) begin
    PC<=0;
   end
   else begin
    if(reEn) begin
       val_read<=PC;   
    end
    if(wrEn) begin
       PC<=val_write;
    end
   end
endmodule