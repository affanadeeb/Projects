`include "fulladder.v"
module fulladder_tb;
  reg A,B,C_in;
  wire S,C;
  fulladder DUT(A,B,C_in,S,C);
  
  integer i;
  
  initial begin
    $dumpfile("fulladder_tb.vcd");
    $dumpvars(0, fulladder_tb);
    A=1'b0;  B=1'b0;  
    C_in=1'b0;
    for (i = 0; i < 8; i = i + 1) begin
       #1
       {C_in,B,A}=i;
       
    end
    
    #1 $finish;
  end
  
endmodule
