.data
f_a: .word 0
f_b: .word 0
f_t4: .word 0
dd: .word 0
f_t1: .word 0
f_t0: .word 0
f_t3: .word 0
f_t2: .word 0
num: .word 0
f_n: .word 0
.text
main:
li $t0,20
move $a0,$t0
sub $sp, $sp,12
sw $a0,4($sp)
jal f
sw $v0,dd
lw $t1,dd
li $v0,1
move $a0,$t1
syscall
li $v0,10
syscall
f:
sw $ra,0($sp)
lw $t2,f_n
move $t2,$a0
li $t3,1
beq $t2,$t3,l0
li $t3,0
j l1
l0:
li $t3,1
l1:
li $t4,0
bgt $t3,$t4,l2
j l3
l2:
li $t4,1
move $v0,$t4
sw $v0,8($sp)
lw $ra,0($sp)
addi $sp,$sp,12
jr $ra
l3:
li $t4,0
beq $t2,$t4,l4
li $t4,0
j l5
l4:
li $t4,1
l5:
li $t5,0
bgt $t4,$t5,l6
j l7
l6:
li $t5,0
move $v0,$t5
sw $v0,8($sp)
lw $ra,0($sp)
addi $sp,$sp,12
jr $ra
l7:
sub $sp, $sp,4
sw $t4,0($sp)
lw $t5,f_t2
sub $sp, $sp,4
sw $t5,0($sp)
sub $sp, $sp,4
sw $t3,0($sp)
sub $sp, $sp,4
sw $t2,0($sp)
li $t6,1
sub $t5,$t2,$t6
move $a0,$t5
sub $sp, $sp,12
sw $a0,4($sp)
jal f
sw $v0,f_a
lw $t2,0($sp)
addi $sp, $sp,4
lw $t3,0($sp)
addi $sp, $sp,4
lw $t5,0($sp)
addi $sp, $sp,4
lw $t4,0($sp)
addi $sp, $sp,4
lw $t6,f_a
sub $sp, $sp,4
sw $t6,0($sp)
sub $sp, $sp,4
sw $t5,0($sp)
lw $t7,f_t3
sub $sp, $sp,4
sw $t7,0($sp)
sub $sp, $sp,4
sw $t3,0($sp)
sub $sp, $sp,4
sw $t4,0($sp)
sub $sp, $sp,4
sw $t2,0($sp)
li $t8,2
sub $t7,$t2,$t8
move $a0,$t7
sub $sp, $sp,12
sw $a0,4($sp)
jal f
sw $v0,f_b
lw $t2,0($sp)
addi $sp, $sp,4
lw $t4,0($sp)
addi $sp, $sp,4
lw $t3,0($sp)
addi $sp, $sp,4
lw $t7,0($sp)
addi $sp, $sp,4
lw $t5,0($sp)
addi $sp, $sp,4
lw $t6,0($sp)
addi $sp, $sp,4
lw $t8,f_b
add $t9,$t6,$t8
move $v0,$t9
sw $v0,8($sp)
lw $ra,0($sp)
addi $sp,$sp,12
jr $ra
lw $ra,0($sp)
addi $sp,$sp,12
jr $ra
