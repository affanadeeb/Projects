module execute(input [7:0] opcode,input [7:0] rArB,input [63:0] valA,input [63:0] valB,input [63:0] valC,input [2:0] cc,output [63:0] valE,output reg [7:0] rArB_execute,output reg Cnd,output reg [2:0] cc_out);
reg [1:0] control;
wire overflow;
reg Cnd_temp;
reg [63:0] input1;
reg [63:0] input2;
reg op;
ALU instance_execute(input1,input2,control,valE,overflow); //ALU driven by input which varies with respecto to the opcode
always @(*) begin
if(opcode[7:4]==4'b0110) begin//6    // changing input1,input2 based on icode 
    control=opcode[1:0];
    input1=valB;
    input2=valA;
    op=1;
end
else if(opcode[7:4]==4'b0100||opcode[7:4]==4'b0101)begin//4,5
    control=2'b00;
    input1=valB;
    input2=valC;
    op=0;
end
else if(opcode[7:4]==4'b1011||opcode[7:4]==4'b1001)begin//9,11
    control=2'b00;
    input1=valB;
    input2=64'd8;
    op=0;
end
else if(opcode[7:4]==4'b0010) begin//2
     control=2'b00;
     input1=valA;
     input2=64'd0;
     op=0;
end
else if(opcode[7:4]==4'b1000||opcode[7:4]==4'b1010) begin//8,10
    control=2'b01;
    input1=valB;
    input2=64'd8;
    op=0;

end
else if(opcode[7:4]==4'b0011) begin//3
    control=2'b00;
     input1=valC;
    input2=64'd0;
    op=0;
end
else begin
  op=0;
end

if(op==1) begin//updating cc if opq has occured
  cc_out[2]=overflow;//setting overflow bit after execute
  if(valE==0) begin//setting zero cc bit after execute
    cc_out[0]=1;
  end
  else begin
    cc_out[0]=0;
  end

  if(valE[63]==1'b1) begin//setting output sign bit after execute
    cc_out[1]=1;
  end
  else begin
    cc_out[1]=0;
  end
  end

else begin//setting output cc to input if no op in execute
  cc_out=cc;
end

if(opcode[3:0]==4'b0000) begin
  Cnd_temp=1;
end
else if(opcode[3:0]==4'b0001) begin//le
    Cnd_temp=(cc_out[1]^cc_out[2])|cc_out[0];//setting Cnd_temp for jump and cmov cases otherwise not used at all
  end

  else if(opcode[3:0]==4'b0010) begin//l
    Cnd_temp=cc_out[1]^cc_out[2];
  end
  else if(opcode[3:0]==4'b0011)begin//e
    Cnd_temp=cc_out[0];
  end
  else if(opcode[3:0]==4'b0100)begin//ne
      Cnd_temp=~cc_out[0];
  end
  else if(opcode[3:0]==4'b0101)begin//ge
      Cnd_temp=~(cc_out[1]^cc_out[2]);
  end
  else if(opcode[3:0]==4'b0110)begin//g
  Cnd_temp= ~(cc_out[1]^cc_out[2])&~(cc_out[0]);
end
else begin
  Cnd_temp=0;
end
if(opcode[7:4]==4'b0010) begin//changing rB to 15 if condition for cmov is not satisfied
    if(Cnd_temp==1) begin
      rArB_execute=rArB;
    end
    else begin
      rArB_execute[7:4]=rArB[7:4];
       rArB_execute[3:0]=4'b1111;
    end
end
else begin
  rArB_execute=rArB;
end

if(opcode [7:4]==4'b0111) begin//setting Cnd for jump case.If Cnd is 1,jump to Dest,other wise no jump
  Cnd=Cnd_temp;
end
else begin
  Cnd=0;
end
end
endmodule