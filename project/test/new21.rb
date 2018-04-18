def fibb(num)
  a = 0
  bb = 1
  c = 1
  out=0
  while c < num-1 do
  	out=a+bb
    a = bb
    bb =out
    c = c+1
  end
  print (bb)
end
fibb(10)