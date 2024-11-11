module Pipelinecontrllogic(input [3:0] E_icode,input [3:0] D_icode,input [3:0] M_icode,input [3:0] E_dstM,input [3:0] d_srcA,input [3:0] d_srcB,input e_Cnd,
output reg F_stall,output reg D_stall,output reg D_bubble,output reg E_bubble);
   always @(*) begin
   if((((E_icode==4'b0101)||(E_icode==4'b1011))&&((E_dstM==d_srcA)||(E_dstM==d_srcB)))||((D_icode==4'b1001)||(E_icode==4'b1001)||(M_icode==4'b1001))) begin
      F_stall=1;
   end
   else begin
    F_stall=0;
   end

   if(((E_icode==4'b0101)||(E_icode==4'b1011))&&((E_dstM==d_srcA)||(E_dstM==d_srcB)))begin
      D_stall=1;
   end
   else begin
      D_stall=0;
   end

   if(((E_icode==4'b0111)&&(!e_Cnd))||(((D_icode==4'b1001)||(E_icode==4'b1001)||(M_icode==4'b1001))&&
   !(((E_icode==4'b0101)||(E_icode==4'b1011))&&((E_dstM==d_srcA)||(E_dstM==d_srcB))))) begin
      D_bubble=1;
   end
   else begin
      D_bubble=0;
   end

   if(((E_icode==4'b0111)&&(!e_Cnd))||((E_icode==4'b0101)||(E_icode==4'b1011))&&((E_dstM==d_srcA)||(E_dstM==d_srcB))) begin
      E_bubble=1;
      
   end
   else begin
      E_bubble=0;
   end
   end
   








endmodule