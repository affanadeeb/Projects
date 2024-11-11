module twotofourdecoder(input S0,input S1,output D0,output D1,output D2,output D3);
  wire S0_comp;
  wire S1_comp;
  not(S0_comp,S0);
  not(S1_comp,S1);
  and(D0,S0_comp,S1_comp);
  and(D1,S0,S1_comp);
  and(D2,S1,S0_comp);
  and(D3,S0,S1);
endmodule