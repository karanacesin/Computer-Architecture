"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
ADD = 0b10100000
RET = 0b00010001
CMP = 0b10100111
JMP = 0B01010100
JEQ = 0b01010101
JNE = 0b01010110

AND = 0b10101000
DEC = 0b01100110
DIV = 0b10100011
INC = 0b01100101
JGE = 0b01011010
JGT = 0b01010111
JLE = 0b01011001
JLT = 0b01011000
LD = 0b10000011

MOD = 0b10100100
NOP = 0b00000000
NOT = 0b01101001
OR = 0b10101010
PRA = 0b01001000
SHL = 0b10101100
SHR = 0b10101101
ST = 0b10000100
SUB = 0b10100001
XOR = 0b10101011

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 7
        self.fl = 0b00000
        

    def load(self):
        """Load a program into memory."""
        try:
            address = 0

            with open(sys.argv[1]) as f:
                for line in f:
                    
                    comment = line.split('#')
                    instruct = comment[0].strip()

                    if instruct == "":
                        continue

                    value = int(instruct, 2)
                    self.ram[address] = value
                    address += 1

        except FileNotFoundError as err:
            print('\n', err, '\n')
            

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write (self, mar, mdr):
        self.ram[mar] = mdr

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        
        elif op == 'MUL':
            self.reg[reg_a] *= self.reg[reg_b]

        elif op == 'CMP':
            if self.reg[reg_a] == self.reg[reg_b]:
                self.fl = 0b00000001

            if self.reg[reg_a] < self.reg[reg_b]:
                self.fl = 0b00000100

            if self.reg[reg_a] > self.reg[reg_b]:
                self.fl = 0b00000010

        elif op == 'AND':
            self.reg[reg_a] &= self.reg[reg_b]

        elif op == 'DEC':
            self.reg[reg_a] -= 1

        elif op == 'DIV':
            self.reg[reg_a] /= self.reg[reg_b]

        elif op == 'INC':
            self.reg[reg_a] += 1

        elif op == 'MOD':
            self.reg[reg_a] %= self.reg[reg_b]

        elif op == 'NOT':
            self.reg[reg_a] != self.reg[reg_b]

        elif op == 'OR':
            self.reg[reg_a] |= self.reg[reg_b]

        elif op == 'SHL':
            self.reg[reg_a] <<= self.reg[reg_b]

        elif op == 'SHR':
            self.reg[reg_a] >>= self.reg[reg_b]

        elif op == 'SUB':
            self.reg[reg_a] -= self.reg[reg_b]

        elif op == 'XOR':
            self.reg[reg_a] ^= self.reg[reg_b]

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True

        while running:

            ir = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if ir == HLT:
                running = False

            elif ir == LDI:
                self.reg[operand_a] = operand_b
                self.pc +=3

            elif ir == PRN:
                print(self.reg[operand_a])
                self.pc += 2

            elif ir == MUL:
                self.alu('MUL', operand_a, operand_b)
                self.pc +=3

            elif ir == PUSH:
                self.reg[self.sp] -= 1
                value = self.reg[operand_a]
                self.ram[self.reg[self.sp]] = value
                self.pc += 2

            elif ir == POP:
               value =  self.ram[self.reg[self.sp]]
               self.reg[operand_a] = value
               self.reg[self.sp] += 1
               self.pc += 2

            elif ir == CALL:
                self.reg[self.sp] -= 1
                self.ram[self.reg[self.sp]] = self.pc + 2
                self.pc = self.reg[operand_a]

            elif ir == RET:
                ret = self.ram[self.reg[self.sp]]
                self.pc = ret
                self.reg[self.sp] += 1

            elif ir == ADD:
                self.alu('ADD', operand_a, operand_b)
                self.pc += 3

            elif ir== CMP:
                self.alu("CMP", operand_a, operand_b)
                self.pc += 3

            elif ir == JMP:
                self.pc = self.reg[operand_a]

            elif ir == JEQ:

                if self.fl == 0b00000001:
                    self.pc = self.reg[operand_a]

                else:
                    self.pc += 2

            elif ir == JNE:

                if self.fl != 0b00000001:
                    self.pc = self.reg[operand_a]

                else:
                    self.pc += 2

            elif ir == AND:
                self.alu('AND', operand_a, operand_b)
                self.pc += 3

            elif ir == DEC:
                self.alu('DEC', operand_a, 0)
                self.pc += 3

            elif ir == DIV:
                self.alu('DIV', operand_a, operand_b)
                self.pc += 3

            elif ir == INC:
                self.alu('INC', operand_a, 0)
                self.pc += 3

            elif ir == MOD:
                self.alu('MOD', operand_a, operand_b)
                self.pc += 3

            elif ir == NOT:
                self.alu('NOT', operand_a, operand_b)
                self.pc += 3

            elif ir == OR:
                self.alu('OR', operand_a, operand_b)
                self.pc += 3

            elif ir == SHL:
                self.alu('SHL', operand_a, operand_b)
                self.pc += 3

            elif ir == SHR:
                self.alu('SHR', operand_a, operand_b)
                self.pc += 3

            elif ir == SUB:
                self.alu('SUB', operand_a, operand_b)
                self.pc += 3

            elif ir == XOR:
                self.alu('XOR', operand_a, operand_b)
                self.pc += 3

            elif ir == JGE:

                if self.fl == 0b00000001 or self.fl == 0b00000010:
                    self.pc = self.reg[operand_a]

                else:
                    self.pc += 2

            elif ir == JGT:

                if self.fl == 0b00000010:
                    self.pc = self.reg[operand_a]

                else:
                    self.pc += 2

            elif ir == JLE:

                if self.fl == 0b00000001 or self.fl == 0b00000100:
                    self.pc = self.reg[operand_a]

                else:
                    self.pc += 2

            elif ir == JLT:

                if self.fl == 0b00000100:
                    self.pc = self.reg[operand_a]

                else:
                    self.pc += 2

            elif ir == LD:
                self.reg[operand_a] = self.ram_read(self.reg[operand_b])
                self.pc +=3

            elif ir == PRA:
                print(chr(self.reg[operand_a]), end = '')

            elif ir == ST:
                self.ram_write(operand_a, operand_b)

            elif ir == NOP:
                pass

            else:
                print(f"Unknown instruction {ir}")
