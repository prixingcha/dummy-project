with open('subscribe_list.txt', 'r') as file:
    data = file.read().strip()[1:-1].split(', ')
    # data is now a list of strings containing the channel IDs
    # print(data)
    
for x in data:
    print(x)