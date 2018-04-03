def fact(places)

  a = 1
  out = 1

  while a <= places do
    out = out*a
    a = a+1
  end
  print(out)
end
puts("enter number ")
gets(num)
puts("factorial  =")
fact (num)
