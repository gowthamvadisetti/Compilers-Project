class chair
	a = 2
	c = 3
	d = c+a
end
class table
	a = 5
	c = 7
end
x = chair.new()
y = table.new()
z = table.new()
x.a = 4
d = x.a+x.c
e = y.c-y.a
f = z.c-x.a 
h = x.d+2

print (d)
print (e)
print (f)
print (h)