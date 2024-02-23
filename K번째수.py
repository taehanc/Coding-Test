def solution(array, commands):
    answer = []
    new_array = []
    for i in range(len(commands)):
        a = commands[i][0] - 1
        b = commands[i][1]
        c = commands[i][2] - 1
        new_array = array[a:b]
        new_array.sort()
        k_element = new_array[c]
        answer.append(k_element)
    return answer