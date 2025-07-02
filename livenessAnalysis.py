import re

def livenessAnalysis(cfg):
    variables = {} # variável: blocos em que ela está viva
    variables_rule = re.compile(r"[a-zA-Z_][a-zA-Z0-9_]*")
    reserved = ["return", "if", "else", "goto", "print"]

    # identificando todas as variáveis usadas no código
    for block in cfg.nodes:
        for i in block.instructions:
            for part in i.split(" "):
                if variables_rule.match(part) and part not in reserved and part not in variables:
                    variables[part] = set() 

    # identificando onde cada variável está viva
    for var in variables:
        for block in cfg.nodes:
            if var in block.IN and var in block.OUT:
                variables[var].add(block.name)
        
    return variables