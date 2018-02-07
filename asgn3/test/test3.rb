#class definition
class MyClass
    @one = 1
    def do_something
      @one = 2
    end
    def output
      puts @one
    end
  end
  instance = MyClass.new
  instance.output
  instance.do_something
  instance.output