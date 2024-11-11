module decode (
  input [7:0] opcode,
  input [7:0] rArB,
  input [63:0] valC,
  output reg error,
  output reg [3:0] registernumber1,
  output reg [3:0] registernumber2
);  //based on opcoded,sets register number to be read which goes to register which reads and gives the output
  reg error1,error2;
  always @(*) begin
    if(rArB[7:4]==4'b1111) begin
          error1=1;
    end //checks if rA,rB are valid registers or not
    else begin
      error1=0;
    end
    if(rArB[3:0]==4'b1111) begin
      error2=1;
    end
    else begin
      error2=0;
    end
    if ((opcode[7:4] == 4'b0100) || (opcode[7:4] == 4'b0101) || (opcode[7:4] == 4'b0110)) begin
      registernumber1 = rArB[7:4];
      registernumber2 = rArB[3:0];
      error = error1|error2;
    end
    else if (opcode[7:4] == 4'b0010) begin
      registernumber1 = rArB[7:4];
      registernumber2 = 4'b0000;
      error = error1|error2;
    end
    else if (opcode[7:4] == 4'b0011) begin
      error=error2;
      registernumber1 = rArB[3:0];
      registernumber2 = 4'b0000;
    end
    else if ((opcode[7:4] == 4'b1001) || (opcode[7:4] == 4'b1000)||(opcode[7:4]==4'b1011)) begin
      registernumber1 = 4'b0100;
      registernumber2 = 4'b0100;
      error = 0;
    end
    else if(opcode[7:4]==4'b1010) begin
      registernumber1=rArB[7:4];
      registernumber2=4'b0100;
      error=error1;
    end
    else begin
      error = 0; 
      registernumber1 = 4'b0000; 
      registernumber2 = 4'b0000;
    end
  end
  
endmodule
