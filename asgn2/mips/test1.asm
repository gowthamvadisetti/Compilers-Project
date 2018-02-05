.data
a: .word 0
c: .word 0
.text
main:
li $t0,2
move $t0,$t0
nor $t1,$t0,$t0
li $v0,1
move $a0,$t0
syscall
li $v0,1
move $a0,$t1
syscall
li $v0,10
syscall
sw $t1,c
sw $t0,a
