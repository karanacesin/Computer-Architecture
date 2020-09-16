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

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 7

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

            else:
                print(f"Unknown instruction {ir}")
