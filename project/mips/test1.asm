.data
dd: .word 0
f_t1: .word 0
f_t0: .word 0
f_t2: .word 0
num: .word 0
f_n: .word 0
f_a: .word 0
.text
main:
li $t0,5
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
li $t3,0
ble $t2,$t3,l0
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
lw $t4,f_t1
sub $sp, $sp,4
sw $t4,0($sp)
sub $sp, $sp,4
sw $t3,0($sp)
sub $sp, $sp,4
sw $t2,0($sp)
li $t5,1
sub $t4,$t2,$t5
move $a0,$t4
sub $sp, $sp,12
sw $a0,4($sp)
jal f
sw $v0,f_a
lw $t2,0($sp)
addi $sp, $sp,4
lw $t3,0($sp)
addi $sp, $sp,4
lw $t4,0($sp)
addi $sp, $sp,4
lw $t5,f_a
mult $t2,$t5
mflo $t6
move $v0,$t6
sw $v0,8($sp)
lw $ra,0($sp)
addi $sp,$sp,12
jr $ra
lw $ra,0($sp)
addi $sp,$sp,12
jr $ra
