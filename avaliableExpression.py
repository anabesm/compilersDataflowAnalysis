def collect_all_expressions(cfg):
    expressions = set()
    for block in cfg.nodes:
        for instr in block.instructions:
            if "=" in instr:
                _, right = instr.split("=")
                expr = right.strip()
                if any(op in expr for op in ["+", "-", "*", "/"]):
                    expressions.add(expr)
    return expressions


def compute_gen_kill(block, all_expressions):
    for instr in block.instructions:
        if "=" in instr:
            left, right = instr.split("=")
            left = left.strip()
            expr = right.strip()
            if any(op in expr for op in ["+", "-", "*", "/"]):
                block.GEN.add(expr)
            for e in all_expressions:
                if left in e:
                    block.KILL.add(e)


def available_expressions(cfg):
    all_expr = collect_all_expressions(cfg)
    for block in cfg.nodes:
        block.GEN = set()
        block.KILL = set()
        block.IN = all_expr.copy()
        block.OUT = set()
        compute_gen_kill(block, all_expr)

    changed = True
    while changed:
        changed = False
        for block in cfg.nodes:
            in_old = block.IN.copy()
            out_old = block.OUT.copy()

            preds = [b for b in cfg.nodes if block in b.successors]
            if preds:
                block.IN = set.intersection(*(p.OUT for p in preds))
            else:
                block.IN = set()

            block.OUT = block.GEN.union(block.IN - block.KILL)

            if in_old != block.IN or out_old != block.OUT:
                changed = True

    print("\nAVAILABLE EXPRESSIONS ANALYSIS")
    for block in cfg.nodes:
        print(f"B{block.name} GEN: {block.GEN}, KILL: {block.KILL}")

    print("\nEXPRESSIONS AVAILABLE AT ENTRY AND EXIT OF BLOCKS")
    for block in cfg.nodes:
        print(f"B{block.name}")
        print(f"  IN: {block.IN}")
        print(f"  OUT: {block.OUT}")
