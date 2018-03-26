def fib(n)
	if n==1
		1
	elsif n==2
		1
	else
		fib(n-1) + fib(n-2)
	end
end	

puts "fibbonacci sum is: #{fib(8)}"