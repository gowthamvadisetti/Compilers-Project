def fact(n,n2)
if n<=0
return 1
end
temp4=n-1
a=fact(temp4,n2)
n=n+1
return n*n2*a
end
num=5
num2=2
dd=fact(num,num2)
print(dd)