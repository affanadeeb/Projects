module registerwrite (input [7:0] opcode,input [7:0] rArB,input [63:0] valE,input [63:0] valM,output reg reset,
output reg [3:0] registernumber1,output reg [3:0] registernumber2,output reg [63:0] val_write1,output reg [63:0] val_write2,output reg wrEn);

  wire error1, error2;
  wire [63:0] temp1;
  wire [63:0] temp2;

  always @(*) begin
    if ((opcode[7:4] == 4'b0110) || (opcode[7:4] == 4'b0011) || (opcode[7:4] == 4'b0010)) begin 
      reset = 0; 
      registernumber1 = rArB[3:0]; 
      registernumber2 = 4'b1111; 
      val_write1 = valE; 
      val_write2 = 64'hFFFFFFFFFFFFFFFF; 
      wrEn=1;
    end
    else if (opcode[7:4] == 4'b0101) begin
      reset = 0; 
      registernumber1 = rArB[7:4]; 
      registernumber2 = 4'b1111; 
      val_write1 = valM; 
      val_write2 = 64'hFFFFFFFFFFFFFFFF; 
      wrEn=1;
    end
    else if (opcode[7:4] == 4'b1011) begin
      reset = 0; 
      registernumber1 = 4'b0100; 
      registernumber2 = rArB[7:4]; 
      val_write1 = valE; 
      val_write2 = valM; 
      wrEn=1;
    end
    else if ((opcode[7:4] == 4'b1000) || (opcode[7:4] == 4'b1001) || (opcode[7:4] == 4'b1010)) begin
      reset = 0; 
      registernumber1 = 4'b0100; 
      registernumber2 = 4'b1111; 
      val_write1 = valE; 
      val_write2 = valE; 
      wrEn=1;
    end
    else begin
      reset = 0; 
      registernumber1 = 4'b1111; 
      registernumber2 = 4'b1111; 
      val_write1 = valE; 
      val_write2 = valE; 
      wrEn=0;
    end
  end
endmodule
