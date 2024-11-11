module PCupdate(input [7:0] opcode,input [63:0] valP,input [63:0] valM,input [63:0] valC,input Cnd,output reg [63:0] finalval_PC);
  always @(*) begin
  if(opcode [7:4]==4'b0111) begin
    if(Cnd==1) begin//if cnd is 1 jump to dest
      finalval_PC=valC;
    end
    else begin
      finalval_PC=valP;
    end
  end
  else if(opcode[7:4]==4'b1000) begin
     finalval_PC=valC;
  end  
  else if(opcode[7:4]==4'b1001) begin
    finalval_PC=valM;
  end
  else begin
    finalval_PC=valP;
  end
  end
endmodule
