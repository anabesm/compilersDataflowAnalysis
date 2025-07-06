def collect_defs(cfg):
    defs = set()
    def_var = {}
    for block in cfg.nodes:
        for idx, instruction in enumerate(block.instructions):
            if "=" in instruction:
                var = instruction.split("=",1)[0].strip()
                did = (block.name, idx)
                defs.add(did)
                def_var[did] = var
    return defs, def_var

def compute_gen_kill(block, defs, def_var):
    block.GEN = set()
    block.KILL = set()
    for idx, instruction in enumerate(block.instructions):
        if "=" in instruction:
            did = (block.name, idx)
            var = def_var[did]
            block.GEN.add(did)
            for d in defs:
                if d != did and def_var[d] == var:
                    block.KILL.add(d)

def reaching_definitions(cfg):
    defs, def_var = collect_defs(cfg)
    for block in cfg.nodes:
        compute_gen_kill(block, defs, def_var)
        block.IN = set()
        block.OUT = set()
    
    changed = True
    while changed:
        changed = False
        for block in cfg.nodes:
            in_old, out_old = block.IN.copy(), block.OUT.copy()

            preds = [P for P in cfg.nodes if block in P.successors]
            block.IN = set()
            for P in preds:
                block.IN |= P.OUT

            block.OUT = block.GEN.union(block.IN.difference(block.KILL))

            if block.IN != in_old or block.OUT != out_old:
                changed = True

    result = {}
    for block in cfg.nodes:
        result[block.name] = {
            'IN': block.IN.copy(),
            'OUT': block.OUT.copy(),
        }
    return result