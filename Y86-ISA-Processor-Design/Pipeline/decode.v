module decode (
  input [7:0] D_opcode,
  input [7:0] D_rArB,
  input [63:0] D_valC,
  input [63:0] D_valP,
  input [1:0] D_stat,input E_bubble,
  input [3:0] e_dstE,input [63:0] e_valE,input [3:0] M_dstE,input [63:0] M_valE,input [3:0] M_dstM,input [63:0] m_valM,input [3:0] W_dstM,input [63:0] W_valM,
  input [3:0] W_dstE,input [63:0] W_valE,
  output reg [1:0] d_stat,
  output reg [7:0] d_opcode,
  output reg [63:0] d_valC,
  output reg [63:0] d_valA,
  output reg [63:0] d_valB,
  output reg [3:0] d_dstE,
  output reg [3:0] d_dstM,
  output reg [3:0] d_srcA,
  output reg [3:0] d_srcB
);  
  reg error1,error2;
  reg error;
  reg check1,check2;
  reg [63:0] registers [15:0]; 
  integer i;
 initial begin
  for(i=0;i<16;i=i+1)begin
    registers[i]=0;
  end
  registers[4]=512;
 end

  always @(*) begin

        

    if(D_rArB[7:4]==4'b1111) begin
          error1=1;
    end
    else begin
      error1=0;
    end
    if(D_rArB[3:0]==4'b1111) begin
      error2=1;
    end
    else begin
      error2=0;
    end
    
   
    if(D_opcode[7:4]==4'b0010||D_opcode[7:4]==4'b0100||D_opcode[7:4]==4'b0110||D_opcode[7:4]==4'b1010) begin
      d_srcA=D_rArB[7:4];
     check1=1;
    end
    else if(D_opcode[7:4]==4'b1001 || D_opcode[7:4]==4'b1011) begin
      d_srcA=4'b0100;
      check1=0;
    end 
    else begin
      d_srcA=4'b1111;
      check1=0;
    end

    if(D_opcode[7:4]==4'b0100||D_opcode[7:4]==4'b0101||D_opcode[7:4]==4'b0110) begin
      d_srcB=D_rArB[3:0];
      check2=1;
    end
    else if(D_opcode[7:4]==4'b1000||D_opcode[7:4]==4'b1001||D_opcode[7:4]==4'b1010||D_opcode[7:4]==4'b1011) begin
      d_srcB=4'b0100;
      check2=0;
    end
    else begin
      d_srcB=4'b1111;
      check2=0;
    end

    error=(check1&error1)|(check2&error2);

   if(D_opcode[7:4]==4'b0011||D_opcode[7:4]==4'b0110||D_opcode[7:4]==4'b0010)begin
       d_dstE=D_rArB[3:0];
    end
    else if(D_opcode[7:4]==4'b1000||D_opcode[7:4]==4'b1001||D_opcode[7:4]==4'b1010||D_opcode[7:4]==4'b1011) begin
       d_dstE=4'b0100;
    end
    else begin
      d_dstE=4'b1111;
    end

    if(D_opcode[7:4]==4'b0101||D_opcode[7:4]==4'b1011) begin
      d_dstM=D_rArB[7:4];
    end
    else begin
      d_dstM=4'b1111;
    end
    

    if(error==0) begin
      d_stat=D_stat;
    end
    else begin
      d_stat=3;
    end


    if(D_opcode[7:4]==4'b0111||D_opcode[7:4]==4'b1000) begin
      d_valA=D_valP;
    end
    else if(d_srcA==e_dstE) begin
      d_valA=e_valE;
    end
    else if(d_srcA==M_dstM)begin
      d_valA=m_valM;
    end
    else if(d_srcA==M_dstE) begin
      d_valA=M_valE;
    end
    else if(d_srcA==W_dstM) begin
      d_valA=W_valM;
    end
    else if(d_srcA==W_dstE) begin
      d_valA=W_valE;
    end
    else begin
      d_valA=registers[d_srcA];
    end

    if(d_srcB==e_dstE) begin
      d_valB=e_valE;
    end
    else if(d_srcB==M_dstM)begin
      d_valB=m_valM;
    end
    else if(d_srcB==M_dstE) begin
      d_valB=M_valE;
    end
    else if(d_srcB==W_dstM) begin
      d_valB=W_valM;
    end
    else if(d_srcB==W_dstE) begin
      d_valB=W_valE;
    end
    else begin
      d_valB=registers[d_srcB];
    end

    if(E_bubble) begin
         d_opcode=8'b00010000;
         d_dstE=4'b1111;
         d_dstM=4'b1111;
         d_stat=0;
    end
    else begin
     d_opcode=D_opcode;
     d_valC=D_valC;
    end

    registers[W_dstM]=W_valM;
    registers[W_dstE]=W_valE;



  end
  
endmodule