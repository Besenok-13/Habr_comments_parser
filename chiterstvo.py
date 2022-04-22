with open("input.txt","r") as inp, open("output.txt", "w") as out:
    inp.readline()
    line = inp.readline().split()
    a = []
    obj = 0
    for i in line:
        if i == "+":
            a[obj-2] = a[obj-2]+a[obj-1]
            obj-=1
        elif i == "-":
            a[obj-2] = a[obj-2]-a[obj-1]
            obj-=1
        elif i == "*":
            a[obj-2] = a[obj-2]*a[obj-1]
            obj-=1
        else:
            i=int(i)
            if len(a)>obj:
                a[obj] = i
            else:
                a.append(i)
            obj+=1
    out.write(str(a[0]))
