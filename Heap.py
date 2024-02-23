import heapq
import numpy as np

# new scoville calculator
def new_sco(a, b):
    mix_sco = a + (b * 2)
    return mix_sco

# count how much times scoville takes to overcome value of K
def solution(scoville, K):
    answer = 0
    while len(scoville) >= 2 and sorted(scoville)[0] < K:
        scoville.append(new_sco(sorted(scoville)[0], sorted(scoville)[1]))
        del scoville[np.argmin(scoville)]
        del scoville[np.argmin(scoville)]
        answer+=1
        if len(scoville) == 1 and sorted(scoville)[0] < K:
            return -1
    return answer