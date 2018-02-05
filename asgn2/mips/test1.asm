.data
aa: .word 0
bb: .word 0
str1: .asciiz "enter any number\n"
str10: .asciiz "factorial of input is "
.text
main:
line1: 
la $a0,str1
li $v0,4
syscall
line2: 
lw $t0,aa
li $v0,5
syscall
move $t0,$v0
line3: 
li $t1,1
move $t1,$t1
line4: 
jal fact
fact:
line6: 
mult $t1,$t0
mflo $t1
line7: 
li $t2,1
sub $t0,$t0,$t2
line8: 
li $t2,1
ble $t0,$t2,line10
line9: 
jal fact
line9: 
jal fact
line10: 
la $a0,str10
li $v0,4
syscall
line11: 
li $v0,1
move $a0,$t1
syscall
line12: 
li $v0,10
syscall
