`include "comparator.v"
module comparator_tb;
  reg [3:0] A;
  reg [3:0] B;
  wire greater,lesser,equal;
  comparator DUT(A,B,greater,lesser,equal);
  
  
  initial begin
    $dumpfile("comparator_tb.vcd");
    $dumpvars(0, comparator_tb);
    
    A=4'b0101;
    B=4'b1001;
    #10
   
    A=4'b1011;
    B=4'b1011;
    #10
   
    A=4'B1011;
    B=4'b1111;
    #10
    
    A=4'b1001;
    B=4'b0110;
    #10
    
    A=4'b1111;
    B=4'b1111;
    #10
  
    A=4'b0100;
    B=4'b1100;
    #10

    A=4'b1110;
    B=4'b0000;
    #10

    A=4'b0011;
    B=4'b1100;

    #10 $finish; 
  end
  
endmodule

  

