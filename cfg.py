class Block:
    def __init__(self, name, instructions, successors):
        self.name = name
        self.instructions = instructions
        self.successors = successors

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
    
    def __str__(self):
        cfg_str = ""

        for node in self.nodes:
            cfg_str += f"B{node.name}: {node.get_instructions()}\n\n"
        cfg_str += "Edges:\n"
        for edge in self.edges:
            cfg_str += f"\t{edge[0]} -> {edge[1]}\n"
            
        return cfg_str