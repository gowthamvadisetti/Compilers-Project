bb=true
a=false
c= a&&bb
bb = true
a = false
c = ~(a&bb)
print(c)