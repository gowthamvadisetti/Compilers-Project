#!/usr/bin/ruby -w


class T

  def initialize
    @a = 'a'
    @b = 0
    @c = 'c'
    @d = 0
    @e = 0.00
    @name = Array.new(10)
    @f = 'a'
  end

end

def f(x)

  
  puts x.inspect
end


k = T.new
f(k)
puts k.inspect



