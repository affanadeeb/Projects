`include "andblock.v"
module andblock_tb;
  reg [3:0] A;
  reg [3:0] B;
  wire [3:0] C;
  andblock DUT(A,B,C);
  
   initial begin
    $dumpfile("andblock_tb.vcd");
    $dumpvars(0, andblock_tb);
    
    A=4'b0101;
    B=4'b1001;
    #10
   
    A=4'b0100;
    B=4'b1011;
    #10
   
    A=4'b0000;
    B=4'b1111;
    #10
    
    A=4'b0110;
    B=4'b1101;
    #10
    
    A=4'b1000;
    B=4'b1000;
    #10
  
    A=4'b0101;
    B=4'b1100;
    #10

    A=4'b0000;
    B=4'b1011;
    #10

    A=4'b0011;
    B=4'b1100;

    #10 $finish; 
  end
  
endmodule

  

