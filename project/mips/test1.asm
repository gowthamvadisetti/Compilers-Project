.data
fibo_temp4: .word 0
dd: .word 0
fibo_a: .word 0
num: .word 0
fibo_temp1: .word 0
fibo_t1: .word 0
fibo_t0: .word 0
fibo_n: .word 0
.text
main:
li $t0,5
move $a0,$t0
sub $sp, $sp,12
sw $ra,0($sp)
sw $a0,4($sp)
jal fibo
sw $v0,dd
lw $t1,dd
li $v0,1
move $a0,$t1
syscall
li $v0,10
syscall
fibo:
lw $t2,fibo_n
sw $ra,0($sp)
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
li $t4,0
move $v0,$t4
li $v0,10
syscall
l3:
li $t5,1
sub $t5,$t2,$t5
move $t6,$t5
move $a0,$t6
sub $sp, $sp,12
sw $ra,0($sp)
sw $a0,4($sp)
jal fibo
sw $v0,fibo_a
lw $t7,fibo_a
move $v0,$t7
li $v0,10
syscall
lw $ra,0($sp)
sw $v0,8($sp)
addi $sp,$sp,12
jr $ra
