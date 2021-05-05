# Inteligencia Artificial e Sistemas Inteligentes - Trabalho de Busca

## Busca Cega - BFS
Foi optado por busca em largura como algoritmo de busca cega. A ideia eh explorar todos os possiveis nodos do board de sudoku de forma linear e expandi-los a partir dai, validando cada novo estado ate chegar em um resultado.

## Busca Heuristica - DFS + A*
Foi utilizada a busca A* juntamente com DFS (para expansao dos nodos) neste algoritmo. A ideia eh de explorar os nodos dando preferencia aos movimentos que propiciam menor numeros de opcoes no quadro e ter uma representacao em grafo de quantos movimentos sao necessarios ate completar o desafio.