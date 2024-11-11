module andblock(input [3:0] A,input [3:0] B,output [3:0] C);
  and(C[3],A[3],B[3]);
  and(C[2],A[2],B[2]);
  and(C[1],A[1],B[1]);
  and(C[0],A[0],B[0]);
endmodule