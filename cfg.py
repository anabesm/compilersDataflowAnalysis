# gráfico de fluxo de controle
import re

class Block:
    def __init__(self, name, instructions, successors):
        self.name = name
        self.instructions = instructions
        self.successors = successors
        self.IN = set()
        self.OUT = set()
        self.defined = set()
        self.use = set()

    def add_instruction(self, instruction):
        self.instructions.append(instruction)

    def add_successor(self, edge):
        self.successors.append(edge)

    def get_instructions(self):
        instructions = ""
        for i in self.instructions:
            instructions += f"\t{i}\n"
        return instructions

    def get_successors(self):
        successors = "[ "
        for s in self.successors:
            successors += f"{s.name} "
        successors += "]"
        return successors
    
    # def : conjunto de variáveis atribuídas em B antes de qualquer uso daquela variável em B
    # use: conjunto de variáveis usadas em B antes de qualquer atribuição à variável em B
    def def_use_variables (self):

        reserved = ["return", "if", "else", "goto", "print"]
        variables_rule = re.compile(r"[a-zA-Z_][a-zA-Z0-9_]*")

        for i in self.instructions:
            if "=" in i:
                left, right = i.split("=")
                left = left.strip()

                right_parts = right.split(" ")

                for part in right_parts:
                    if variables_rule.match(part) and part not in reserved and part not in self.defined:
                        self.use.add(part)

                if  left not in self.use:
                    self.defined.add(left)


            else:
                parts = i.split(" ")

                for part in parts:
                    if variables_rule.match(part) and part not in reserved and part not in self.defined:
                        self.use.add(part)


            
    
    def __str__(self):
        res = f"B{self.name}\n"
        for i in self.instructions:
            res += f"\t{i}\n"
        return res

    
class CFG:
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges

    def add_node(self, node):
        self.nodes.append(node)

    def add_edge(self, edge):
        self.edges.append(edge)

    # IN: conjunto de variáveis vivas no início de B
    # OUT: conjunto de variáveis vivas no fim de B
    def find_IN_OUT(self):
        change = True

        while (change):
            change = False
            for block in reversed(self.nodes):
                curr_IN = block.IN.copy()
                curr_OUT = block.OUT.copy()

                for succ in block.successors:
                    block.OUT.update(succ.IN)

                block.IN = (block.use).union((block.OUT).difference(block.defined))

                if (curr_IN != block.IN or curr_OUT != block.OUT):
                    change = True
                
                # print(f"B{block.name} old_in: {curr_IN} old_in: {curr_OUT}")
                # print(f"B{block.name} new_in: {block.IN} new_out: {block.OUT}")
                # print("----------")

    
    def __str__(self):
        cfg_str = ""

        for node in self.nodes:
            cfg_str += f"B{node.name}: {node.get_instructions()}\n Succ: {node.get_successors()}\n def: {node.defined}\n use: {node.use}\n IN: {node.IN}\n OUT: {node.OUT}\n\n"
        cfg_str += "Edges:\n"
        for edge in self.edges:
            cfg_str += f"\t{edge[0]} -> {edge[1]}\n"
            
        return cfg_str