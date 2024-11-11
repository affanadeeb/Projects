module execute(input [1:0] E_status,input [7:0] E_opcode,input [63:0] E_valA,input [63:0] E_valB,input [63:0] E_valC,input [3:0] E_dstE,input [3:0] E_dstM,
input [3:0] E_srcA,input [3:0] E_srcB,
output reg [1:0] e_status,output reg [3:0] e_icode,output [63:0] e_valE,output reg [63:0] e_valA,output reg [3:0] e_dstM,output reg e_Cnd,output reg [3:0] e_dstE);
reg [1:0] alufun;
wire overflow;
reg e_Cnd_temp;
reg [63:0] aluA;
reg [63:0] aluB;
reg op; 
reg [2:0] cc;

initial begin cc=0;
end
ALU instance_execute(aluA,aluB,alufun,e_valE,overflow); 
always @(*) begin

  if(E_opcode[7:4]==4'b0110||E_opcode[7:4]==4'b0100||E_opcode[7:4]==4'b0101||E_opcode[7:4]==4'b1011||E_opcode[7:4]==4'b1001||E_opcode[7:4]==4'b1000||E_opcode[7:4]==4'b1010) 
  begin
    aluA=E_valB;
  end
  else begin
    aluA=0;
  end

  
  if(E_opcode[7:4]==4'b0110||E_opcode[7:4]==4'b0010) begin
    aluB=E_valA;
  end
  else if(E_opcode[7:4]==4'b0011||E_opcode[7:4]==4'b0100||E_opcode[7:4]==4'b0101) begin
    aluB=E_valC;
  end
  else if(E_opcode[7:4]==4'b1011||E_opcode[7:4]==4'b1001||E_opcode[7:4]==4'b1000||E_opcode[7:4]==4'b1010)begin
    aluB=8;
 end
else begin
  aluB=0;
end

if(E_opcode[7:4]==4'b0110) begin
  alufun=E_opcode[1:0];
  op=1;
end
else if(E_opcode[7:4]==4'b1000||E_opcode[7:4]==4'b1010) begin
  alufun=1;
  op=0;
end
else begin
  alufun=0;
  op=0;
end

  e_status=E_status;
  e_icode=E_opcode[7:4];
  e_valA=E_valA;
  e_dstM=E_dstM;

if(E_opcode[3:0]==4'b0000) begin
  e_Cnd_temp=1;
end
else if(E_opcode[3:0]==4'b0001) begin
    e_Cnd_temp=(cc[1]^cc[2])|cc[0];
  end

  else if(E_opcode[3:0]==4'b0010) begin
    e_Cnd_temp=cc[1]^cc[2];
  end
  else if(E_opcode[3:0]==4'b0011)begin
    e_Cnd_temp=cc[0];
  end
  else if(E_opcode[3:0]==4'b0100)begin
      e_Cnd_temp=~cc[0];
  end
  else if(E_opcode[3:0]==4'b0101)begin
      e_Cnd_temp=~(cc[1]^cc[2]);
  end
  else if(E_opcode[3:0]==4'b0110)begin
  e_Cnd_temp= ~(cc[1]^cc[2])&~(cc[0]);
end
else begin
  e_Cnd_temp=0;
end

if(E_opcode[7:4]==4'b0010) begin
    if(e_Cnd_temp==1) begin
      e_dstE=E_dstE;
    end
    else begin
       e_dstE=4'b1111;
    end
end
else begin
  e_dstE=E_dstE;
end

if(E_opcode [7:4]==4'b0111) begin
  e_Cnd=e_Cnd_temp;
end
else begin
  e_Cnd=0;
end

if(op==1) begin
  cc[2]=overflow;
  if(e_valE==0) begin
    cc[0]=1;
  end
  else begin
    cc[0]=0;
  end

  if(e_valE[63]==1'b1) begin
    cc[1]=1;
  end
  else begin
    cc[1]=0;
  end
end
end

 
endmodule