`include "twotofourdecoder.v"
module twotofourdecoder_tb;
  wire D0, D1, D2, D3;
  reg S0;
  reg S1;
  twotofourdecoder DUT(S0, S1, D0, D1, D2, D3);
  integer i;
  
  initial begin
    $dumpfile("twotofourdecoder_tb.vcd");
    $dumpvars(0, twotofourdecoder_tb);
    S0=1'b0; S1=1'b0;
    for (i = 0; i < 4; i = i + 1) begin
       #1
       {S1,S0}=i;
    end
    #1 $finish;
  end
  
endmodule
