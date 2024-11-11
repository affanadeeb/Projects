module F(input clk,input [63:0] f_predPC,output reg [63:0] F_predPC);
   reg count;
   initial begin
      count=1;
   end
   always @(posedge clk) begin
    if(count==0) begin
      F_predPC=f_predPC;
    end
    else begin
      F_predPC=0;
      count=count-1;
    end
   
   end
endmodule