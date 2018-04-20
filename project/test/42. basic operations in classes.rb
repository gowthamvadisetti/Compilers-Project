class cric1
	a = 2
	c = 3
	e = 7
	d = c+a*e
	puts ("This is cric1 class\n")
end
class cric2
	a = 5
	c = 7
	h = a|c
end
x = cric1.new()
y = cric2.new()
x.a = 4
m = x.d+x.e
n = y.h-y.a
print (m)
puts ("\n")
print (n)
puts ("\n")

