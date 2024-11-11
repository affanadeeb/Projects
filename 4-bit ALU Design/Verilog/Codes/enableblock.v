module enableblock(input enable,input [3:0] A_in,input [3:0] B_in,output [3:0] A_out,output [3:0] B_out);
  and(A_out[3],A_in[3],enable);
  and(A_out[2],A_in[2],enable);
  and(A_out[1],A_in[1],enable);
   and(A_out[0],A_in[0],enable);
   and(B_out[3],B_in[3],enable);
  and(B_out[2],B_in[2],enable);
  and(B_out[1],B_in[1],enable);
  and(B_out[0],B_in[0],enable);
endmodule