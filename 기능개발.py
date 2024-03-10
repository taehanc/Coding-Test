import math
def solution(progresses, speeds):
    answer = []
    new_answer = 0
    new_answer1 = []
    for i in range(len(progresses)):
        new_answer = math.ceil((100-progresses[i]) / speeds[i])
        new_answer1.append(new_answer)
    count = 1
    new_answer3 = []
    for i in range(1, len(progresses)):
        if new_answer1[i] > new_answer1[0]:
            answer.append(count)
            new_answer1[0] = new_answer1[i]
            count = 1
        else:
            count += 1
    answer.append(count)
    return answer