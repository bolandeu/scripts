import os


try:
    f = open("list.txt")    
    for line in f.readlines():
        path = 'result/' + line.rstrip()
        try:            
            os.mkdir(path)
        except OSError:
            print ("Создать директорию %s не удалось" % path)
        else:
            print ("Успешно создана директория: %s " % path)    
except IOError:
    print ("Нет файла")
