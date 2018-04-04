def fibo(n)
# print(n)
if n==0
temp1=1
return temp1
end
temp4=n-1
a=fibo(temp4)
n=n+1
temp5=a*2
return temp5
end
num=1
dd=fibo(num)
print(dd)