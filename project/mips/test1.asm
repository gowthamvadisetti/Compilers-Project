.data
f_a: .word 0
.text
main:
sub $sp, $sp,12
sw $a0,4($sp)
jal f
li $v0,10
syscall
f:
sw $ra,0($sp)
li $t0,1
li $v0,1
move $a0,$t0
syscall
lw $ra,0($sp)
addi $sp,$sp,12
jr $ra
