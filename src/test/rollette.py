import random

match_max_list = []
for i in range(1000):
    spin_list = []
    for i in range(1000):
        spin_list.append(random.randint(0,1))
    print(spin_list)

    count = 0
    match = 0
    match_max = 0
    for i in range(len(spin_list)-1):
        count += 1
        if spin_list[i] == spin_list[i+1]:
            match += 1
            if match > match_max:
                match_max = match
        else:
            match = 0
    match_max_list.append(match_max)
print(match_max_list)
average_max = sum(match_max_list) / len(match_max_list)
print(average_max)
    

