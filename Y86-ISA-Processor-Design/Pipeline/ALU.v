module ALU(input [63:0] A,input [63:0] B,input [1:0] control,output [63:0] C,output overflow);
  wire [63:0] C1;
  wire [63:0] C2;
  wire [63:0] C3;
  wire [63:0] C4;
  wire [63:0] A1;
  wire [63:0] A2;
  wire [63:0] A3;
  wire [63:0] A4;
  wire overflow1,overflow2;
  wire overflow11,overflow22;
  wire temp1,temp2;
  wire D0,D1,D2,D3;
  not(temp1,control[0]);
  not(temp2,control[1]);
  and(D0,temp1,temp2);
  and(D1,temp2,control[0]);
  and(D2,control[1],temp1);
  and(D3,control[0],control[1]);
  ADD_64 instance1(A, B, C1, overflow1);
  SUB_64 instance2(A, B, C2, overflow2);
  AND_64 instance3(A, B, C3);
  XOR_64 instance4(A, B, C4);

  genvar i;
   generate
    for(i=0;i<64;i=i+1)
    begin
      and(A1[i],C1[i],D0);
    end
   endgenerate
   and(overflow11,overflow1,D0);

   generate
    for(i=0;i<64;i=i+1)
    begin
      and(A2[i],C2[i],D1);
    end
   endgenerate
   and(overflow22,overflow2,D1);

   generate
    for(i=0;i<64;i=i+1)
    begin
      and(A3[i],C3[i],D2);
    end
   endgenerate

   generate
    for(i=0;i<64;i=i+1)
    begin
      and(A4[i],C4[i],D3);
    end
   endgenerate

    generate
    for(i=0;i<64;i=i+1)
    begin
      or(C[i],A1[i],A2[i],A3[i],A4[i]);
    end
   endgenerate

   or(overflow,overflow11,overflow22);


endmodule