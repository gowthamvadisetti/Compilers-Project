.data
a: .word 0
e: .word 0
g: .word 0
.text
main:
li $t0,2
move $t0,$t0
li $v0,1
move $a0,$t0
syscall
jal foo
sw $v0,g
lw $t1,g
li $v0,1
move $a0,$t1
syscall
li $v0,10
syscall
foo:
li $t2,11
move $t2,$t2
li $v0,1
move $a0,$t2
syscall
move $v0,$t2
jr $ra
syscall
sw $t2,e
sw $t1,g
sw $t0,a
