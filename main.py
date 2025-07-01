import sys
import io
from cfg import Block
from cfg import CFG
import re
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

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # verifica se a linha tem formato (n m)
        if header.match(line):
            data = line.split(" ")
            n = str(data[0]) # nome do bloco
            m = int(data[1]) # quantidade de instrucoes
            block = Block(n, [], [])

            # adiciona as instrucoes
            for j in range (m):
                i += 1
                block.add_instruction(lines[i].strip())

            i += 1

            block_edges = lines[i].split(" ")
            # adiciona as arestas 
            for edge in block_edges:
                if edge != '0':
                    block.add_successor(edge.strip())
                    cfg.add_edge((block.name, edge.strip()))

            cfg.add_node(block)

        i += 1

    for block in cfg.nodes:
        block.def_use_variables()
        print(f"{block.name} defined: {block.defined}, use: {block.use}")

    print(cfg.__str__())

if __name__ == "__main__":
    main()