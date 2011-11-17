class IntermediateNode(object):
    def __init__(self, parents):
        self.parents = parents

    def parentsToString(self):
        return [x.generateCode() for x in self.parents]
            

    #TODO: MAKE THIS ABSTRACT
    def generateIntermediateCode(self, registerMap):
        pass
        
    def generateCode(self, registerMap = {}):
        pass
        
    def alteredRegisters(self):
        return []

    def uses(self):
        return self.registers
        
class InstructionNode(IntermediateNode):
    def __init__(self, instruction, parents):
        super(InstructionNode, self).__init__(parents)
        self.instruction = instruction
    
    def generateIntermediateCode(self):
        return "%s " %(self.instruction) + (', ').join(["T%d" % r for r in self.registers])
    
    def generateCode(self, registerMap = {}):
        if registerMap == {}:
            return self.generateIntermediateCode()
        return ["%s " %(self.instruction) + (', ').join(["%s" % registerMap[r] for r in self.registers])]
    
    def alteredRegisters(self):
        return [self.registers[0]]
        
class MovNode(InstructionNode):
    def __init__(self, reg1, reg2, parents):
        super(MovNode, self).__init__("mov", parents)
        self.registers = [reg1, reg2]
    
    def uses(self):
        return [self.registers[1]]

class ImmMovNode(InstructionNode):  
    def __init__(self, reg, imm, parents):
        super(ImmMovNode, self).__init__("mov", parents)  
        self.registers = [reg]
        self.imm = imm
        
    def generateIntermediateCode(self):
        return "%s T%d, %s" %(self.instruction, self.registers[0], self.imm)
        
    def generateCode(self, registerMap = {}):
        if registerMap == {}:
            return self.generateIntermediateCode()
        return ["%s %s, %s" %(self.instruction, registerMap[self.registers[0]], self.imm)]

    def uses(self):
        return []
    
    
#TODO MAKE THIS ABSTRACT
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

    def generateIntermediateCode(self):
        return "%s T%d, %s" %(self.instruction, self.registers[0], self.imm)

    def generateCode(self, registerMap = {}):
        if registerMap == {}:
            return self.generateIntermediateCode() 
        
        idivRegisters = ["rax", "rdx", "rcx" ]
        registersToPreserve = list( set(idivRegisters) - set(self.registers) )
        return (["cmp %s %d" % (self.registers[1], 0),
                 "jz os_return" ] +
                [["push", x] for x in registersToPreserve] +
                ["mov rax, %s"%self.registers[0],
                 "mov rcx, %s"%self.registers[1],
                 "mov rdx, %d"%0,
                 "idiv rcx",
                 "mov %s %s"%(self.registers[0], self.regToReturn)
                ] +
                [["pop", x] for x in registersToPreserve])
        
class ModNode(DivNode):
    def __init__(self, reg1, reg2, parents):
        super(ModNode, self).__init__("idiv", reg1, reg2, parents) 
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
    def __init__(self, reg, parents):
        super(SpokeNode, self).__init__(parents)
        self.registers = [reg]

    def generateIntermediateCode(self):
        return "PRINT T%d" %self.registers[0]
        
    def generateCode(self, registerMap = {}):
        if registerMap == {}:
            return self.generateIntermediateCode()
        
        return ["mov rsi, %s" % registerMap[self.registers[0]],
                "mov rdi, intfmt",
                "xor rax, rax",
                "call printf"]
    
