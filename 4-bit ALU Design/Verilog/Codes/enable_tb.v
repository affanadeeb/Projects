`include "enableblock.v"
module enable_tb;
  reg enable;
  reg [3:0] A_in;
  reg [3:0] B_in;
  wire [3:0] A_out;
  wire [3:0] B_out;
  enableblock DUT(enable,A_in,B_in,A_out,B_out);
  
  initial begin
    $dumpfile("enable_tb.vcd");
    $dumpvars(0, enable_tb);
    enable=1'b1;
    A_in=4'b0101;
    B_in=4'b1001;
    #10
    enable=1'b0;
    A_in=4'b0100;
    B_in=4'b1011;
    #10
    enable=1'b1;
    A_in=4'b0000;
    B_in=4'b1111;
    #10
    enable=1'b1;
    A_in=4'b0110;
    B_in=4'b1101;
    #10
    enable=1'b0;
    A_in=4'b1000;
    B_in=4'b1000;
    #10
     enable=1'b0;
    A_in=4'b0101;
    B_in=4'b1100;

    
    $finish; 
  end
  
endmodule
