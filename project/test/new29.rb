class chair
a = 2
c = 3
end
class table
a = 5
c = 7
end
x = chair()
y = table()
z = table()
x.a = 4
d = x.a+x.c
e = y.c-y.a
f = z.c-x.a
print (d)
print (e)
print (f)