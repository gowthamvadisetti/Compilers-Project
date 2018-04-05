.data
f_a: .word 0
dd: .word 0
f_t0: .word 0
g_cc: .word 0
g_bb: .word 0
g_t0: .word 0
.text
main:
li $t0,100
move $a0,$t0
sub $sp, $sp,12
sw $a0,4($sp)
jal g
sw $v0,dd
lw $t0,dd
li $v0,1
move $a0,$t0
syscall
li $v0,10
syscall
f:
lw $t1,f_a
sw $ra,0($sp)
move $t1,$a0
li $t2,2
mult $t1,$t2
mflo $t2
move $v0,$t2
lw $ra,0($sp)
sw $v0,8($sp)
addi $sp,$sp,12
jr $ra
lw $ra,0($sp)
sw $v0,8($sp)
addi $sp,$sp,12
jr $ra
g:
lw $t3,g_bb
sw $ra,0($sp)
move $t3,$a0
move $a0,$t3
sub $sp, $sp,12
sw $a0,4($sp)
jal f
sw $v0,g_cc
lw $t4,g_cc
li $t5,3
mult $t4,$t5
mflo $t5
move $v0,$t5
lw $ra,0($sp)
sw $v0,8($sp)
addi $sp,$sp,12
jr $ra
lw $ra,0($sp)
sw $v0,8($sp)
addi $sp,$sp,12
jr $ra
