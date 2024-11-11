module fetch(input clk,input [3:0] M_icode,input M_Cnd,input [63:0] M_valA,input [3:0] W_icode,input [63:0] W_valM,input [63:0] F_predPC,input F_stall,
input D_stall,input [63:0] D_valP,input [7:0] D_opcode,input [7:0] D_rArB,input [63:0] D_valC,input [1:0] D_stat,input D_bubble,
output reg [63:0] f_valP,output reg [7:0]f_opcode,output reg [7:0] f_rArB,output reg [63:0] f_valC,output reg [1:0] f_stat,output reg [63:0] f_predPC);
    reg addrerror;
    reg instrerror;
    reg halterror;
    reg addrerror1,addrerror2,addrerror3,addrerror4;
    reg [7:0] instructionmemory [4095:0];
     initial begin
       $readmemb("Demo.txt", instructionmemory);
       f_pc=0;
       stall=0;
     end
     reg [63:0] val_2;
     reg [63:0] f_pc;
     reg [63:0] val_1;
     integer i;
     reg stall;



    always @(*) begin
      if(stall) begin
        f_pc=F_predPC;
      end
        
      if(M_icode==4'b0111&&M_Cnd==0) begin
           f_pc=M_valA;
      end
      else if(W_icode==4'b1001) begin 
          f_pc=W_valM;
      end
      else begin
        f_pc=F_predPC;
      end
      

      if(f_pc>4095) begin
        addrerror1=1;
      end
      else begin
        addrerror1=0;
      end

      if(f_pc+1>4095) begin
        addrerror2=1;
      end
      else begin
        addrerror2=0;
      end
      if(f_pc+9>4095) begin
        addrerror3=1;
      end
      else begin
        addrerror3=0;
      end

      if(f_pc+8>4095) begin
        addrerror4=1;
      end
      else begin
        addrerror4=0;
      end
     
     if(addrerror1==0) begin
       f_opcode=instructionmemory[f_pc];
     end
     else begin
       f_opcode=8'b00000000;
     end

     if(addrerror2==0) begin
        f_rArB=instructionmemory[f_pc+1];
     end
     else begin
        f_rArB=0;
     end

     if(addrerror3==0) begin
        val_2[63:56]=instructionmemory[f_pc+9]; val_2[55:48]=instructionmemory[f_pc+8]; val_2[47:40]=instructionmemory[f_pc+7]; val_2[39:32]=instructionmemory[f_pc+6];
        val_2[31:24]=instructionmemory[f_pc+5]; val_2[23:16]=instructionmemory[f_pc+4]; val_2[15:8]=instructionmemory[f_pc+3]; val_2[7:0]=instructionmemory[f_pc+2];
     end
     else begin
        val_2=0;
     end

      if(addrerror4==0) begin
        val_1[63:56]=instructionmemory[f_pc+8]; val_1[55:48]=instructionmemory[f_pc+7]; val_1[47:40]=instructionmemory[f_pc+6]; val_1[39:32]=instructionmemory[f_pc+5];
        val_1[31:24]=instructionmemory[f_pc+4]; val_1[23:16]=instructionmemory[f_pc+3]; val_1[15:8]=instructionmemory[f_pc+2]; val_1[7:0]=instructionmemory[f_pc+1];
     end
     else begin
        val_1=0;
     end

    if(f_opcode==8'b00010000||f_opcode==8'b00000000||f_opcode==8'b10010000) begin
        instrerror=0;
        addrerror=addrerror1;
        f_valP=f_pc+1;
    end
    else if(f_opcode[7:4]==4'b0010||f_opcode[7:4]==4'b0110||f_opcode[7:4]==4'b1010||f_opcode[7:4]==4'b1011) begin
        if((f_opcode[7:4]==4'b0010&&f_opcode[3:0]>6)||(f_opcode[7:4]==4'b0110&&f_opcode[3:0]>3)||(f_opcode[7:4]==4'b1011&&f_rArB[3:0]!=4'b1111)||(f_opcode[7:4]==4'b1010&&f_rArB[3:0]!=4'b1111)) begin
            instrerror=1;
        end
        else begin
            instrerror=0;
        end
        addrerror=addrerror1|addrerror2;
        f_valP=f_pc+2;
    end
    else if(f_opcode[7:4]==4'b0111||f_opcode[7:4]==4'b1000) begin
        if(f_opcode[7:4]==4'b0111&&f_opcode[3:0]>6) begin
            instrerror=1;
        end
        else begin
            instrerror=0;
        end
        f_valC=val_1;
        addrerror=addrerror1|addrerror4;
        f_valP=f_pc+9;
    end
    else if(f_opcode[7:4]==4'b0011||f_opcode[7:4]==4'b0100||f_opcode[7:4]==4'b0101) begin
        f_valC=val_2;
        addrerror=addrerror1|addrerror2|addrerror3;
        if(f_opcode[7:4]==4'b0011&&f_rArB[7:4]!=4'b1111) begin
        instrerror=1;
        end
        else begin
            instrerror=0;
        end
        f_valP=f_pc+10;
    end
    else begin
        addrerror=addrerror1;
        instrerror=1;
        f_valP=f_pc+1;
    end

   if(F_stall==0) begin
    stall=0;
   if(f_opcode [7:4]==4'b0111||f_opcode[7:4]==4'b1000) begin
     f_predPC=f_valC;
   end
   else begin
     f_predPC=f_valP;
   end
   end
   else begin
    f_predPC=f_pc;
    stall=1;
   end
   
  
   if(f_opcode==8'b00000000) begin
    halterror=1;
   end
   else begin
    halterror=0;
   end

    if(addrerror==1)begin
      f_stat=2;
    end
    else if(halterror==1)begin
        f_stat=1;
    end
    else if(instrerror==1)begin
        f_stat=3;
    end
    else begin
        f_stat=0;
    end
    
    if(F_stall) begin
      f_stat=0;
    end
     
    if(D_bubble) begin
     f_opcode=8'b00010000;
     f_stat=0;
    end
    
    if(D_stall)begin
     f_opcode=D_opcode;
      f_valP=D_valP;
      f_valC=D_valC;
      f_rArB=D_rArB;
      f_stat=D_stat;
    end
    end

    //  initial begin
    //   $monitor("%d",f_pc);
    // end
endmodule
