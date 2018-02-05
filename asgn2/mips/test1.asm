.data
str1: .asciiz "Hello World\n"
str2: .asciiz "Hi again"
.text
main:
line1: 
la $a0,str1
li $v0,4
syscall
line2: 
la $a0,str2
li $v0,4
syscall