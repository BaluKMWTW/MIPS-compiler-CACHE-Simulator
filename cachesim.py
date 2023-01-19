# import time
# def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
  
#     percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
#     filledLength = int(length * iteration // total)
#     bar = fill * filledLength + '-' * (length - filledLength)
#     print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
#     # Print New Line on Complete
#     if iteration == total: 
#         print()
index = 1
def twosComp(x):
    y = ''
    for i in range(16):
        if (x[i] == '0'):
            y = y + '1'
        else:
            y = y + '0'
    y_int = int(y, base=2)
    z_int = y_int + 1
    z = bin(z_int)
    z = z[2:].zfill(16)
    return z
  
def decimalToBinary(n):
    y = bin(n).replace("0b", "").zfill(16)
    if y.startswith("-"):
        y = y.replace("-", "").zfill(16)
        y = twosComp(y)
    return y
def binaryToDecimal(n):
    x = 0
    if n.startswith("1"):
        x = -1*pow(2,15)
        a = 0
        for i in range(15,0,-1):
            if n[i] == "1":
                x = x + pow(2,a)
            a += 1
    else:
        x = int(n,2)
    return x
def XOR(x,y):
  z =""
  for i in range(16):
    if x[i] != y[i]:
      z += "1"
    else:
      z += "0"
  return z

def isRtype(bin):
  rs, rt, rd, sa = bin[6:11], bin[11:16], bin[16:21], bin[21:26]
  rs = str(int(rs, base=2))
  rt = str(int(rt, base=2))
  rd = str(int(rd, base=2))
  sa = str(int(sa, base=2))

  op = bin[26:]
  if (op == "100000"):
    op = "add"
  elif (op == "100100"):
    op = "and"
  elif (op == "100010"):
    op = "sub"
  elif (op == "101010"):
    op = "slt"
  elif (op == "000010"):
    op = "srl"
  elif (op == "000000"):
    op = "sll"
  elif (op == "100110"):
    op = "xor"
  else:
    op = "broke"

  if (op == "srl" or op == "sll"):
    instr = op + " $" + rd + ", $" + rt + ", " + sa
    return instr
  else:
    instr = op + " $" + rd + ", $" + rs + ", $" + rt
    return instr


def isItype(bin):
  rs, rt, imm = bin[6:11], bin[11:16], bin[16:32]
  twos_flag = False
  if imm[0] == "1":
    imm = twosComp(imm)
    twos_flag = True

  rs = str(int(rs, base=2))
  rt = str(int(rt, base=2))
  imm = str(int(imm, base=2))
  if twos_flag:
    imm = "-" + imm
  op = bin[:6]
  if (op == '000010'):
    op = "beq"
  elif (op == '001100'):
    op = "andi"
  elif (op == '001000'):
    op = "addi"
  elif (op == '000101'):
    op = "bne"
  elif (op == '100011'):
    op = "lw"
  elif (op == '101011'):
    op = "sw"
  elif (op == '111111'):
    op = "cnt"
  elif (op == '000100'):
    op = "beq"
  if (op == "lw" or op == "sw"):
    instr = op + " $" + rt + ", " + imm + "($" + rs + ")"
  elif (op == "beq" or op == "bne"):
    instr = op + " $" + rs + ", $" + rt + ", " + imm
  else:
    instr = op + " $" + rt + ", $" + rs + ", " + imm

  return instr


# def log()
f = open("p4.mc")
lines = f.readlines()
f.close

ALUcount = 0
branchCount = 0
memoryCount = 0
otherCount = 0
totInstr = 0
pc_max = 0
pc = 0
memX = 8192
hexmemX = 8192
instr = {}
hexinstr = {}
mem_dict = {}
hexmem_dict = {}
label_dict = {}
save = 8192
saved_dict = {}
reg_dict = {
  '0': 0,
  '1': 0,
  '2': 0,
  '3': 0,
  '4': 0,
  '5': 0,
  '6': 0,
  '7': 0,
  '8': 0,
  '9': 0,
  '10': 0,
  '11': 0,
  '12': 0,
  '13': 0,
  '14': 0,
  '15': 0,
  '16': 0,
  '17': 0,
  '18': 0,
  '19': 0,
  '20': 0,
  '21': 0,
  '22': 0,
  '23': 0,
  '24': 0,
  '25': 0,
  '26': 0,
  '27': 0,
  '28': 0,
  '29': 0,
  '30': 0,
  '31': 0,
  'PC': 0
}
while (save < 8736):
  saved_dict[save] = 0
  save += 4

# mode = input("Press 'n' to finish program or 's' to go by each step\n")
s_flag = False
# if mode == "s":
#   s_flag = True
while (memX <= 8703):
  mem_dict[memX] = 0
  memX += 4

while (hexmemX <= 8703):
  x = hex(hexmemX)
  hexmem_dict[x] = 0
  hexmemX += 4
commands = {}
for i, x in enumerate(lines):
  x.replace("\n", "")
  code_bin = bin(int(x, 16))[2:].zfill(32)
  instr[pc_max] = code_bin
  commands[pc_max] = x
  pc_max += 4
#print(commands)
i = 0
config = input("Select prefered cache configuration\n1 - a DM cache with 8 sets, block size of 64 Bytes\n2 - a DM cache with 4 sets, block size of 32 Bytes\n3 - a 4-way FA cache, block size of 32 Bytes\n4 - a 4-way SA cache with 2 sets, block size of 64 Bytes\n")
print("config =",config)
hit = 0
miss = 0
open('log.txt', 'w').close()
if config == "1":
  cache_dict = {'set0': {'w1': 0},
                'set1': {'w1': 0},
                'set2': {'w1': 0},
                'set3': {'w1': 0},
                'set4': {'w1': 0},
                'set5': {'w1': 0},
                'set6': {'w1': 0},
                'set7': {'w1': 0}}
  
  while pc < pc_max:
    if s_flag:
      next = input("\nPress enter for next step or n to skip\n")
      if next == "n":
        s_flag = False
    #R-type
    if instr[pc][0:6] == "000000":
      rs = instr[pc][6:11]
      rt = instr[pc][11:16]
      rd = instr[pc][16:21]
      sh = instr[pc][21:27]
      rs = str(int(rs, base=2))
      rt = str(int(rt, base=2))
      rd = str(int(rd, base=2))
      sh = str(int(sh, base=2))
  
      instr_text = isRtype(instr[pc])
      #print(instr_text)
      # add
      if instr_text[0:3] == "add":
        reg_dict[rd] = reg_dict[rs] + reg_dict[rt]
        pc += 4
        ALUcount += 1
      if instr_text[0:3] == "sub":
        reg_dict[rd] = reg_dict[rs] - reg_dict[rt]
        pc += 4
        ALUcount += 1
      # and
      if instr_text[0:3] == "and":
        reg_dict[rd] = reg_dict[rs] & reg_dict[rt]
        pc += 4
        ALUcount += 1
      # slt
      if instr_text[0:3] == "slt":
        pc += 4
        if reg_dict[rs] < reg_dict[rt]:
          reg_dict[rd] = 1
        else:
          reg_dict[rd] = 0
        otherCount += 1
      # slr
      if instr_text[0:3] == "srl":
        ALUcount += 1
        pc += 4
        if reg_dict[rt] < 0:
          #ALUcount += 1
          reg_dict[rt] = (reg_dict[rt]) & 0xffffffff
        if reg_dict[rt] == 1:
          reg_dict[rt] = 0
        reg_dict[rd] = int(int(reg_dict[rt]) / int(sh))
      #XOR
      if instr_text[0:3] == "xor":
        pc += 4
        #reg_dict[rd] = reg_dict[rs] ^ reg_dict[rt]
        rs_binary = decimalToBinary(reg_dict[rs])
        rt_binary = decimalToBinary(reg_dict[rt])
        rd_binary = XOR(rs_binary, rt_binary)
        reg_dict[rd] = binaryToDecimal(rd_binary)
  
      if s_flag:
        print(instr_text)
        print("hex: ", commands[pc - 4], sep='')
        print("PC: ", pc - 4, sep='')
        print("rd $", rd, ": ", reg_dict[rd])
        print("rs $", rs, ": ", reg_dict[rs])
        print("rt $", rt, ": ", reg_dict[rt])
  
    #I-type
    else:
      instr_text = isItype(instr[pc])
      totInstr += 1
      #print(instr_text)
      rs = instr[pc][6:11]
      rt = instr[pc][11:16]
      imm_b = instr[pc][16:]
      rs = str(int(rs, base=2))
      rt = str(int(rt, base=2))
      imm = int(imm_b, base=2)
      #addi
      if instr[pc][0:6] == "001000":
        pc += 4
        if imm_b[0] == "1":  # if negative, perform 2s complement
          #print("imm_b = ", imm_b)
          imm = twosComp(str(imm_b))
          #print("imm =", -int(imm, base=2))
          reg_dict[rt] = (reg_dict[rs] - int(imm, base=2))
        else:
          reg_dict[rt] = (reg_dict[rs] + imm)
        ALUcount += 1
      #bne
      elif instr[pc][0:6] == "000101":
        pc += 4
        if reg_dict[rs] != reg_dict[rt]:
          #imm = int(instr_text[11:])
          new = instr_text.split(',')
          imm = int(new[2])
          pc += (imm * 4)
        branchCount += 1
      #beq
      elif instr[pc][0:6] == "000100":
        pc += 4
        if (reg_dict[rs] == reg_dict[rt]):
  
          #imm = int(instr_text[11:])
          new = instr_text.split(',')
          imm = int(new[2])
          pc += (imm * 4)
        branchCount += 1
      #andi
      elif instr[pc][0:6] == "001100":
        pc += 4
        reg_dict[rt] = (reg_dict[rs] & imm)
        ALUcount += 1
      #lw
      elif instr[pc][0:6] == "100011":
        reg_dict[rt] = saved_dict[reg_dict[rs] + imm]
        memoryCount += 1
        print("\n")
        #print("instr[pc] = ", instr[pc])
        cmd = str(bin(reg_dict[rs] + imm)[2:]).zfill(32)
        #print("cmd =", cmd)
        tag = cmd[0:23]
        set = cmd[23:26]
        offset = cmd[26:]
        f = open("log.txt", "a")
        f.write("(")
        f.write(str(index))
        f.write(") ")
        f.write("addres: ")
        f.write(hex(int(instr[pc], 2)))
        f.write("\n")
        f.write("tag =")
        f.write(hex(int(tag)))
        f.write("\n")
        f.write("set = ")
        f.write(set)
        f.write("\n")
        f.write("offset =")
        f.write(offset)
        f.write("\n")
        index += 1
        set = "set" + str(int(set,2))
        if (cache_dict[set]["w1"] != tag):
              cache_dict[set]["w1"] = tag
              miss = miss + 1
              f.write("MISS\n\n")
        elif (cache_dict[set]["w1"] == tag):
              hit = hit + 1
              f.write("HIT!\n\n")
        pc += 4
      #sw
      elif instr[pc][0:6] == "101011":
        saved_dict[reg_dict[rs] + imm] = reg_dict[rt]
        memoryCount += 1
        print("\n")
        cmd = str(bin(reg_dict[rs] + imm)[2:]).zfill(32)
        print("cmd =", cmd)
        tag = cmd[0:23]
        set = cmd[23:26]
        offset = cmd[26:]
        f = open("log.txt", "a")
        f.write("(")
        f.write(str(index))
        f.write(") ")
        f.write("addres: ")
        f.write(hex(int(instr[pc], 2)))
        f.write("\n")
        f.write("tag =")
        f.write(hex(int(tag)))
        f.write("\n")
        f.write("set = ")
        f.write(set)
        f.write("\n")
        f.write("offset =")
        f.write(offset)
        f.write("\n")
        index += 1
        set = "set" + str(int(set,2))
        if (cache_dict[set]["w1"] != tag):
              cache_dict[set]["w1"] = tag
              miss = miss + 1
              f.write("MISS\n\n")
        elif (cache_dict[set]["w1"] == tag):
              hit = hit + 1
              f.write("HIT!\n\n")
        pc += 4
      elif instr[pc][0:6] == "111111":
        pc += 4
        parity = 0
        if reg_dict['5'] < 0:
          reg_dict['5'] += 2**32
        while reg_dict['5'] != 0:
          y = reg_dict['5'] % 2
          parity += y
          z = int(reg_dict['5'] / 2)
          reg_dict['5'] = z
        reg_dict['3'] = parity
        #count = getParity()
        ALUcount += 1
      if s_flag:
        print(instr_text)
        print("hex: ", commands[pc - 4], sep='')
        print("PC: ", pc - 4, sep='')
        print("rs $", rs, ": ", reg_dict[rs], sep='')
        print("rt $", rt, ": ", reg_dict[rt], sep='')
        print("sh $", rt, sep='')
        print("imm: ", imm, sep='')
    reg_dict['32'] = pc

elif config == "2":
  cache_dict = {'set0': {'w1': 0},
                'set1': {'w1': 0},
                'set2': {'w1': 0},
                'set3': {'w1': 0}}
  
  while pc < pc_max:
    if s_flag:
      next = input("\nPress enter for next step or n to skip\n")
      if next == "n":
        s_flag = False
    #R-type
    if instr[pc][0:6] == "000000":
      rs = instr[pc][6:11]
      rt = instr[pc][11:16]
      rd = instr[pc][16:21]
      sh = instr[pc][21:27]
      rs = str(int(rs, base=2))
      rt = str(int(rt, base=2))
      rd = str(int(rd, base=2))
      sh = str(int(sh, base=2))
  
      instr_text = isRtype(instr[pc])
      #print(instr_text)
      # add
      if instr_text[0:3] == "add":
        reg_dict[rd] = reg_dict[rs] + reg_dict[rt]
        pc += 4
        ALUcount += 1
      if instr_text[0:3] == "sub":
        reg_dict[rd] = reg_dict[rs] - reg_dict[rt]
        pc += 4
        ALUcount += 1
      # and
      if instr_text[0:3] == "and":
        reg_dict[rd] = reg_dict[rs] & reg_dict[rt]
        pc += 4
        ALUcount += 1
      # slt
      if instr_text[0:3] == "slt":
        pc += 4
        if reg_dict[rs] < reg_dict[rt]:
          reg_dict[rd] = 1
        else:
          reg_dict[rd] = 0
        otherCount += 1
      # slr
      if instr_text[0:3] == "srl":
        ALUcount += 1
        pc += 4
        if reg_dict[rt] < 0:
          #ALUcount += 1
          reg_dict[rt] = (reg_dict[rt]) & 0xffffffff
        if reg_dict[rt] == 1:
          reg_dict[rt] = 0
        reg_dict[rd] = int(int(reg_dict[rt]) / int(sh))
      #XOR
      if instr_text[0:3] == "xor":
        pc += 4
        #reg_dict[rd] = reg_dict[rs] ^ reg_dict[rt]
        rs_binary = decimalToBinary(reg_dict[rs])
        rt_binary = decimalToBinary(reg_dict[rt])
        rd_binary = XOR(rs_binary, rt_binary)
        reg_dict[rd] = binaryToDecimal(rd_binary)
  
      if s_flag:
        print(instr_text)
        print("hex: ", commands[pc - 4], sep='')
        print("PC: ", pc - 4, sep='')
        print("rd $", rd, ": ", reg_dict[rd])
        print("rs $", rs, ": ", reg_dict[rs])
        print("rt $", rt, ": ", reg_dict[rt])
  
    #I-type
    else:
      instr_text = isItype(instr[pc])
      totInstr += 1
      #print(instr_text)
      rs = instr[pc][6:11]
      rt = instr[pc][11:16]
      imm_b = instr[pc][16:]
      rs = str(int(rs, base=2))
      rt = str(int(rt, base=2))
      imm = int(imm_b, base=2)
      #addi
      if instr[pc][0:6] == "001000":
        pc += 4
        if imm_b[0] == "1":  # if negative, perform 2s complement
          #print("imm_b = ", imm_b)
          imm = twosComp(str(imm_b))
          #print("imm =", -int(imm, base=2))
          reg_dict[rt] = (reg_dict[rs] - int(imm, base=2))
        else:
          reg_dict[rt] = (reg_dict[rs] + imm)
        ALUcount += 1
      #bne
      elif instr[pc][0:6] == "000101":
        pc += 4
        if reg_dict[rs] != reg_dict[rt]:
          #imm = int(instr_text[11:])
          new = instr_text.split(',')
          imm = int(new[2])
          pc += (imm * 4)
        branchCount += 1
      #beq
      elif instr[pc][0:6] == "000100":
        pc += 4
        if (reg_dict[rs] == reg_dict[rt]):
  
          #imm = int(instr_text[11:])
          new = instr_text.split(',')
          imm = int(new[2])
          pc += (imm * 4)
        branchCount += 1
      #andi
      elif instr[pc][0:6] == "001100":
        pc += 4
        reg_dict[rt] = (reg_dict[rs] & imm)
        ALUcount += 1
      #lw
      elif instr[pc][0:6] == "100011":
        reg_dict[rt] = saved_dict[reg_dict[rs] + imm]
        memoryCount += 1
        print("\n")
        #print("instr[pc] = ", instr[pc])
        cmd = str(bin(reg_dict[rs] + imm)[2:]).zfill(32)
        #print("cmd =", cmd)
        tag = cmd[0:25]
        set = cmd[25:27]
        offset = cmd[27:]
        f = open("log.txt", "a")
        f.write("(")
        f.write(str(index))
        f.write(") ")
        f.write("addres: ")
        f.write(hex(int(instr[pc], 2)))
        f.write("\n")
        f.write("tag =")
        f.write(hex(int(tag)))
        f.write("\n")
        f.write("set = ")
        f.write(set)
        f.write("\n")
        f.write("offset =")
        f.write(offset)
        f.write("\n")
        index += 1
        set = "set" + str(int(set,2))
        if (cache_dict[set]["w1"] != tag):
              cache_dict[set]["w1"] = tag
              miss = miss + 1
              f.write("MISS\n\n")
        elif (cache_dict[set]["w1"] == tag):
              hit = hit + 1
              f.write("HIT!\n\n")
        pc += 4
      #sw
      elif instr[pc][0:6] == "101011":
        saved_dict[reg_dict[rs] + imm] = reg_dict[rt]
        memoryCount += 1
        print("\n")
        cmd = str(bin(reg_dict[rs] + imm)[2:]).zfill(32)
        print("cmd =", cmd)
        tag = cmd[0:25]
        set = cmd[25:27]
        offset = cmd[27:]
        f = open("log.txt", "a")
        f.write("(")
        f.write(str(index))
        f.write(") ")
        f.write("addres: ")
        f.write(hex(int(instr[pc], 2)))
        f.write("\n")
        f.write("tag =")
        f.write(hex(int(tag)))
        f.write("\n")
        f.write("set = ")
        f.write(set)
        f.write("\n")
        f.write("offset =")
        f.write(offset)
        f.write("\n")
        index += 1
        set = "set" + str(int(set,2))
        if (cache_dict[set]["w1"] != tag):
              cache_dict[set]["w1"] = tag
              miss = miss + 1
              f.write("MISS\n\n")
        elif (cache_dict[set]["w1"] == tag):
              hit = hit + 1
              f.write("HIT!\n\n")
        pc += 4
      elif instr[pc][0:6] == "111111":
        pc += 4
        parity = 0
        if reg_dict['5'] < 0:
          reg_dict['5'] += 2**32
        while reg_dict['5'] != 0:
          y = reg_dict['5'] % 2
          parity += y
          z = int(reg_dict['5'] / 2)
          reg_dict['5'] = z
        reg_dict['3'] = parity
        #count = getParity()
        ALUcount += 1
      if s_flag:
        print(instr_text)
        print("hex: ", commands[pc - 4], sep='')
        print("PC: ", pc - 4, sep='')
        print("rs $", rs, ": ", reg_dict[rs], sep='')
        print("rt $", rt, ": ", reg_dict[rt], sep='')
        print("sh $", rt, sep='')
        print("imm: ", imm, sep='')
    reg_dict['32'] = pc
elif config == "3":
  cache_dict = {'set0': {'w1': 0, 'w2': 0, 'w3': 0, 'w4': 0}}
  cache_cnt_dict = {'w1':0, 'w2':0,'w3':0,'w4':0,}
  casheCnt = 1
  while pc < pc_max:
    if s_flag:
      next = input("\nPress enter for next step or n to skip\n")
      if next == "n":
        s_flag = False
    #R-type
    if instr[pc][0:6] == "000000":
      rs = instr[pc][6:11]
      rt = instr[pc][11:16]
      rd = instr[pc][16:21]
      sh = instr[pc][21:27]
      rs = str(int(rs, base=2))
      rt = str(int(rt, base=2))
      rd = str(int(rd, base=2))
      sh = str(int(sh, base=2))
  
      instr_text = isRtype(instr[pc])
      #print(instr_text)
      # add
      if instr_text[0:3] == "add":
        reg_dict[rd] = reg_dict[rs] + reg_dict[rt]
        pc += 4
        ALUcount += 1
      if instr_text[0:3] == "sub":
        reg_dict[rd] = reg_dict[rs] - reg_dict[rt]
        pc += 4
        ALUcount += 1
      # and
      if instr_text[0:3] == "and":
        reg_dict[rd] = reg_dict[rs] & reg_dict[rt]
        pc += 4
        ALUcount += 1
      # slt
      if instr_text[0:3] == "slt":
        pc += 4
        if reg_dict[rs] < reg_dict[rt]:
          reg_dict[rd] = 1
        else:
          reg_dict[rd] = 0
        otherCount += 1
      # slr
      if instr_text[0:3] == "srl":
        ALUcount += 1
        pc += 4
        if reg_dict[rt] < 0:
          #ALUcount += 1
          reg_dict[rt] = (reg_dict[rt]) & 0xffffffff
        if reg_dict[rt] == 1:
          reg_dict[rt] = 0
        reg_dict[rd] = int(int(reg_dict[rt]) / int(sh))
      #XOR
      if instr_text[0:3] == "xor":
        pc += 4
        #reg_dict[rd] = reg_dict[rs] ^ reg_dict[rt]
        rs_binary = decimalToBinary(reg_dict[rs])
        rt_binary = decimalToBinary(reg_dict[rt])
        rd_binary = XOR(rs_binary, rt_binary)
        reg_dict[rd] = binaryToDecimal(rd_binary)
  
      if s_flag:
        print(instr_text)
        print("hex: ", commands[pc - 4], sep='')
        print("PC: ", pc - 4, sep='')
        print("rd $", rd, ": ", reg_dict[rd])
        print("rs $", rs, ": ", reg_dict[rs])
        print("rt $", rt, ": ", reg_dict[rt])
  
    #I-type
    else:
      instr_text = isItype(instr[pc])
      totInstr += 1
      #print(instr_text)
      rs = instr[pc][6:11]
      rt = instr[pc][11:16]
      imm_b = instr[pc][16:]
      rs = str(int(rs, base=2))
      rt = str(int(rt, base=2))
      imm = int(imm_b, base=2)
      #addi
      if instr[pc][0:6] == "001000":
        pc += 4
        if imm_b[0] == "1":  # if negative, perform 2s complement
          #print("imm_b = ", imm_b)
          imm = twosComp(str(imm_b))
          #print("imm =", -int(imm, base=2))
          reg_dict[rt] = (reg_dict[rs] - int(imm, base=2))
        else:
          reg_dict[rt] = (reg_dict[rs] + imm)
        ALUcount += 1
      #bne
      elif instr[pc][0:6] == "000101":
        pc += 4
        if reg_dict[rs] != reg_dict[rt]:
          #imm = int(instr_text[11:])
          new = instr_text.split(',')
          imm = int(new[2])
          pc += (imm * 4)
        branchCount += 1
      #beq
      elif instr[pc][0:6] == "000100":
        pc += 4
        if (reg_dict[rs] == reg_dict[rt]):
  
          #imm = int(instr_text[11:])
          new = instr_text.split(',')
          imm = int(new[2])
          pc += (imm * 4)
        branchCount += 1
      #andi
      elif instr[pc][0:6] == "001100":
        pc += 4
        reg_dict[rt] = (reg_dict[rs] & imm)
        ALUcount += 1
      #lw
      elif instr[pc][0:6] == "100011":
        reg_dict[rt] = saved_dict[reg_dict[rs] + imm]
        memoryCount += 1
        print("\n")
        #print("instr[pc] = ", instr[pc])
        cmd = str(bin(reg_dict[rs] + imm)[2:]).zfill(32)
        #print("cmd =", cmd)
        tag = cmd[0:27]
        offset = cmd[27:]
        f = open("log.txt", "a")
        f.write("(")
        f.write(str(index))
        f.write(") ")
        f.write("addres: ")
        f.write(hex(int(instr[pc], 2)))
        f.write("\n")
        f.write("tag =")
        f.write(hex(int(tag)))
        f.write("\n")
        f.write("offset =")
        f.write(offset)
        f.write("\n")
        index += 1
        #print("set ="set)
        set = "set0" #+ str(int(set,2))
        #if its a hit:
        if (cache_dict[set]["w1"] == tag):
              cache_cnt_dict["w1"] = casheCnt
              casheCnt = casheCnt + 1
              hit = hit + 1
              f.write("HIT!\n\n")
        elif (cache_dict[set]["w2"] == tag):
              cache_cnt_dict["w2"] = casheCnt
              casheCnt = casheCnt + 1
              hit = hit + 1
              f.write("HIT!\n\n")
        elif (cache_dict[set]["w3"] == tag):
              cache_cnt_dict["w3"] = casheCnt
              casheCnt = casheCnt + 1
              hit = hit + 1
              f.write("HIT!\n\n")
        elif (cache_dict[set]["w4"] == tag):
              cache_cnt_dict["w4"] = casheCnt
              casheCnt = casheCnt + 1
              hit = hit + 1
              f.write("HIT!\n\n")
        #if its a miss:
        if ((cache_dict[set]["w1"] != tag) and
            (cache_dict[set]["w2"] != tag) and 
			      (cache_dict[set]["w3"] != tag) and 
            (cache_dict[set]["w4"] != tag)):
              
          #first check to see if any way is open
          if (cache_dict[set]["w1"] == 0):
            cache_dict[set]["w1"] = tag
            cache_cnt_dict["w1"] = casheCnt
            casheCnt = casheCnt + 1
            miss = miss + 1
            f.write("MISS\n\n")
            
          elif (cache_dict[set]["w2"] == 0):
            cache_dict[set]["w2"] = tag
            cache_cnt_dict["w2"] = casheCnt
            casheCnt = casheCnt + 1
            miss = miss + 1
            f.write("MISS\n\n")

          elif (cache_dict[set]["w3"] == 0):
            cache_dict[set]["w3"] = tag
            cache_cnt_dict["w3"] = casheCnt
            casheCnt = casheCnt + 1
            miss = miss + 1
            f.write("MISS\n\n")

          elif (cache_dict[set]["w4"] == 0):
            cache_dict[set]["w4"] = tag
            cache_cnt_dict["w4"] = casheCnt
            casheCnt = casheCnt + 1
            miss = miss + 1
            f.write("MISS\n\n")

          else:
            key_min = min(cache_cnt_dict.keys(), key = (lambda k: cache_cnt_dict[k]))
            way = key_min[0:2]
            cache_dict[set][way] = tag
            cache_cnt_dict[key_min] = casheCnt
            miss = miss + 1
            casheCnt = casheCnt + 1
            f.write("MISS\n\n")
        pc += 4
      #sw
      elif instr[pc][0:6] == "101011":
        saved_dict[reg_dict[rs] + imm] = reg_dict[rt]
        memoryCount += 1
        print("\n")
        cmd = str(bin(reg_dict[rs] + imm)[2:]).zfill(32)
        #print("cmd =", cmd)
        tag = cmd[0:27]
        offset = cmd[27:]
        f = open("log.txt", "a")
        f.write("(")
        f.write(str(index))
        f.write(") ")
        f.write("addres: ")
        f.write(hex(int(instr[pc], 2)))
        f.write("\n")
        f.write("tag =")
        f.write(hex(int(tag)))
        f.write("\n")
        f.write("offset =")
        f.write(offset)
        f.write("\n")
        index += 1
        set = "set0" #+ str(int(set,2))
        #if its a hit:
        if (cache_dict[set]["w1"] == tag):
              cache_cnt_dict["w1"] = casheCnt
              casheCnt = casheCnt + 1
              hit = hit + 1
              f.write("HIT!\n\n")
          
        elif (cache_dict[set]["w2"] == tag):
              cache_cnt_dict["w2"] = casheCnt
              casheCnt = casheCnt + 1
              hit = hit + 1
              f.write("HIT!\n\n")
          
        elif (cache_dict[set]["w3"] == tag):
              cache_cnt_dict["w3"] = casheCnt
              casheCnt = casheCnt + 1
              hit = hit + 1
              f.write("HIT!\n\n")
          
        elif (cache_dict[set]["w4"] == tag):
              cache_cnt_dict["w4"] = casheCnt
              casheCnt = casheCnt + 1
              hit = hit + 1
              f.write("HIT!\n\n")
          
        #if its a miss:
        if ((cache_dict[set]["w1"] != tag) and
            (cache_dict[set]["w2"] != tag) and 
			      (cache_dict[set]["w3"] != tag) and 
            (cache_dict[set]["w4"] != tag)):
              
          #first check to see if any way is open
          if (cache_dict[set]["w1"] == 0):
            cache_dict[set]["w1"] = tag
            cache_cnt_dict["w1"] = casheCnt
            casheCnt = casheCnt + 1
            miss = miss + 1
            f.write("MISS\n\n")
            
          elif (cache_dict[set]["w2"] == 0):
            cache_dict[set]["w2"] = tag
            cache_cnt_dict["w2"] = casheCnt
            casheCnt = casheCnt + 1
            miss = miss + 1
            f.write("MISS\n\n")

          elif (cache_dict[set]["w3"] == 0):
            cache_dict[set]["w3"] = tag
            cache_cnt_dict["w3"] = casheCnt
            casheCnt = casheCnt + 1
            miss = miss + 1
            f.write("MISS\n\n")

          elif (cache_dict[set]["w4"] == 0):
            cache_dict[set]["w4"] = tag
            cache_cnt_dict["w4"] = casheCnt
            casheCnt = casheCnt + 1
            miss = miss + 1
            f.write("MISS\n\n")

          else:
            key_min = min(cache_cnt_dict.keys(), key = (lambda k: cache_cnt_dict[k]))
            way = key_min[0:2]
            cache_dict[set][way] = tag
            cache_cnt_dict[key_min] = casheCnt
            miss = miss + 1
            casheCnt = casheCnt + 1
            f.write("MISS\n\n")
        pc += 4
      elif instr[pc][0:6] == "111111":
        pc += 4
        parity = 0
        if reg_dict['5'] < 0:
          reg_dict['5'] += 2**32
        while reg_dict['5'] != 0:
          y = reg_dict['5'] % 2
          parity += y
          z = int(reg_dict['5'] / 2)
          reg_dict['5'] = z
        reg_dict['3'] = parity
        #count = getParity()
        ALUcount += 1
      if s_flag:
        print(instr_text)
        print("hex: ", commands[pc - 4], sep='')
        print("PC: ", pc - 4, sep='')
        print("rs $", rs, ": ", reg_dict[rs], sep='')
        print("rt $", rt, ": ", reg_dict[rt], sep='')
        print("sh $", rt, sep='')
        print("imm: ", imm, sep='')
    reg_dict['32'] = pc
elif config == "4":
  cache_dict = {'set0': {'w1': 0, 'w2': 0, 'w3': 0, 'w4': 0},
                 'set1': {'w1': 0, 'w2': 0, 'w3': 0, 'w4': 0} }
  
  cache_cnt_dict= {'set0': {'w1s0':0, 'w2s0':0,'w3s0':0,'w4s0':0},
                   'set1':{'w1s1':0, 'w2s1':0,'w3s1':0,'w4s1':0} }
  casheCnt = 1
  casheCnt2 = 1
  while pc < pc_max:
    if s_flag:
      next = input("\nPress enter for next step or n to skip\n")
      if next == "n":
        s_flag = False
    #R-type
    if instr[pc][0:6] == "000000":
      rs = instr[pc][6:11]
      rt = instr[pc][11:16]
      rd = instr[pc][16:21]
      sh = instr[pc][21:27]
      rs = str(int(rs, base=2))
      rt = str(int(rt, base=2))
      rd = str(int(rd, base=2))
      sh = str(int(sh, base=2))
  
      instr_text = isRtype(instr[pc])
      #print(instr_text)
      # add
      if instr_text[0:3] == "add":
        reg_dict[rd] = reg_dict[rs] + reg_dict[rt]
        pc += 4
        ALUcount += 1
      if instr_text[0:3] == "sub":
        reg_dict[rd] = reg_dict[rs] - reg_dict[rt]
        pc += 4
        ALUcount += 1
      # and
      if instr_text[0:3] == "and":
        reg_dict[rd] = reg_dict[rs] & reg_dict[rt]
        pc += 4
        ALUcount += 1
      # slt
      if instr_text[0:3] == "slt":
        pc += 4
        if reg_dict[rs] < reg_dict[rt]:
          reg_dict[rd] = 1
        else:
          reg_dict[rd] = 0
        otherCount += 1
      # slr
      if instr_text[0:3] == "srl":
        ALUcount += 1
        pc += 4
        if reg_dict[rt] < 0:
          #ALUcount += 1
          reg_dict[rt] = (reg_dict[rt]) & 0xffffffff
        if reg_dict[rt] == 1:
          reg_dict[rt] = 0
        reg_dict[rd] = int(int(reg_dict[rt]) / int(sh))
      #XOR
      if instr_text[0:3] == "xor":
        pc += 4
        #reg_dict[rd] = reg_dict[rs] ^ reg_dict[rt]
        rs_binary = decimalToBinary(reg_dict[rs])
        rt_binary = decimalToBinary(reg_dict[rt])
        rd_binary = XOR(rs_binary, rt_binary)
        reg_dict[rd] = binaryToDecimal(rd_binary)
  
      if s_flag:
        print(instr_text)
        print("hex: ", commands[pc - 4], sep='')
        print("PC: ", pc - 4, sep='')
        print("rd $", rd, ": ", reg_dict[rd])
        print("rs $", rs, ": ", reg_dict[rs])
        print("rt $", rt, ": ", reg_dict[rt])
  
    #I-type
    else:
      instr_text = isItype(instr[pc])
      totInstr += 1
      #print(instr_text)
      rs = instr[pc][6:11]
      rt = instr[pc][11:16]
      imm_b = instr[pc][16:]
      rs = str(int(rs, base=2))
      rt = str(int(rt, base=2))
      imm = int(imm_b, base=2)
      #addi
      if instr[pc][0:6] == "001000":
        pc += 4
        if imm_b[0] == "1":  # if negative, perform 2s complement
          #print("imm_b = ", imm_b)
          imm = twosComp(str(imm_b))
          #print("imm =", -int(imm, base=2))
          reg_dict[rt] = (reg_dict[rs] - int(imm, base=2))
        else:
          reg_dict[rt] = (reg_dict[rs] + imm)
        ALUcount += 1
      #bne
      elif instr[pc][0:6] == "000101":
        pc += 4
        if reg_dict[rs] != reg_dict[rt]:
          #imm = int(instr_text[11:])
          new = instr_text.split(',')
          imm = int(new[2])
          pc += (imm * 4)
        branchCount += 1
      #beq
      elif instr[pc][0:6] == "000100":
        pc += 4
        if (reg_dict[rs] == reg_dict[rt]):
  
          #imm = int(instr_text[11:])
          new = instr_text.split(',')
          imm = int(new[2])
          pc += (imm * 4)
        branchCount += 1
      #andi
      elif instr[pc][0:6] == "001100":
        pc += 4
        reg_dict[rt] = (reg_dict[rs] & imm)
        ALUcount += 1
      #lw
      elif instr[pc][0:6] == "100011":
        reg_dict[rt] = saved_dict[reg_dict[rs] + imm]
        memoryCount += 1
        print("\n")
        #print("instr[pc] = ", instr[pc])
        cmd = str(bin(reg_dict[rs] + imm)[2:]).zfill(32)
        #print("cmd =", cmd)
        tag = cmd[0:25]
        set = cmd[25:26]
        offset = cmd[26:]
        f = open("log.txt", "a")
        f.write("(")
        f.write(str(index))
        f.write(") ")
        f.write("addres: ")
        f.write(hex(int(instr[pc], 2)))
        f.write("\n")
        f.write("tag =")
        f.write(hex(int(tag)))
        f.write("\n")
        f.write("set = ")
        f.write(set)
        f.write("\n")
        f.write("offset =")
        f.write(offset)
        f.write("\n")
        index += 1
        #print("set ="set)
        set = "set" + str(int(set,2))
        #if its a hit:
        if (cache_dict[set]["w1"] == tag):
          if (set == 'set0'):
            cache_cnt_dict[set]["w1s0"] = casheCnt
            hit = hit + 1
            casheCnt2 = casheCnt + 1
            f.write("HIT!\n\n") 
          elif(set == 'set1'):
            way = 'w1s1'
            cache_cnt_dict[set]["w1s1"] = casheCnt
            hit = hit + 1
            casheCnt2 = casheCnt + 1
            f.write("HIT!\n\n")
            
        elif (cache_dict[set]["w2"] == tag):
          if (set == 'set0'):
            cache_cnt_dict[set]["w2s0"] = casheCnt
            hit = hit + 1
            casheCnt2 = casheCnt + 1
            f.write("HIT!\n\n")
          elif(set == 'set1'):
            way = 'w1s1'
            cache_cnt_dict[set]["w2s1"] = casheCnt
            hit = hit + 1
            casheCnt2 = casheCnt + 1
            f.write("HIT!\n\n")
            
        elif (cache_dict[set]["w3"] == tag):
          if (set == 'set0'):
            cache_cnt_dict[set]["w3s0"] = casheCnt
            hit = hit + 1
            casheCnt2 = casheCnt + 1
            f.write("HIT!\n\n")
          elif(set == 'set1'):
            cache_cnt_dict[set]["w3s1"] = casheCnt
            hit = hit + 1
            casheCnt2 = casheCnt + 1
            f.write("HIT!\n\n")
            
        elif (cache_dict[set]["w4"] == tag):
          if (set == 'set0'):
            cache_cnt_dict[set]["w4s0"] = casheCnt
            hit = hit + 1
            casheCnt2 = casheCnt + 1
            f.write("HIT!\n\n")
          elif(set == 'set1'):
            cache_cnt_dict[set]["w4s1"] = casheCnt
            hit = hit + 1
            casheCnt2 = casheCnt + 1
            f.write("HIT!\n\n")
        #if its a miss:
        if ((cache_dict[set]["w1"] != tag) and
            (cache_dict[set]["w2"] != tag) and 
			      (cache_dict[set]["w3"] != tag) and 
            (cache_dict[set]["w4"] != tag)):
              
          #first check to see if any way is open
          if(cache_dict[set]["w1"] == 0):
            cache_dict[set]["w1"] = tag
            if(set == 'set0'):
              cache_cnt_dict[set]["w1s0"] = casheCnt
              casheCnt = casheCnt + 1
              miss = miss + 1
              f.write("MISS\n\n")
            elif (set == 'set1'):
              cache_cnt_dict[set]["w1s1"] = casheCnt2
              casheCnt2 = casheCnt2 + 1
              miss = miss + 1
              f.write("MISS\n\n")
            
          elif(cache_dict[set]["w2"] == 0):
            cache_dict[set]["w2"] = tag
            if(set == 'set0'):
              cache_cnt_dict[set]["w2s0"] = casheCnt
              casheCnt = casheCnt + 1
              miss = miss + 1
              f.write("MISS\n\n")
            elif (set == 'set1'):
              cache_cnt_dict[set]["w2s1"] = casheCnt2
              casheCnt2 = casheCnt2 + 1
              miss = miss + 1
              f.write("MISS\n\n")

          elif(cache_dict[set]["w3"] == 0):
            cache_dict[set]["w3"] = tag
            if(set == 'set0'):
              cache_cnt_dict[set]["w3s0"] = casheCnt
              casheCnt = casheCnt + 1
              miss = miss + 1
              f.write("MISS\n\n")
            elif (set == 'set1'):
              cache_cnt_dict[set]["w3s1"] = casheCnt2
              casheCnt2 = casheCnt2 + 1
              miss = miss + 1
              f.write("MISS\n\n")

          elif(cache_dict[set]["w4"] == 0):
            cache_dict[set]["w4"] = tag
            if(set == 'set0'):
              cache_cnt_dict[set]["w4s0"] = casheCnt
              casheCnt = casheCnt + 1
              miss = miss + 1
              f.write("MISS\n\n")
            elif (set == 'set1'):
              cache_cnt_dict[set]["w4s1"] = casheCnt2
              casheCnt2 = casheCnt2 + 1
              miss = miss + 1
              f.write("MISS\n\n")

          else:
            key_min = min(cache_cnt_dict[set].keys(), key = (lambda k: cache_cnt_dict[set][k]))
            way = key_min[0:2]
            cache_dict[set][way] = tag
            cntSet = key_min[3:]
            cntSet =  "set" + cntSet
            if (cntSet == 'set0'):
              cache_cnt_dict[cntSet][key_min] = casheCnt
              casheCnt = casheCnt + 1 
              miss = miss + 1
              f.write("MISS\n\n")
            elif (cntSet == 'set1'):
              cache_cnt_dict[cntSet][key_min] = casheCnt2
              casheCnt2 = casheCnt2 + 1 
              miss = miss + 1
              f.write("MISS\n\n")
        pc += 4
      #sw
      elif instr[pc][0:6] == "101011":
        saved_dict[reg_dict[rs] + imm] = reg_dict[rt]
        memoryCount += 1
        print("\n")
        cmd = str(bin(reg_dict[rs] + imm)[2:]).zfill(32)
        #print("cmd =", cmd)
        tag = cmd[0:25]
        set = cmd[25:26]
        offset = cmd[26:]
        f = open("log.txt", "a")
        f.write("(")
        f.write(str(index))
        f.write(") ")
        f.write("addres: ")
        f.write(hex(int(instr[pc], 2)))
        f.write("\n")
        f.write("tag =")
        f.write(hex(int(tag)))
        f.write("\n")
        f.write("set = ")
        f.write(set)
        f.write("\n")
        f.write("offset =")
        f.write(offset)
        f.write("\n")
        index += 1
        #print("set ="set)
        set = "set" + str(int(set,2))
        #if its a hit:
        if (cache_dict[set]["w1"] == tag):
          if (set == 'set0'):
            cache_cnt_dict[set]["w1s0"] = casheCnt
            hit = hit + 1
            casheCnt2 = casheCnt + 1
            f.write("HIT!\n\n")
          elif(set == 'set1'):
            way = 'w1s1'
            cache_cnt_dict[set]["w1s1"] = casheCnt
            hit = hit + 1
            casheCnt2 = casheCnt + 1
            f.write("HIT!\n\n")
            
        elif (cache_dict[set]["w2"] == tag):
          if (set == 'set0'):
            cache_cnt_dict[set]["w2s0"] = casheCnt
            hit = hit + 1
            casheCnt2 = casheCnt + 1
            f.write("HIT!\n\n")
          elif(set == 'set1'):
            way = 'w1s1'
            cache_cnt_dict[set]["w2s1"] = casheCnt
            hit = hit + 1
            casheCnt2 = casheCnt + 1
            f.write("HIT!\n\n")
            
        elif (cache_dict[set]["w3"] == tag):
          if (set == 'set0'):
            cache_cnt_dict[set]["w3s0"] = casheCnt
            hit = hit + 1
            casheCnt2 = casheCnt + 1
            f.write("HIT!\n\n")
          elif(set == 'set1'):
            cache_cnt_dict[set]["w3s1"] = casheCnt
            hit = hit + 1
            casheCnt2 = casheCnt + 1
            f.write("HIT!\n\n")
            
        elif (cache_dict[set]["w4"] == tag):
          if (set == 'set0'):
            cache_cnt_dict[set]["w4s0"] = casheCnt
            hit = hit + 1
            casheCnt2 = casheCnt + 1
            f.write("HIT!\n\n")
          elif(set == 'set1'):
            cache_cnt_dict[set]["w4s1"] = casheCnt
            hit = hit + 1
            casheCnt2 = casheCnt + 1
            f.write("HIT!\n\n")
        #if its a miss:
        if ((cache_dict[set]["w1"] != tag) and
            (cache_dict[set]["w2"] != tag) and 
			      (cache_dict[set]["w3"] != tag) and 
            (cache_dict[set]["w4"] != tag)):
              
          #first check to see if any way is open
          if(cache_dict[set]["w1"] == 0):
            cache_dict[set]["w1"] = tag
            if(set == 'set0'):
              cache_cnt_dict[set]["w1s0"] = casheCnt
              casheCnt = casheCnt + 1
              miss = miss + 1
              f.write("MISS\n\n")
            elif (set == 'set1'):
              cache_cnt_dict[set]["w1s1"] = casheCnt2
              casheCnt2 = casheCnt2 + 1
              miss = miss + 1
              f.write("MISS\n\n")
            
          elif(cache_dict[set]["w2"] == 0):
            cache_dict[set]["w2"] = tag
            if(set == 'set0'):
              cache_cnt_dict[set]["w2s0"] = casheCnt
              casheCnt = casheCnt + 1
              miss = miss + 1
              f.write("MISS\n\n")
            elif (set == 'set1'):
              cache_cnt_dict[set]["w2s1"] = casheCnt2
              casheCnt2 = casheCnt2 + 1
              miss = miss + 1
              f.write("MISS\n\n")

          elif(cache_dict[set]["w3"] == 0):
            cache_dict[set]["w3"] = tag
            if(set == 'set0'):
              cache_cnt_dict[set]["w3s0"] = casheCnt
              casheCnt = casheCnt + 1
              miss = miss + 1
              f.write("MISS\n\n")
            elif (set == 'set1'):
              cache_cnt_dict[set]["w3s1"] = casheCnt2
              casheCnt2 = casheCnt2 + 1
              miss = miss + 1
              f.write("MISS\n\n")

          elif(cache_dict[set]["w4"] == 0):
            cache_dict[set]["w4"] = tag
            if(set == 'set0'):
              cache_cnt_dict[set]["w4s0"] = casheCnt
              casheCnt = casheCnt + 1
              miss = miss + 1
              f.write("MISS\n\n")
            elif (set == 'set1'):
              cache_cnt_dict[set]["w4s1"] = casheCnt2
              casheCnt2 = casheCnt2 + 1
              miss = miss + 1
              f.write("MISS\n\n")

          else:
            key_min = min(cache_cnt_dict[set].keys(), key = (lambda k: cache_cnt_dict[set][k]))
            print("cum", key_min[0:2])
            way = key_min[0:2]
            cache_dict[set][way] = tag
            cntSet = key_min[3:]
            cntSet =  "set" + cntSet
            if (cntSet == 'set0'):
              cache_cnt_dict[cntSet][key_min] = casheCnt
              casheCnt = casheCnt + 1 
              miss = miss + 1
              f.write("MISS\n\n")
            elif (cntSet == 'set1'):
              cache_cnt_dict[cntSet][key_min] = casheCnt2
              casheCnt2 = casheCnt2 + 1 
              miss = miss + 1
              f.write("MISS\n\n")
        pc += 4
      elif instr[pc][0:6] == "111111":
        pc += 4
        parity = 0
        if reg_dict['5'] < 0:
          reg_dict['5'] += 2**32
        while reg_dict['5'] != 0:
          y = reg_dict['5'] % 2
          parity += y
          z = int(reg_dict['5'] / 2)
          reg_dict['5'] = z
        reg_dict['3'] = parity
        #count = getParity()
        ALUcount += 1
      if s_flag:
        print(instr_text)
        print("hex: ", commands[pc - 4], sep='')
        print("PC: ", pc - 4, sep='')
        print("rs $", rs, ": ", reg_dict[rs], sep='')
        print("rt $", rt, ": ", reg_dict[rt], sep='')
        print("sh $", rt, sep='')
        print("imm: ", imm, sep='')
    reg_dict['32'] = pc
if(config == '1'):
  policy = "Direct Mapping"
  blocks = 8
  size = 16
if(config == '2'):
  policy = "Direct Mapping"
  blocks = 4
  size = 8
if(config == '3'):
  policy = "Fully Associative"
  blocks = 4
  size = 8
if(config == '4'):
  policy = "Set Associative"
  blocks = 4
  size = 16
t = miss + hit 
te = round(100*(hit/t))
#endIn = input("Do you want to search for a specific adress y/n?")
#while endIn == 'y':
#hexIn = input("Please input hex address or n to leave")
#print(hex(int(hexIn,base=16)),':[',saved_dict[int(hexIn,base=16)],']')
print("\n------------Instruction Statistics-----------\n")
print("Total Instructin:", ALUcount + branchCount + memoryCount + otherCount)
print("AlU count:", ALUcount)
print("Branch count:", branchCount)
print("Memory count:", memoryCount)
print("Other count:", otherCount)
print("\n--------------Memory/Register Values---------\n")
for i, x in enumerate(saved_dict):
  if i <= 32:
    print(
      f'Memory {hex(x)} = [{saved_dict[x]:4}]   |||   Reg ${i:2} = [{reg_dict[str(i)]:4}]'
    )
  else:
    print(f'Memory {hex(x)} = [{saved_dict[x]:3}] ')
  x += 4
print("\n------------------Data Cache Info--------------\n")
print("Placement Policy:", policy)
print("Number of blocks:", blocks)
print("Cache block size (words)", size)
print("Block Replacement Policy: LRU\n")
print("Memory Access Count:",t)
print("Cache Hit Count: ", "\033[32m", hit, "\033[0m", sep = '')
print("Cashe Miss Count: ", "\033[31m", miss, "\033[0m", sep = '')
print("Cache Hit Rate: ", "\033[34m", te, "%","\033[0m", sep = '')
# items = list(range(0, hit))
# smallhit = int(hit/4)
# smallmiss = int(miss/4)
# l = len(items)
# printProgressBar(0, l, prefix = 'HIT RATE:', suffix = "", length = smallhit + smallmiss)
# cntr = 0
# for i, item in enumerate(items):
#     if(cntr <= te):
#       time.sleep(0.1)
#       printProgressBar(i + 1, l, prefix = 'HIT RATE:', suffix = "", length = smallhit + smallmiss)
#       cntr += 1