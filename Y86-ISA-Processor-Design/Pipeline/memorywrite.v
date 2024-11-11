module memorywrite (input [1:0]M_status,input [3:0] M_icode,input M_Cnd,input [3:0] M_dstE,input [3:0] M_dstM,input [63:0] M_valA,input [63:0] M_valE,
output reg [1:0] m_status,output reg [3:0] m_icode,output reg [63:0] m_valE,output reg [63:0] m_valM,output reg [3:0] m_dstE,output reg [3:0] m_dstM);
   reg [63:0] mem_addr;
   reg [7:0] datamemory [4095:0];
   reg mem_read,mem_write;
   integer i;
   reg dmem_error;
   initial begin
    for(i=0;i<4095;i=i+1) begin
      datamemory[i]=0;
    end
    datamemory[200]=200;
    datamemory[208]=210;
    datamemory[216]=220;
    datamemory[224]=120;
   end
  always @(*) begin
      if ((M_icode == 4'b0100) || (M_icode == 4'b1010)|(M_icode ==4'b0101) || (M_icode ==4'b1000)) begin
       mem_addr = M_valE; 
    end
    else if((M_icode == 4'b1011)||(M_icode == 4'b1001)) begin
      mem_addr=M_valA;
    end
    else begin
      mem_addr=0;
    end

   m_valM[63:56]=datamemory[mem_addr+7]; 
      m_valM[55:48]=datamemory[mem_addr+6]; 
      m_valM[47:40]=datamemory[mem_addr+5]; 
      m_valM[39:32]=datamemory[mem_addr+4];
        m_valM[31:24]=datamemory[mem_addr+3]; 
        m_valM[23:16]=datamemory[mem_addr+2]; 
        m_valM[15:8]=datamemory[mem_addr+1]; 
        m_valM[7:0]=datamemory[mem_addr];

    if ((M_icode == 4'b0100) || (M_icode == 4'b1010)|(M_icode ==4'b1000)) begin
       mem_write =1; 
    end
    else begin
      mem_write=0;
    end

    if ((M_icode == 4'b0101) || (M_icode == 4'b1011)|(|M_icode ==4'b1001)) begin
       mem_read =1; 
    end
    else begin
      mem_read=0;
    end



    if(mem_read|mem_write) begin
      if(mem_addr>4088) begin
        dmem_error=1;
      end
      else begin
        dmem_error=0;
      end
    end
    else begin
      dmem_error=0;
    end
    
    if(dmem_error==0) begin
      m_status=M_status;

    if(mem_write) begin
      datamemory[mem_addr+7]=M_valA[63:56];datamemory[mem_addr+6]=M_valA[55:48];datamemory[mem_addr+5]=M_valA[47:40];
      datamemory[mem_addr+4]=M_valA[39:32];datamemory[mem_addr+3]=M_valA[31:24];datamemory[mem_addr+2]=M_valA[23:16];
      datamemory[mem_addr+1]=M_valA[15:8];datamemory[mem_addr]=M_valA[7:0];
     end
     m_icode=M_icode;
     m_valE=M_valE;
     m_dstE=M_dstE;
     m_dstM=M_dstM;
    end
    else begin
      m_status=2;
    end
  end

    

endmodule
