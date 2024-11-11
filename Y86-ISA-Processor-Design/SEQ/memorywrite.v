module memorywrite (input clk,input [7:0] opcode,input [7:0] rArB,input [63:0] valA,input [63:0] valE,input [63:0] valP,output reg reset,output reg [63:0] addr,output reg [63:0] val_write,output reg wrEn,output reg reEn);

  always @(*) begin
    if ((opcode[7:4] == 4'b0100) || (opcode[7:4] == 4'b1010)) begin
      reset = 0; addr = valE; val_write = valA; wrEn = 1; reEn = 0;
    end
    else if (opcode[7:4] == 4'b0101) begin
      reset = 0; addr = valE; val_write = valA; wrEn = 0; reEn = 1;
    end
    else if (opcode[7:4] == 4'b1011) begin
      reset = 0; addr = valA; val_write = valA; wrEn = 0; reEn = 1;
    end
    else if (opcode[7:4] == 4'b1000) begin
      reset = 0; addr = valE; val_write = valP; wrEn = 1; reEn = 0;
    end
    else if (opcode[7:4] == 4'b1001) begin
      reset = 0; addr = valA; val_write = valA; wrEn = 0; reEn = 1;
    end
    else begin
      reset = 0; addr = 0; val_write = 0; wrEn = 0; reEn = 0;
    end
  end
endmodule
