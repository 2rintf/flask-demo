class A():
    b = 1
    c = 2
    def __init__(self):
        self.b = 1;

    def p(self):
        print("sdsdss")

class B():
    a_from_B = A()

b=B()
b.a_from_B

test = A()
test.p()
print(str(test.b))

test2 = B()
temp = test2.a_from_B
test2.a_from_B.b = 100
print(temp)
print(temp.b)


print(test2.a_from_B)
B.a_from_B = 100


