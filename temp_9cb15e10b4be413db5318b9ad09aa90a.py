import rand
a = []
for i in range(3):
    b = []
    for j in range(3):
        b.append(i+j+1+rand()%3)
    a.append(b)
print(a)
    