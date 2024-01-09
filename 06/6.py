import sys
import os 
class Code:
    def dest(self, represent):
        dest_list = {"": "000", "M": "001", "D": "010", "MD": "011", "A": "100", "AM": "101", "AD": "110", "AMD": "111"}
        return dest_list.get(represent, "000")
  
    def jump(self, represent):
        jump_list = {'JGT': '001', 'JEQ': '010', 'JGE': '011', 'JLT': '100', 'JNE': '101', 'JLE': '110', 'JMP': '111'}
        return jump_list.get(represent, '000')
    
    def comp(self, represent):
        comp_list = {
            '0': '101010', '1': '111111', '-1': '111010', 'D': '001100', 'A': '110000', '!D': '001101','!A': '110001','-D': '001111','-A': '110011', 'D+1': '011111', 'A+1': '110111', 'D-1': '001110','A-1': '110010', 'D+A': '000010', 'D-A': '010011', 'A-D': '000111', 'D&A': '000000', 'D|A': '010101'
        }
        a = '0'
        if 'M' in represent:
            a = '1'
            represent = represent.replace('M', 'A')
        c = comp_list.get(represent, '000000')
        total=a+c
        return total 
class Assembler:
    def assemble(self, ASM_files):
        self.prepare_files(ASM_files)
        parser = self.parser
        while parser.commandsduo:
            parser.advance()
            if parser.command_type == 'L':
                self.forL(parser.symbol)
        parser.reset_file()
        self.ram_address = 16
        while parser.commandsduo:
            parser.advance()
            if parser.command_type == 'A':
                self.forA(parser.symbol)
            elif parser.command_type == 'C':
                self.forC(parser.dest, parser.comp, parser.jump)
        parser.close_asm()
        self.hack.close()

    def prepare_files(self, ASM_files):
        if '.asm' not in ASM_files:
            raise ValueError('.asm file must be passed!')
        self.parser.load_file(ASM_files)
        HACK_files = ASM_files.replace('.asm', '.hack')
        self.hack = open(HACK_files, 'w')

    def create_address(self, symbol):
        address = '{0:b}'.format(int(symbol))
        foundation = (15 - len(address)) * '0'
        return foundation + address

    def write(self, instruction):
        self.hack.write(instruction + '\n')

    def forA(self, symbol):
        instruction = '0'
        try:
            int(symbol)
        except ValueError:
            if not self.symbol_table.contains(symbol):
                address = self.create_address(self.ram_address)
                self.symbol_table.add_entry(symbol, address)
                self.ram_address += 1
            instruction += self.symbol_table.get_address(symbol)
        else:
            instruction += self.create_address(symbol)
        self.write(instruction)
    def forC(self, dest, comp, jump):
        instruction = '111'
        instruction += self.code.comp(comp)
        instruction += self.code.dest(dest)
        instruction += self.code.jump(jump)
        self.write(instruction)
    def forL(self, symbol):
        address = self.create_address(self.parser.instruction_num + 1)
        self.symbol_table.add_entry(symbol, address)
    def __init__(self, parser, symbol_table, code):
        self.parser = parser
        self.symbol_table = symbol_table
        self.code = code
class Parser:
  def load_file(self, ASM_files):
    self.asm = open(ASM_files, 'r')
    self.reset_file()
    self.comp = None
    self.jump = None
    self.symbol = None
    self.dest = None
    self.command_type = None

  def reset_file(self):
    self.asm.seek(0)
    line = self.asm.readline().strip()
    while not line or line[:2] == '//':
      line = self.asm.readline().strip()
    self.current = line
    self.instruction_num = -1

  def close_asm(self):
    self.asm.close()

  def is_not_instruction(self, line):
    return not line or line[:2] == '//'

  @property
  def commandsduo(self):
    return bool(self.current)

  def get_next_instruction(self):
    line = self.asm.readline().strip()
    line = line.split('//')[0]
    line = line.strip()
    self.current = line

  def advance(self):
    ci = self.current
    if ci[0] == '@':
      self.parse_A(ci)
      self.instruction_num += 1
    elif ci[0] == '(':
      self.parse_L(ci)
    else:
      self.parse_C(ci)
      self.instruction_num += 1
    self.get_next_instruction()

  def parse_A(self, instruction):
    self.symbol = instruction[1:]
    self.command_type = 'A'

  def parse_L(self, instruction):
    self.symbol = instruction[1:-1]
    self.command_type = 'L'

  def parse_C(self, instruction):
    self.dest = None
    self.comp = None
    self.jump = None
    parts = instruction.split(';')
    remainder = parts[0]
    if len(parts) == 2:
      self.jump = parts[1]
    parts = remainder.split('=')
    if len(parts) == 2:
      self.dest = parts[0]
      self.comp = parts[1]
    else:
      self.comp = parts[0]
    self.command_type = 'C'
class SymbolTable:
  def symbol_table(self):
    return {'SP': '000000000000000'  , 'LCL': '000000000000001'   , 'ARG': '000000000000010', 'THIS': '000000000000011',
            'THAT': '000000000000100', 'R0': '000000000000000'    , 'R1': '000000000000001', 'R2': '000000000000010',
            'R3': '000000000000011'  , 'R4': '000000000000100'    , 'R5': '000000000000101', 'R6': '000000000000110',
            'R7': '000000000000111'  , 'R8': '000000000001000'    , 'R9': '000000000001001', 'R10': '000000000001010',
            'R11': '000000000001011' , 'R12': '000000000001100'   , 'R13': '000000000001101', 'R14': '000000000001110',
            'R15': '000000000001111' , 'SCREEN': '100000000000000', 'KBD': '110000000000000'}

  def __init__(self):
    self.sym = self.symbol_table()
    self.ram_position = 16

  def get_address(self, symbol):
    return self.sym[symbol]

  def contains(self, symbol):
    return symbol in self.sym

  def add_entry(self, symbol, address):
    self.sym[symbol] = address

if __name__ == '__main__':
  import sys
  ASM_files = sys.argv[1]
  assembler = Assembler(Parser(), SymbolTable(), Code())
  assembler.assemble(ASM_files)
