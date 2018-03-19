def fib(num)
  a = 0
  b = 1
  c = 1
  while c < num do
    a,b = b,a+b
    c = c+1
  end
  puts(b)
end
fib(8)