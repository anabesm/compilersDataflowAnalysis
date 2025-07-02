import sys
import io
from cfg import Block
from cfg import CFG
import re
from livenessAnalysis import livenessAnalysis
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


    for block in cfg.nodes:
        block.def_use_variables()

    
    # criando pares {block.name: block (object)} para alocar os sucessores
    name_to_block = {block.name: block for block in cfg.nodes}

    # alocando os blocos reais correspondentes aos sucessores
    for block in cfg.nodes:
        block.successors = [name_to_block[name] for name in succ_allocator[block.name]]

    cfg.find_IN_OUT()

    print(cfg.__str__())

    liveness = livenessAnalysis(cfg)

    print ("LIVENESS ANALYSIS")
    for var in liveness:
        blocks = liveness[var]
        if len(blocks) == 0:
            print(f"\t{var}: {{ }} , total: {len(liveness[var])}")
        else:
            print(f"\t{var}: {blocks}, total: {len(liveness[var])}")

if __name__ == "__main__":
    main()