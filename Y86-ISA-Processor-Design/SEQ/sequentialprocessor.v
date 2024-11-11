module sequentialprocessor(input clk,input reboot,output [7:0] opcode,output  [7:0] rArB,output  [63:0] valA,output  [63:0] valB,output  [63:0] valC,output  [63:0] valE,
output  [63:0] valM,output  [63:0] pc1,output [2:0] cc1,output  [1:0] status1);
 reg [63:0] pc;
  wire [63:0] valP;
  wire decodeerror;
  reg finalerror;
  wire [3:0] registernumber1_read, registernumber2_read;
  wire [3:0] registernumber1_write, registernumber2_write; 
  wire [7:0] rArB_execute;
  wire Cnd;
  wire [2:0] cc_out;
  reg [2:0] cc;
  wire mem_reset, reg_reset;
  wire [63:0] mem_addr;
  wire [63:0] mem_val_write;
  wire mem_reEn, mem_wrEn;
  wire [63:0] val_write1, val_write2;
  wire [63:0] finalval_PC;
  reg [1:0] status;
  reg reg_reEn;
  wire reg_wrEn;
  wire memerror;
  wire [1:0] status_final;
   wire [1:0] status_temp;
   wire mem_wrEn1;
   
initial begin
  cc=0;
  status=0; //initializing values 
  pc=0;
  reg_reEn=1;
end
assign reg_wrEn=(~clk)&wrEn;//registerwrite,memorywrite happnens at  negative clock edge.Rest all is triggered by posedge which trigeers fetch
assign cc1=cc; //copying values for testbench
assign pc1=pc;
assign status1=status;



  register DUT_reg (
    .clk(clk),
    .reset(reg_reset),
    .registernumber1_read(registernumber1_read),
    .registernumber2_read(registernumber2_read),
    .registernumber1_write(registernumber1_write),
    .registernumber2_write(registernumber2_write),
    .val_write1(val_write1),
    .val_write2(val_write2),
    .wrEn(reg_wrEn),
    .reEn(reg_reEn),
    .val_read1(valA),
    .val_read2(valB),
    .regerr(regerr)
  );//registerfile

  dataMem DUT_data (
    .clk(clk),
    .reset(mem_reset),
    .addr(mem_addr),
    .val_write(mem_val_write),
    .wrEn(mem_wrEn),
    .reEn(mem_reEn),
    .val_read(valM),
    .memerror(memerror)
  );//datamemory

  fetch DUT_fetch(clk,pc,valP, opcode, rArB,valC, status_final);//fetch which contains instruction memory

  decode inst_decode(opcode, rArB, valC, decodeerror, registernumber1_read, registernumber2_read);//decode

  execute inst_execute(opcode, rArB, valA, valB, valC, cc, valE, rArB_execute, Cnd, cc_out);//execute

  memorywrite inst_memorywrite(clk,opcode, rArB_execute, valA, valE, valP, mem_reset, mem_addr, mem_val_write, mem_wrEn, mem_reEn);//memorywrite

  registerwrite inst_registerwrite(opcode, rArB_execute, valE, valM, reg_reset, registernumber1_write, registernumber2_write, val_write1, val_write2,wrEn);//register write

  PCupdate inst_PCupdate(opcode, valP, valM, valC, Cnd, finalval_PC);//Pc update gievs updated PC vale for next instruction to be executed in next posedge clk

  statusupdate inst_statusupdate(decodeerror,memerror,status_final,status,status_temp);//updates status variable

always @(negedge clk) begin //During negative edge of clock cycle,it updated status based on status update,pc value from pc update and cc from cc_out of execute
  if(reboot!=1) begin
  status=status_temp;
  if(status_temp==0) begin
  pc=finalval_PC;
  cc=cc_out;
  end
  end
end


    

    
    

  

endmodule