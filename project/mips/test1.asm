.data
f_a: .word 0
f_i: .word 0
s: .word 0
k: .word 0
f_t1: .word 0
l: .word 0
t0: .word 0
f_t0: .word 0
f_jj: .word 0
f_bb: .word 0
.text
main:
li $t0,2
li $t1,2
li $t2,2
add $t2,$t0,$t2
move $a0,$t2
move $a1,$t1
sub $sp, $sp,12
sw $a0,4($sp)
jal f
sw $v0,s
lw $t3,s
li $v0,1
move $a0,$t3
syscall
li $v0,10
syscall
f:
sw $ra,0($sp)
lw $t4,f_a
move $t4,$a0
lw $t5,f_bb
move $t5,$a1
li $t6,2
add $t6,$t4,$t6
li $t7,3
add $t7,$t6,$t7
move $t8,$t7
move $t9,$t5
move $v0,$t8
sw $v0,8($sp)
lw $ra,0($sp)
addi $sp,$sp,12
jr $ra
lw $ra,0($sp)
addi $sp,$sp,12
jr $ra
