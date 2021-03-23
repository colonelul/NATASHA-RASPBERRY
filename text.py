a = 1
def test1():
    global a
    a+=1

def test2():
    global a
    a+=1
    print(a)

test1()
test2()
