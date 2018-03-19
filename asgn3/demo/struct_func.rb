#!/usr/bin/ruby -w


class T

def initialize
    @a
    @b = 0
    @c = 'c'
    @d = 0
    @e = 0.00
    @name = Array.new(10)
    @f = 'a'
end

end

def f(x)
  x.a = 'a'
  x.b = 47114711
  x.c = 'c'
  x.d = 1234
  x.e = 3.141592897932
  x.f = '*'
  x.name = "abc"
end
k = T()
f(k)