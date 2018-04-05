.data
fact_n2: .word 0
fact_t1: .word 0
num2: .word 0
fact_t3: .word 0
fact_t2: .word 0
fact_temp4: .word 0
fact_t0: .word 0
num: .word 0
fact_a: .word 0
fact_t4: .word 0
fact_n: .word 0
dd: .word 0
.text
main:
li $t0,5
li $t1,10
move $a0,$t0
move $a1,$t1
sub $sp, $sp,12
sw $a0,4($sp)
jal fact
sw $v0,dd
lw $t2,dd
li $v0,1
move $a0,$t2
syscall
li $v0,10
syscall
fact:
lw $t3,fact_n
sw $ra,0($sp)
move $t3,$a0
lw $t4,fact_n2
sw $ra,0($sp)
move $t4,$a1
li $t5,0
ble $t3,$t5,l0
li $t5,0
j l1
l0:
li $t5,1
l1:
li $t6,0
bgt $t5,$t6,l2
j l3
l2:
li $t6,1
move $v0,$t6
lw $ra,0($sp)
sw $v0,8($sp)
addi $sp,$sp,12
jr $ra
l3:
li $t6,1
sub $t6,$t3,$t6
move $t7,$t6
move $a0,$t7
move $a1,$t4
sub $sp, $sp,12
sw $a0,4($sp)
jal fact
sw $v0,fact_a
li $t8,1
add $t8,$t3,$t8
move $t3,$t8
mult $t3,$t4
mflo $t9
lw $s0,fact_a
mult $t9,$s0
mflo $s1
move $v0,$s1
lw $ra,0($sp)
sw $v0,8($sp)
addi $sp,$sp,12
jr $ra
lw $ra,0($sp)
sw $v0,8($sp)
addi $sp,$sp,12
jr $ra
