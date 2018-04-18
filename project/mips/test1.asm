.data
i: .word 0
k: .word 0
t0: .word 0
jj: .word 0
.text
main:
li $t0,1
li $t1,1
beq $t0,$t1,l0
li $t2,0
j l1
l0:
li $t2,1
l1:
move $t3,$t2
li $v0,1
move $a0,$t3
syscall
li $v0,10
syscall
