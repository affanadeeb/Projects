module ADD_64(input [63:0] A,input [63:0] B,output [63:0] sum,output overflow);
    wire [63:0] carry;
    wire temp1,temp2,temp3;
    genvar i;
    fulladder instance_0(A[0],B[0],1'b0,sum[0],carry[0]);
    generate
        for (i=1;i<64;i=i+1)
        begin
            fulladder instance_i(A[i],B[i],carry[i-1],sum[i],carry[i]);
        end
    endgenerate
    xor(temp1,A[63],B[63]);
    not(temp2,temp1);
    xor(temp3,carry[63],sum[63]);
    and(overflow,temp3,temp2);
endmodule