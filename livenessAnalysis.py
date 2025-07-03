import re

def livenessAnalysis(cfg):
    variables = {} # variável: blocos em que ela está viva

    # identificando todas as variáveis usadas no código
    for block in cfg.nodes:
        for var in (block.use).union(block.defined):
            variables[var] = set() 
    print(variables)

    # identificando onde cada variável está viva
    for block in cfg.nodes:
        for var in block.IN | block.OUT:
            variables[var].add(block.name)
        
    return variables