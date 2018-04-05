.data
a: .word 0
f_a: .word 0
g_a: .word 0
.text
main:
li $t0,22
sub $sp, $sp,12
sw $a0,4($sp)
jal f
li $v0,1
move $a0,$t0
syscall
li $v0,10
syscall
f:
sw $ra,0($sp)
li $t1,1
sub $sp, $sp,12
sw $a0,4($sp)
jal g
li $v0,1
move $a0,$t1
syscall
lw $ra,0($sp)
addi $sp,$sp,12
jr $ra
g:
sw $ra,0($sp)
li $t2,45
li $v0,1
move $a0,$t2
syscall
lw $ra,0($sp)
addi $sp,$sp,12
jr $ra
