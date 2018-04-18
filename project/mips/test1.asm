.data
a: .word 0
t0: .word 0
c: .word 0
t1: .word 0
d: .word 0
.text
main:
li $t0,2
li $t1,10
sll $a0,$t1,2
li $v0,9
syscall
sw $v0,t0
lw $t1,t0
move $t2,$t1
add $t3,$t0,$t2
move $t4,$t3
li $v0,1
move $a0,$t4
syscall
li $v0,10
syscall
