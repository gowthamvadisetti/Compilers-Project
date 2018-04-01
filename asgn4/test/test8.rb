#fibonacci program 
def fibonacci( n )
if n <= 1 return n 
fibonacci( n - 1 ) + fibonacci( n - 2 )
end 
puts (fibonacci( 9 ))
end