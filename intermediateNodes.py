import re

class IntermediateNode(object):
    def __init__(self, parents):
        self.parents = parents

    def generateCode(self, registerMap):
        pass
        
    def alteredRegisters(self):
        return []

    def uses(self):
        return self.registers
        
    def pushRegs(self, registersToPush):
        return ["push %s" %x for x in registersToPush]
        
    def popRegs(self, registersToPop):
        return ["pop %s" %x for x in registersToPop]
        
class InstructionNode(IntermediateNode):
    def __init__(self, instruction, parents):
        super(InstructionNode, self).__init__(parents)
        self.instruction = instruction
        
    def generateCode(self, registerMap):
        return ["%s " %(self.instruction) + (', ').join(["%s" % registerMap[r] for r in self.registers])]
    
    def alteredRegisters(self):
        return [self.registers[0]]
        
    # Works out if a given value for an instruction is in memory by using 
    # regular expressions. 
    def isInMemory(self, value):
        return re.match('\[\w+\]', value)
        
class MovNode(InstructionNode):
    def __init__(self, reg1, reg2, parents):
        super(MovNode, self).__init__("mov", parents)
        self.registers = [reg1, reg2]
    
    def uses(self):
        return [self.registers[1]]
    
    def generateCode(self, registerMap):
        if registerMap[self.registers[0]] == registerMap[self.registers[1]]:
            return []
        return ["%s " %(self.instruction) + (', ').join(["%s" % registerMap[r] for r in self.registers])]

class ImmMovNode(InstructionNode):  
    def __init__(self, reg, imm, parents):
        super(ImmMovNode, self).__init__("mov", parents)  
        self.registers = [reg]
        self.imm = imm
        
    # Chosen to move into rax as it is a given in assembly that this register will
    # get overwritten in function calls.
    def generateCode(self, registerMap):
        destReg = registerMap[self.registers[0]]
        if self.isInMemory(destReg):
            return ["mov rax, %s \n%s %s, rax" %(self.imm, self.instruction, destReg)]
            
        return ["%s %s, %s" %(self.instruction, registerMap[self.registers[0]], self.imm)]

    def uses(self):
        return []
    
class BinOpNode(InstructionNode):
    def __init__(self, instruction, reg1, reg2, parents):
        super(BinOpNode, self).__init__(instruction, parents)  
        self.registers = [reg1, reg2]

class AddNode(BinOpNode):
    def __init__(self, reg1, reg2, parents):
        super(AddNode, self).__init__("add", reg1, reg2, parents)  
        
class SubNode(BinOpNode):
    def __init__(self, reg1, reg2, parents):
        super(SubNode, self).__init__("sub", reg1, reg2, parents) 
         
class MulNode(BinOpNode):
    def __init__(self, reg1, reg2, parents):
        super(MulNode, self).__init__("imul", reg1, reg2, parents)
          
class DivNode(BinOpNode):
    def __init__(self, reg1, reg2, parents):
        super(DivNode, self).__init__("idiv", reg1, reg2, parents)
        self.regToReturn = "rax"
        self.idivRegisters = ["rdx", "rcx"]
    
    # Preserves registers that could get overwritten by the div instruction
    # unless it's the desintation register.
    # Puts registers in relevant registers required by idiv instruction.
    def generateCode(self, registerMap):
        destReg, nextReg = map(lambda x: registerMap[x], self.registers)
        registersToPreserve = list(set(self.idivRegisters) - set([destReg]))
        registersToPreserveReverse = registersToPreserve[0:]
        registersToPreserveReverse.reverse()
        
        if self.isInMemory(nextReg):
            compCode = "mov rax, %s \ncmp rax, 0" %(nextReg)
        else:
            compCode = "cmp %s, 0" %nextReg
        
        return ([compCode,
                 "jz os_return" ] +
                self.pushRegs(registersToPreserve) +
                ["mov rax, %s" %destReg,
                 "mov rcx, %s" %nextReg,
                 "mov rdx, %d" %0,
                 "idiv rcx",
                 "mov %s, %s"%(destReg, self.regToReturn)] +
               self.popRegs(registersToPreserveReverse))
        
class ModNode(DivNode):
    def __init__(self, reg1, reg2, parents):
        super(ModNode, self).__init__(reg1, reg2, parents) 
        self.regToReturn = "rdx"
         
class OrNode(BinOpNode):
    def __init__(self, reg1, reg2, parents):
        super(OrNode, self).__init__("or", reg1, reg2, parents)  
        
class XORNode(BinOpNode):
    def __init__(self, reg1, reg2, parents):
        super(XORNode, self).__init__("xor", reg1, reg2, parents) 
         
class AndNode(BinOpNode):
    def __init__(self, reg1, reg2, parents):
        super(AndNode, self).__init__("and", reg1, reg2, parents)  

class UnOpNode(InstructionNode):
    def __init__(self, instruction, reg, parents):
        super(UnOpNode, self).__init__(instruction, parents)  
        self.registers = [reg]
        
class IncNode(UnOpNode):
    def __init__(self, reg, parents):
        super(IncNode, self).__init__("inc", reg, parents)
        
class DecNode(UnOpNode):
    def __init__(self, reg, parents):
        super(DecNode, self).__init__("dec", reg, parents)
        
class NotNode(UnOpNode):
    def __init__(self, reg, parents):
        super(NotNode, self).__init__("not", reg, parents)

class SpokeNode(IntermediateNode):
    def __init__(self, reg, parents, formatting):
        super(SpokeNode, self).__init__(parents)
        self.registers = [reg]
        self.formatting = formatting
        self.spokeRegisters = ['rsi', 'rdi']
    
    # Puts registers in the relevant registers required for printf call and
    # preserves the registers which may be overwritten.
    def generateCode(self, registerMap):
        destReg = registerMap[self.registers[0]]
        registersToPreserve = list(set(self.spokeRegisters) - set([destReg]))
        registersToPreserveReverse = registersToPreserve[0:]
        registersToPreserveReverse.reverse()
        return (self.pushRegs(registersToPreserve) +
                ["mov rsi, %s" %destReg,
                "mov rdi, %s" %self.formatting,
                "xor rax, rax",
                "call printf"] +
                self.popRegs(registersToPreserve))
