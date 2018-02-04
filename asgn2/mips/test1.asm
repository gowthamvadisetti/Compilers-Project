.data
a: .word 0
d: .word 0
c: .word 0
.text
main:
li $t0,2
move $t0,$t0
li $t1,8
move $t1,$t1
mult $t0,$t1
mflo $t2
li $v0,1
move $a0,$t2
syscall
jr $ra
jal foo
foo:
jr $ra
sw $t2,d
sw $t1,c
sw $t0,a
