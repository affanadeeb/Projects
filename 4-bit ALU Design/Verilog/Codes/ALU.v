`include "twotofourdecoder.v"
`include "enableblock.v"
`include "addersubtractor.v"
`include "comparator.v"
`include "andblock.v"
module ALU(input S0,input S1,input [3:0] A,input [3:0] B,output [3:0] S_0,output carry,output greater,output lesser,output equal,output [3:0] S_3 );
   wire D0,D1,D2,D3;
   wire [3:0] A_0;
   wire [3:0] A_2;
   wire [3:0] A_3;
   wire [3:0] B_0;
   wire [3:0] B_2;
   wire [3:0] B_3;
  wire D_updated;
  wire equal_temp;
  wire carry_temp;
  wire carry_temp2;
  twotofourdecoder instance_1(.S0(S0),.S1(S1),.D0(D0),.D1(D1),.D2(D2),.D3(D3));
  or(D_updated,D0,D1);
  enableblock inst_1(.enable(D_updated),.A_in(A),.B_in(B),.A_out(A_0),.B_out(B_0));
  enableblock inst_2(.enable(D2),.A_in(A),.B_in(B),.A_out(A_2),.B_out(B_2));
  enableblock inst_3(.enable(D3),.A_in(A),.B_in(B),.A_out(A_3),.B_out(B_3));
  addersubtractor inst_4(.M(S0),.A(A_0),.B(B_0),.S(S_0),.carry(carry_temp));
  comparator inst_5(.A(A_2),.B(B_2),.greater(greater),.lesser(lesser),.equal(equal_temp));
  andblock inst_6(.A(A_3),.B(B_3),.C(S_3));
  and(equal,equal_temp,D2);
  and(carry_temp2,carry_temp,D_updated);
  xor(carry,carry_temp2,D1);

endmodule