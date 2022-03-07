import re

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

print(5//2)

if 'auto' < 'auta':
    print("I ma in")

integer = 5
print(str(integer))

if 'false' < 'true':
    print("PANDO")

stack = [1,2,3,4]




print(0x45)


string = 'a032hoj&lt;ako&lt;&quot;sam&apos;as'
string = re.sub('&lt;', '<', string)
string = re.sub('&gt;', '>', string)
string = re.sub('&amp;', '&', string)
string = re.sub('&quot;', '"', string)
string = re.sub('&apos;', '\'', string)
if re.search('\\\\', string):
    print("HERE")


f = open("test.txt", "r")
string2 = f.read()


while re.search('\\\\\d{3}',string2):
    string2 = re.sub('\\\\\d{3}',chr(int(re.search('\\\\\d{3}',string2)[0][1:])),string2, count= 1 )

print(string2) 
#print(string2[0]) 

