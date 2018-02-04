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
<<<<<<< HEAD

  x.a = 'a';
  x.b = 47114711;
  x.c = 'c';
  x.d = 1234;
  x.e = 3.141592897932;
  x.f = '*';
  x.name = "abc";
  
=======
x.a = 'a';
x.b = 47114711;
x.c = 'c';
x.d = 1234;
x.e = 3.141592897932;
x.f = '*';
x.name = "abc";
>>>>>>> ba9ecf6fa0171fb55c0bedfa647e2183eaa02400
end


k = T.new
f(k)



