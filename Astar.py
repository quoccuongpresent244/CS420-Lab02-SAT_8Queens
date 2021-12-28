import random
import time
from function import attacked_queens_pairs, display_board, read_input

def Astar():
    seqs = read_input()
    frontier_priority_queue = [{'unplaced_queens':seqs.count(0), 'pairs':attacked_queens_pairs(seqs), 'seqs':seqs}]
    solution = []
    flag = 0 

    while frontier_priority_queue: 
        first = frontier_priority_queue.pop(0)  
        if first['pairs'] == 0 and first['unplaced_queens'] == 0: 
            solution = first['seqs']
            flag = 1  
            break
        nums = list(range(1, 9))  
        seqs = first['seqs']
        if seqs.count(0) == 0: 
            continue 
        for j in range(8): 
            pos = seqs.index(0)
            temp_seqs = list(seqs)
            temp = random.choice(nums)  
            temp_seqs[pos] = temp 
            nums.remove(temp)  
            frontier_priority_queue.append({'unplaced_queens':temp_seqs.count(0), 'pairs':attacked_queens_pairs(temp_seqs),'seqs':temp_seqs})
        frontier_priority_queue = sorted(frontier_priority_queue, key=lambda x:(x['pairs']+x['unplaced_queens']))

    if solution:
        #print('Solution sequence found:' + str(solution))
        #display_board(solution)
        return solution
    else:
        return False