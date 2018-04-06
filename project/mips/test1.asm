.data
bb: .word 0
cc: .word 0
t0: .word 0
arr_a: .word 0
arr_t0: .word 0
.text
main:
sub $sp, $sp,12
sw $a0,4($sp)
jal arr
sw $v0,bb
lw $t1,bb
li $t2,0
sw $t1,bb
add $t2,$t2,$t2
add $t2,$t2,$t2
add $t1,$t1,$t2
lw $t0,0($t1)
lw $t1,bb
move $t2,$t0
li $v0,1
move $a0,$t2
syscall
li $v0,10
syscall
arr:
sw $ra,0($sp)
li $t3,10
sll $a0,$t3,2
li $v0,9
syscall
sw $v0,arr_t0
lw $t3,arr_t0
move $t4,$t3
li $t5,0
li $t6,10
sw $t4,arr_a
add $t5,$t5,$t5
add $t5,$t5,$t5
add $t4,$t4,$t5
sw $t6,0($t4)
lw $t4,arr_a
move $v0,$t4
sw $v0,8($sp)
lw $ra,0($sp)
addi $sp,$sp,12
jr $ra
lw $ra,0($sp)
addi $sp,$sp,12
jr $ra
