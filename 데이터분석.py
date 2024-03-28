def solution(data, ext, val_ext, sort_by):
    answer = [[]]
    new_answer = []
    new_answer1 = []
    dic = {"code" : 0, "date" : 1, "maximum" : 2, "remain" : 3}
    new_dic = dic[ext]
    new_dic1 = dic[sort_by]
    for i in range(len(data)):
        new_answer = data[i]
        if new_answer[new_dic] < val_ext:
            new_answer1.append(new_answer)
        else:
            continue
    new_answer1.sort(key = lambda x:x[new_dic1])
    answer = new_answer1
    return answer