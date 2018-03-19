def fact(places)

  a = 1
  out = 1

  while a <= places do
    out,a = out*a,a+1
  end
  puts out
end

fact (4)
