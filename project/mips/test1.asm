.data
bb: .word 0
cc: .word 0
arr_dd: .word 0
t0: .word 0
arr_a: .word 0
arr_t0: .word 0
.text
main:
li $t0,2
move $a0,$t0
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
lw $t3,arr_dd
sw $ra,0($sp)
move $t3,$a0
li $t4,10
sll $a0,$t4,2
li $v0,9
syscall
sw $v0,arr_t0
lw $t4,arr_t0
move $t5,$t4
li $t6,0
li $t7,10
sw $t5,arr_a
add $t6,$t6,$t6
add $t6,$t6,$t6
add $t5,$t5,$t6
sw $t7,0($t5)
lw $t5,arr_a
move $v0,$t5
sw $v0,8($sp)
lw $ra,0($sp)
addi $sp,$sp,12
jr $ra
lw $ra,0($sp)
addi $sp,$sp,12
jr $ra
