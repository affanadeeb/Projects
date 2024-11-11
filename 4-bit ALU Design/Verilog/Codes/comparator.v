module comparator(input [3:0] A,input [3:0] B,output greater,output lesser,output equal);
  wire eq0;
  wire eq1;
  wire eq2;
  wire eq3;
  xnor(eq0,A[0],B[0]);
  xnor(eq1,A[1],B[1]);
  xnor(eq2,A[2],B[2]);
  xnor(eq3,A[3],B[3]);

  
  wire [3:0] A_comp;
  wire [3:0] B_comp;
  not(A_comp[3],A[3]);
  not(A_comp[2],A[2]);
  not(A_comp[1],A[1]);
  not(A_comp[0],A[0]);
  not(B_comp[3],B[3]);
  not(B_comp[2],B[2]);
  not(B_comp[1],B[1]);
  not(B_comp[0],B[0]);


  wire greater0;
  wire greater1;
  wire greater2;
  wire greater3;
  and(greater3,A[3],B_comp[3]);
  and(greater2,eq3,A[2],B_comp[2]);
  and(greater1,eq3,eq2,A[1],B_comp[1]);
  and(greater0,eq3,eq2,eq1,A[0],B_comp[0]);

 
  wire lesser0;
  wire lesser1;
  wire lesser2;
  wire lesser3;
  and(lesser3,A_comp[3],B[3]);
  and(lesser2,eq3,A_comp[2],B[2]);
  and(lesser1,eq3,eq2,A_comp[1],B[1]);
  and(lesser0,eq3,eq2,eq1,A_comp[0],B[0]);
  

  and(equal,eq0,eq1,eq2,eq3);
  or(greater,greater0,greater1,greater2,greater3);
  or(lesser,lesser0,lesser1,lesser2,lesser3);


endmodule