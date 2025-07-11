import sys
import io
from cfg import Block
from cfg import CFG
import re
from livenessAnalysis import livenessAnalysis
from avaliableExpression import available_expressions
from reachingDefinitions import reaching_definitions

def read_source():
    if len(sys.argv) > 1:
        path = sys.argv[1]
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    return sys.stdin.read()

def main():
    code = read_source()
    cfg = CFG([], [])
    lines = code.split("\n")
    header = re.compile(r"^\d+\s+\d+$")
    succ_allocator = {}

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # verifica se a linha tem formato (n m)
        if header.match(line):
            data = line.split(" ")
            n = str(data[0]) # nome do bloco
            m = int(data[1]) # quantidade de instrucoes
            block = Block(n, [], [])
            succ_allocator[n] = set()

            # adiciona as instrucoes
            for j in range (m):
                i += 1
                block.add_instruction(lines[i].strip())

            i += 1

            block_edges = lines[i].split(" ")
            # adiciona as arestas e sucessores 
            for edge in block_edges:
                new_block = Block (edge.strip(), [], [])
                if edge != '0':
                    succ_allocator[n].add(new_block.name)
                    # block.succ_names.append(edge.strip())
                    cfg.add_edge((block.name, edge.strip()))

            cfg.add_node(block)

        i += 1

    # criando pares {block.name: block (object)} para alocar os sucessores
    name_to_block = {block.name: block for block in cfg.nodes}

    # alocando os blocos reais correspondentes aos sucessores
    for block in cfg.nodes:
        block.successors = [name_to_block[name] for name in succ_allocator[block.name]]

    # print(cfg.__str__())

    liveness = livenessAnalysis(cfg)

    reach_defs = reaching_definitions(cfg)

    print("\nLIVENESS ANALYSIS")
    for block in liveness.keys():
        print(f"B{block}:")
        if len(liveness[block]["IN"]) != 0:
            print(f"\tIN: {liveness[block]['IN']}")
        else:
            print(f"\tIN: {{}}")
            
        if len(liveness[block]["OUT"]) != 0:
            print(f"\tOUT: {liveness[block]['OUT']}")
        else:
            print(f"\tOUT: {{}}")

    print("\nREACHING DEFINITIONS ANALYSIS")
    for name in sorted(reach_defs, key=int):
        ins  = {f"Bloco {blk} - linha {idx}" for blk, idx in reach_defs[name]["IN"]}
        outs = {f"Bloco {blk} - linha {idx}" for blk, idx in reach_defs[name]["OUT"]}
        print(f"B{name}:")
        print(f"\tIN : {ins or set()}")
        print(f"\tOUT: {outs or set()}")

    available_expressions(cfg)

if __name__ == "__main__":
    main()