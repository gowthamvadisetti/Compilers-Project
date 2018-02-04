.data
a: .word 0
e: .word 0
.text
main:
li $t0,2
move $t0,$t0
jal foo
jr $ra
foo:
li $t1,21
move $t1,$t1
li $v0,1
move $a0,$t1
syscall
jr $ra
sw $t1,e
sw $t0,a
