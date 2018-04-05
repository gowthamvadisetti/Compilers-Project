def fact(n)
if n<=0
return 1
end
temp4=n-1
a=fact(temp4)
n=n+1
return n*a
end
num=5
dd=fact(num)
print(dd)