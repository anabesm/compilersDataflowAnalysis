# gráfico de fluxo de controle
import re

class Block:
    def __init__(self, name, instructions, successors):
        self.name = name
        self.instructions = instructions
        self.successors = successors
        self.IN = []
        self.OUT = []
        self.defined = []
        self.use = []

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
        successors = ""
        for s in self.successors:
            successors += f"\t{s}\n"
        return successors
    
    def def_use_variables (self):

        reserved = ["return", "if", "else", "while", "for", "goto"]
        variables_rule = re.compile(r"[a-zA-Z_][a-zA-Z0-9_]*")

        for i in self.instructions:
            if "=" in i:
                left, right = i.split("=")
                left = left.strip()

                right_parts = right.split(" ")

                for part in right_parts:
                    if variables_rule.match(part) and part not in self.use and part not in reserved and part not in self.defined:
                        self.use.append(part)

                if left not in self.defined:
                    self.defined.append(left)


            else:
                parts = i.split(" ")

                for part in parts:
                    if variables_rule.match(part) and part not in self.use and part not in reserved and part not in self.defined:
                        self.use.append(part)
            
    
    def __str__(self):
        res = f"Block: {self.name}\n"
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
    
    def __str__(self):
        res = "CFG:\n"
        for node in self.nodes:
            res += f"{node.name}: {node.get_instructions()}\n"
        res += "Edges:\n"
        for edge in self.edges:
            res += f"\t{edge[0]} -> {edge[1]}\n"
        return res
    