def fact(n)
if n<=0 return 1 end
a=fact(n-1)
n=n+1
return n*a
end
num=5
dd=fact(num)
print(dd)