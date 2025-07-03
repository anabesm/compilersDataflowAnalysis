Equipe:
- Ana Beatriz de Sousa Martins - 553026
- Rebeca Amorim Penha - 553614
- Ricardo Andrade Chagas Cavalcante - 555596

Execução:

    - Acesse o diretório raiz do projeto:
        cd /caminho/para/compilersDataflowAnalysis
    - Execute com:
        python main.py <arquivo_teste>

Localização das questões:

1. Análise de Longevidade (livenessAnalysis.py): determina quais variáveis estão vivas em determinado ponto do programa, ou seja, se seu valor pode ser usado mais adiante.
    - Tipo de análise: backward (reversa)
    - Equações:
        - IN[B] = USE[B] ∪ (OUT[B] - DEF[B])
        - OUT[B] = ⋃ IN[S] para todos os sucessores S de B

2. Reaching Definitions (a implementar): identifica quais definições de variáveis podem atingir um determinado ponto do programa sem serem sobrescritas.
    - Tipo de análise: forward (direta)
    - Equações:
        - GEN[B]: definições geradas em B
        - KILL[B]: definições invalidadas em B
        - IN[B] = ⋃ OUT[P] para todos os predecessores P de B
        - OUT[B] = GEN[B] ∪ (IN[B] - KILL[B])

3. Available Expressions (availableExpressions.py): determina quais expressões já foram calculadas e ainda são válidas (não invalidadas por reatribuições).
    - Tipo de análise: forward (direta)
    - Equações:
        - GEN[B]: expressões computadas em B
        - KILL[B]: expressões invalidadas em B
        - IN[B] = ⋂ OUT[P] para todos os predecessores P de B
        - OUT[B] = GEN[B] ∪ (IN[B] - KILL[B])