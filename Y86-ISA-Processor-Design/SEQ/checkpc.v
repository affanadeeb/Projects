module checkpc(input [63:0] pc,output reg error);
  always@(*) begin
  if(pc>1023) begin
    error=1;
  end
  else begin
    error=0; //checks if pc value is a valid address for instruction or not
  end
  end
endmodule