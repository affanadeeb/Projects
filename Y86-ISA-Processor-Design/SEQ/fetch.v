module fetch(input clk,input [63:0] pc,output reg [63:0] valP,output reg [7:0] opcode,output reg [7:0] rArB,output reg [63:0] valC,output reg [1:0] status);
    reg addrerror;
    reg instrerror;
    reg halterror;
    wire addrerror1,addrerror2,addrerror3,addrerror4;
    reg [7:0] instructionmemory [1023:0];
     initial begin
       $readmemb("Demo.txt", instructionmemory);
     end
     reg [7:0] opcode_temp;
     reg [7:0] rArB_temp;
     reg [63:0] val_2;
     reg [63:0] val_1;
     
     checkpc inst1_pc(pc,addrerror1);
     checkpc inst2_pc(pc+1,addrerror2);
     checkpc inst3_pc(pc+9,addrerror3);
     checkpc inst4_pc(pc+8,addrerror4);
     
    integer i;


    always @(posedge clk) begin
     if(addrerror1==0) begin
        opcode=instructionmemory[pc];
     end
     else begin
        opcode=8'b00000000;
     end

     if(addrerror2==0) begin
        rArB=instructionmemory[pc+1];
     end
     else begin
        rArB=0;
     end

     if(addrerror3==0) begin
        val_2[63:56]=instructionmemory[pc+9]; val_2[55:48]=instructionmemory[pc+8]; val_2[47:40]=instructionmemory[pc+7]; val_2[39:32]=instructionmemory[pc+6];
        val_2[31:24]=instructionmemory[pc+5]; val_2[23:16]=instructionmemory[pc+4]; val_2[15:8]=instructionmemory[pc+3]; val_2[7:0]=instructionmemory[pc+2];
     end
     else begin
        val_2=0;
     end

      if(addrerror4==0) begin
        val_1[63:56]=instructionmemory[pc+8]; val_1[55:48]=instructionmemory[pc+7]; val_1[47:40]=instructionmemory[pc+6]; val_1[39:32]=instructionmemory[pc+5];
        val_1[31:24]=instructionmemory[pc+4]; val_1[23:16]=instructionmemory[pc+3]; val_1[15:8]=instructionmemory[pc+2]; val_1[7:0]=instructionmemory[pc+1];
     end
     else begin
        val_1=0;
     end

    if(opcode==8'b00010000||opcode==8'b00000000||opcode==8'b10010000) begin
        instrerror=0;
        addrerror=addrerror1;
        valP=pc+1;
    end
    else if(opcode[7:4]==4'b0010||opcode[7:4]==4'b0110||opcode[7:4]==4'b1010||opcode[7:4]==4'b1011) begin
        if((opcode[7:4]==4'b0010&&opcode[3:0]>6)||(opcode[7:4]==4'b0110&&opcode[3:0]>3)||(opcode[7:4]==4'b1011&&rArB[3:0]!=4'b1111)||(opcode[7:4]==4'b1010&&rArB[3:0]!=4'b1111)) begin
            instrerror=1;
        end
        else begin
            instrerror=0;
        end
        addrerror=addrerror1|addrerror2;
        valP=pc+2;
    end
    else if(opcode[7:4]==4'b0111||opcode[7:4]==4'b1000) begin
        if(opcode[7:4]==4'b0111&&opcode[3:0]>6) begin
            instrerror=1;
        end
        else begin
            instrerror=0;
        end
        valC=val_1;
        addrerror=addrerror1|addrerror4;
        valP=pc+9;
    end
    else if(opcode[7:4]==4'b0011||opcode[7:4]==4'b0100||opcode[7:4]==4'b0101) begin
        valC=val_2;
        addrerror=addrerror1|addrerror2|addrerror3;
        if(opcode[7:4]==4'b0011&&rArB[7:4]!=4'b1111) begin
        instrerror=1;
        end
        else begin
            instrerror=0;
        end
        valP=pc+10;
    end
    else begin
        addrerror=addrerror1;
        instrerror=1;
        valP=pc+1;
    end

   if(opcode==8'b00000000) begin
    halterror=1;
   end
   else begin
    halterror=0;
   end

    if(addrerror==1)begin
      status=2;//Invalid address
    end
    else if(halterror==1)begin
        status=1;//1-halt
    end
    else if(instrerror==1)begin
        status=3;//3-Invalid instruction
    end
    else begin
        status=0;//0-correct instruction
    end
    end
//doubt---if there are invalid address and invalid instruction both are there then??
endmodule
