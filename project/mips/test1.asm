.data
fact_t0: .word 0
fact_t1: .word 0
fact_t3: .word 0
fact_t2: .word 0
dd: .word 0
num: .word 0
fact_a: .word 0
fact_n: .word 0
.text
main:
li $t0,5
move $a0,$t0
sub $sp, $sp,12
sw $a0,4($sp)
jal fact
sw $v0,dd
lw $t1,dd
li $v0,1
move $a0,$t1
syscall
li $v0,10
syscall
fact:
sw $ra,0($sp)
lw $t2,fact_n
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
li $t4,1
sub $t4,$t2,$t4
move $a0,$t4
sub $sp, $sp,12
sw $a0,4($sp)
jal fact
sw $v0,fact_a
li $t5,1
add $t5,$t2,$t5
move $t2,$t5
lw $t6,fact_a
mult $t2,$t6
mflo $t7
move $v0,$t7
sw $v0,8($sp)
lw $ra,0($sp)
addi $sp,$sp,12
jr $ra
lw $ra,0($sp)
addi $sp,$sp,12
jr $ra
