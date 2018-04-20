def f(n)
if n==1 return 1 end
if n==0 return 0 end
a=f(n-1)
b=f(n-2)
return a+b
end
num =9
dd =f(num)
print(dd)