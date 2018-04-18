.data
f: .word 0
x_chair_a: .word 0
t2: .word 0
t0: .word 0
d: .word 0
z_table_c: .word 0
y_table_a: .word 0
z_table_a: .word 0
y_table_c: .word 0
e: .word 0
t1: .word 0
x_chair_c: .word 0
.text
main:
li $t0,2
li $t1,3
li $t2,5
li $t3,7
li $t4,5
li $t5,7
li $t0,4
add $t6,$t0,$t1
move $t7,$t6
sub $t8,$t3,$t2
move $t9,$t8
sub $s0,$t5,$t0
move $s1,$s0
li $v0,1
move $a0,$t7
syscall
li $v0,1
move $a0,$t9
syscall
li $v0,1
move $a0,$s1
syscall
li $v0,10
syscall
