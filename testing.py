direc ={
    'ahoj': 1,
    'ako':2
}
i = 5
try:
    i = direc['sa']
except:
    print('nic')

print(i)

if i:
    ahoj = "cau"

print(ahoj)

def func():
    return 1,2,3

a,b,c = func()

print(a,b,c)
arr = [[1,"ahoj"], [2, "kamo"]]
t = arr.pop()
print(t[0])