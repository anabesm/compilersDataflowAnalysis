import re    

# def : conjunto de variáveis atribuídas em B antes de qualquer uso daquela variável em B
# use: conjunto de variáveis usadas em B antes de qualquer atribuição à variável em B
def def_use_variables (block):
    reserved = ["return", "if", "else", "goto", "print"]
    variables_rule = re.compile(r"[a-zA-Z_][a-zA-Z0-9_]*")

    for i in block.instructions:
        if "=" in i:
            left, right = i.split("=")
            left = left.strip()

            right_parts = right.split(" ")

            for part in right_parts:
                if variables_rule.match(part) and part not in reserved and part not in block.defined:
                    block.use.add(part)

            if  left not in block.use:
                block.defined.add(left)


        else:
            parts = i.split(" ")

            for part in parts:
                if variables_rule.match(part) and part not in reserved and part not in block.defined:
                    block.use.add(part)


# IN: conjunto de variáveis vivas no início de B
# OUT: conjunto de variáveis vivas no fim de B
def find_IN_OUT(cfg):
    change = True

    while (change):
        change = False
        for block in reversed(cfg.nodes):
            curr_IN = block.IN.copy()
            curr_OUT = block.OUT.copy()

            for succ in block.successors:
                block.OUT.update(succ.IN)

            block.IN = (block.use).union((block.OUT).difference(block.defined))

            if (curr_IN != block.IN or curr_OUT != block.OUT):
                change = True

def livenessAnalysis(cfg):
    liveness = {} # par {bloco: {IN, OUT}}

    for block in cfg.nodes:
        block.defined = set()
        block.use = set()
        block.IN = set()
        block.OUT = set()
        def_use_variables(block)

    find_IN_OUT(cfg)

    for block in cfg.nodes:
        liveness[block.name] = {"IN": block.IN, "OUT": block.OUT}

    return liveness