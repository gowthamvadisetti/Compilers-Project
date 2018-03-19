class Tables
  def initialize(v)
    @val = v
  end
  def set(v)
    @val = v
  end
  def get
    return @val
  end
  def increment
    @val += 1
  end
  def to_s
    return "Tables(val=" + @val + ")"
  end
end
class Chairs < Tables
  def initialize(x)
    inherit(x)
  end
end
a = Tables(621)
b = Chairs(144)
a.increment
b.increment
print(a, b,"\n")