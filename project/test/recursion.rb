def f(n)
	if n<=0 return 1 end
	a =f(n-1)
	return n*a
end
num =5
dd =f(num)
print(dd)