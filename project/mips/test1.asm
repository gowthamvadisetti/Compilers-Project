.data
e: .word 0
f_n: .word 0
f_t0: .word 0
f_a: .word 0
f_c: .word 0
g_m: .word 0
g_t0: .word 0
g_d: .word 0
.text
main:
li $t0,5
move $a0,$t0
sub $sp, $sp,12
sw $a0,4($sp)
jal f
sw $v0,e
lw $t0,e
li $v0,1
move $a0,$t0
syscall
lw $ra,0($sp)
addi $sp,$sp,12
jr $ra
li $v0,10
syscall
f:
lw $t1,f_n
sw $ra,0($sp)
move $t1,$a0
li $t2,1
sub $t2,$t1,$t2
move $t3,$t2
move $a0,$t3
sub $sp, $sp,12
sw $a0,4($sp)
jal g
sw $v0,f_c
lw $t4,f_c
move $v0,$t4
sw $v0,8($sp)
lw $ra,0($sp)
addi $sp,$sp,12
jr $ra
lw $ra,0($sp)
addi $sp,$sp,12
jr $ra
g:
lw $t5,g_m
sw $ra,0($sp)
move $t5,$a0
li $t6,1
sub $t6,$t5,$t6
move $t7,$t6
move $v0,$t7
sw $v0,8($sp)
lw $ra,0($sp)
addi $sp,$sp,12
jr $ra
lw $ra,0($sp)
addi $sp,$sp,12
jr $ra
