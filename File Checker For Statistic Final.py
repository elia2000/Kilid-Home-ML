
all = ''
for i in range(400):
    file_path = 'Doros 2/Statistic Page '+ str(i) + '.txt'
    with open(file_path , 'r') as file:
        lines = file.readlines()
        file.close()
        if lines[3] == '		All: 0 \n':
            all += f'{i}\n'
with open('none pages 2.txt', 'w') as file_a:
        file_a.write(all)
file_a.close()