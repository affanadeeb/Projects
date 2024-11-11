module fulladder(input A,input B,input C_in,output S,output C);
   wire S_inter;
   wire C_inter1;
   wire C_inter2;
   xor(S_inter,A,B);
   xor(S,S_inter,C_in);
   and(C_inter1,A,B);
   and(C_inter2,S_inter,C_in);
   or(C,C_inter1,C_inter2);

endmodule