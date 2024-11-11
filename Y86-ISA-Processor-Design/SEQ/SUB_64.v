module SUB_64(input [63:0] A,input [63:0] B,output [63:0] sum,output overflow);
    wire [63:0] carry2;
    wire temp1,temp2;
    wire [63:0] B_updated1; 
    genvar j;
    generate
        for(j=0;j<64;j=j+1)
        begin
            xor(B_updated1[j],B[j],1);
        end
    endgenerate
    genvar i;
    fulladder instance_0(A[0],B_updated1[0],1'b1,sum[0],carry2[0]);
    generate
        for (i=1;i<64;i=i+1)
        begin
            fulladder instance_i(A[i],B_updated1[i],carry2[i-1],sum[i],carry2[i]);
        end
    endgenerate
    xor(temp1,A[63],B[63]);
    xor(temp2,carry2[63],sum[63]);
    and(overflow,temp1,temp2);
endmodule