module statusupdate (
  input decodeerror,input memerror,input[1:0] status_final,input [1:0]status,output reg [1:0] status_out
);
  
  always @* begin
    if (status == 0) begin
      if (status_final == 0) begin
        if (decodeerror == 1) begin
          status_out = 3;
        end
        else if (memerror == 1) begin
          status_out = 2;
        end
        else begin
          status_out = status_final;
        end
      end
      else begin
        status_out = status_final;
      end
    end
  end
endmodule
