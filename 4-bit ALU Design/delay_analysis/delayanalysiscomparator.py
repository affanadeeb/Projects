import os
import subprocess
import re
fp3 = open("output_comparator.txt",'w')
fp3.close()
command = ["ngspice destination.cir"]
search_text="V_in_A3 A3 gnd PULSE(1.8 0 0ns 1ps 1ps 10ns 20ns)\nV_in_A2 A2 gnd PULSE(0 1.8 0ns 1ps 1ps 10ns 20ns)\nV_in_A1 A1 gnd PULSE(0 1.8 0ns 1ps 1ps 10ns 20ns)\nV_in_A0 A0 gnd PULSE(1.8 0 0ns 1ps 1ps 10ns 20ns)\nV_in_B3 B3 gnd PULSE(0 1.8 0ns 1ps 1ps 20ns 40ns)\nV_in_B2 B2 gnd PULSE(0 1.8 0ns 1ps 1ps 20ns 40ns)\nV_in_B1 B1 gnd PULSE(1.8 0 0ns 1ps 1ps 20ns 40ns)\nV_in_B0 B0 gnd PULSE(1.8 0 0ns 1ps 1ps 20ns 40ns)"
replace_text="V_in_A2 A2 gnd 0\nV_in_A1 A1 gnd 0\nV_in_A0 A0 gnd 0\nV_in_B2 B2 gnd 0\nV_in_B1 B1 gnd 0\nV_in_B0 B0 gnd 0\nV_in_A3 A3 gnd PULSE(0 1.8 0ns 1ps 1ps 40ns 80ns)\nV_in_B3 B3 gnd PULSE(0 1.8 0ns 1ps 1ps 160ns 320ns)\n"
search="V_in_S1 S1 gnd 0\nV_in_S0 S0 gnd 0"
replace="V_in_S1 S1 gnd 1.8\nV_in_S0 S0 gnd 0"
for j in range(0,8):
    if j<4:
        s = "A"+str(j) 
    else:
        s="B"+str(j-4)
    for k in range(0,3):
        a="1.8"
        b="0"
        c="1.8"
        if k==0:
            out="equal"
        if k==1:
            out="greater"
            if j<4:
                c="0"
        if k==2:
            out="lesser"
            if j<4:
              a="0"
              b="1.8"
            else:
                c="0"
              
        
        fp1 = open("ALU.cir",'r') 
        fp2 =open("destination.cir",'w') 
        fp3 = open("output_comparator.txt",'a') 
        mode1 = "RISE"
        mode2 = "RISE"
        mode3 = "FALL"
        mode4 = "FALL"
        if j<4:
            s1="B"+str(j)
        else:
            s1="A"+str(j-4)
        
        search_text4=f"V_in_A3 A3 gnd PULSE(0 1.8 0ns 1ps 1ps 40ns 80ns)"
        search_text5=f"V_in_B3 B3 gnd PULSE(0 1.8 0ns 1ps 1ps 160ns 320ns)"
        replace_text4=f"V_in_{s} {s} gnd PULSE({a} {b} 0ns 1ps 1ps 40ns 80ns)"
        replace_text5=f"V_in_{s1} {s1} gnd {c}"
        search_text6=f"V_in_{s} {s} gnd 0"
        search_text7=f"V_in_{s1} {s1} gnd 0"
        replace_text6="V_in_A3 A3 gnd 0"
        replace_text7="V_in_B3 B3 gnd 0"
        
        
        data = fp1.read() 
        data=data.replace(search_text,replace_text)
        data=data.replace(search,replace)
        search_text1 = "*target text"
        if j<4:
            if k==1:
               replace_text1= f'''
    .measure tran trise 
      + TRIG v({s}) VAL = 'SUPPLY/2' {mode1} =1
      + TARG v({out}) VAL = 'SUPPLY/2' {mode2} =1 

       .measure tran tfall 
       + TRIG v({s}) VAL = 'SUPPLY/2' {mode3} =1 
      + TARG v({out}) VAL = 'SUPPLY/2' {mode4}=1

      .measure tran tpd param = '(trise + tfall)/2' goal = 0
        
        ''' 
            else:
                replace_text1= f'''
    .measure tran trise 
      + TRIG v({s}) VAL = 'SUPPLY/2' {mode1} =1
      + TARG v({out}) VAL = 'SUPPLY/2' {mode3} =1 

       .measure tran tfall 
       + TRIG v({s}) VAL = 'SUPPLY/2' {mode4} =1 
      + TARG v({out}) VAL = 'SUPPLY/2' {mode2}=1

      .measure tran tpd param = '(trise + tfall)/2' goal = 0
        
        ''' 
        else:
            if k==2:
               replace_text1= f'''
    .measure tran trise 
      + TRIG v({s}) VAL = 'SUPPLY/2' {mode1} =1
      + TARG v({out}) VAL = 'SUPPLY/2' {mode2} =1 

       .measure tran tfall 
       + TRIG v({s}) VAL = 'SUPPLY/2' {mode3} =1 
      + TARG v({out}) VAL = 'SUPPLY/2' {mode4}=1

      .measure tran tpd param = '(trise + tfall)/2' goal = 0
        
        ''' 
            else:
                replace_text1= f'''
    .measure tran trise 
      + TRIG v({s}) VAL = 'SUPPLY/2' {mode1} =1
      + TARG v({out}) VAL = 'SUPPLY/2' {mode3} =1 

       .measure tran tfall 
       + TRIG v({s}) VAL = 'SUPPLY/2' {mode4} =1 
      + TARG v({out}) VAL = 'SUPPLY/2' {mode2}=1

      .measure tran tpd param = '(trise + tfall)/2' goal = 0
        
        ''' 
           
           
        data = data.replace(search_text4,replace_text4)
        data = data.replace(search_text5,replace_text5)
        data = data.replace(search_text7,replace_text7,1)
        data = data.replace(search_text6,replace_text6,1)
        data = data.replace(search_text1,replace_text1)
        search_text3="*quit"
        replace_text3= f"quit"
        data=data.replace(search_text3,replace_text3)
        fp2.write(data) 
        fp1.close()
        fp2.close()

        
        completed_process = subprocess.run(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if completed_process.returncode == 0:
            output = completed_process.stdout
        else:
            output = ("Command execution failed. at",s)

        output = output.split('\n') 
        output = output[-4] 
        additional_text = f" for input = {s} and output={out}\n"

        output=output[23:34]
        num=float(output)
        fp3.write(output+additional_text)
        fp3.close()
                
