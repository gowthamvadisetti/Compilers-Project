.data
cc: .word 0
arr_a: .word 0
.text
main:
sub $sp, $sp,12
sw $a0,4($sp)
jal arr
li $t0,2
li $v0,1
move $a0,$t0
syscall
li $v0,10
syscall
arr:
li $t1,10
lw $ra,0($sp)
addi $sp,$sp,12
jr $ra
