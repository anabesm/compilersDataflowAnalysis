import re

def livenessAnalysis(cfg):
    variables = {}
    variables_rule = re.compile(r"[a-zA-Z_][a-zA-Z0-9_]*")
    reserved = ["return", "if", "else", "while", "for", "goto"]


    for block in cfg.nodes:
        for i in block.instructions:
            for part in i.split(" "):
                if variables_rule.match(part) and part not in reserved and part not in variables:
                    variables[part] = set() 


    for var in variables:
        for block in cfg.nodes:
            if var in block.IN and var in block.OUT:
                variables[var].add(block.name)
        
    return variables