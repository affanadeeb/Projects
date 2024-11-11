`include "fulladder.v"
module addersubtractor(input M,input [3:0] A,input [3:0] B,output [3:0] S,output carry);
  wire [3:0] B_updated;
  xor(B_updated[3],B[3],M);
  xor(B_updated[2],B[2],M);
  xor(B_updated[1],B[1],M);
  xor(B_updated[0],B[0],M);
  wire C1;
  wire C2;
  wire C3;
  fulladder instance_1(.A(A[0]),.B(B_updated[0]),.C_in(M),.S(S[0]),.C(C1));
  fulladder instance_2(.A(A[1]),.B(B_updated[1]),.C_in(C1),.S(S[1]),.C(C2));
  fulladder instance_3(.A(A[2]),.B(B_updated[2]),.C_in(C2),.S(S[2]),.C(C3));
  fulladder instance_4(.A(A[3]),.B(B_updated[3]),.C_in(C3),.S(S[3]),.C(carry));
  
endmodule