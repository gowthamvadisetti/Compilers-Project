.data
a: .word 0
c: .word 0
t0: .word 0
t1: .word 0
t2: .word 0
str14: .asciiz "1\n"
.text
main:
li $t0,1
li $t1,10
li $t2,1
add $t2,$t0,$t2
li $t3,1
sub $t3,$t1,$t3
move $t4,$t2
l0:
bge $t4,$t2,l3
j l2
l3:
ble $t4,$t3,l1
j l2
l1:
la $a0,str14
li $v0,4
syscall
li $t5,1
add $t4,$t4,$t5
j l0
l2:
li $v0,10
syscall
