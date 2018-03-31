a = 2
b = a
for i in 1..7
for j in 0...10
b += 1
if b == 8
b=2
break
end
end
end
if a==1
a=3
end