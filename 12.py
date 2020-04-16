def dict_log(c_name):
    dict_ = {}
    for i in dict_:
        if i in dict_:
            dict_[i] += 1
            if dict_[i] == 3:
                del dict_[i]
        else:
            dict_[i] = 1
    return dict_[c_name]

# def print_():

print(dict_log("1"))