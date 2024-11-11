`include "addersubtractor.v"
module addersubtractor_tb;
  reg [3:0] A;
  reg [3:0] B;
  reg M;
  wire [3:0] S;
  wire carry;
  addersubtractor DUT(M,A,B,S,carry);
  
  
  initial begin
    $dumpfile("addersubtractor_tb.vcd");
    $dumpvars(0, addersubtractor_tb);
    M=0;
    A=4'b0101;
    B=4'b1001;
    #10
    M=1;
    A=4'b0100;
    B=4'b1011;
    #10
    M=0;
    A=4'b0000;
    B=4'b1111;
    #10
    M=0;
    A=4'b0110;
    B=4'b1101;
    #10
    M=1;
    A=4'b1000;
    B=4'b1000;
    #10
    M=1;
    A=4'b0101;
    B=4'b1100;
    #10
    M=1;
    A=4'b0000;
    B=4'b1001;
    #10
    M=0;
    A=4'b0011;
    B=4'b1100;

    #10 $finish; 
  end
  
endmodule

  

