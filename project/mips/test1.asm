.data
fibb_t1: .word 0
fibb_a: .word 0
fibb_num: .word 0
fibb_c: .word 0
fibb_out: .word 0
fibb_t3: .word 0
fibb_t2: .word 0
fibb_t0: .word 0
fibb_bb: .word 0
.text
main:
li $t0,10
move $a0,$t0
sub $sp, $sp,12
sw $a0,4($sp)
jal fibb
li $v0,10
syscall
fibb:
sw $ra,0($sp)
lw $t0,fibb_num
move $t0,$a0
li $t1,0
li $t2,1
li $t3,1
li $t4,0
l0:
li $t5,1
sub $t5,$t0,$t5
blt $t3,$t5,l1
li $t6,0
j l2
l1:
li $t6,1
l2:
li $t7,0
bgt $t6,$t7,l3
j l4
l3:
add $t7,$t1,$t2
move $t4,$t7
move $t1,$t2
move $t2,$t4
li $t8,1
add $t8,$t3,$t8
move $t3,$t8
j l0
l4:
li $v0,1
move $a0,$t2
syscall
lw $ra,0($sp)
addi $sp,$sp,12
jr $ra
