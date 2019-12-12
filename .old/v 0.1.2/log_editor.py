# Universal func for add data to log
def add2log(data, file):
    open('./log/' + file, 'a', encoding="utf8").write(data + '\n')