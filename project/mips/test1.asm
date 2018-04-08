.data
res: .word 0
t4: .word 0
t5: .word 0
t2: .word 0
t3: .word 0
t0: .word 0
t1: .word 0
jj: .word 0
str31: .asciiz "res="
.text
main:
li $t0,0
li $t1,0
li $t2,0
li $t3,9
move $t4,$t2
l0:
bge $t4,$t2,l7
j l6
l7:
ble $t4,$t3,l1
j l6
l1:
li $t5,0
li $t6,9
move $t7,$t5
l2:
bge $t7,$t5,l5
j l4
l5:
ble $t7,$t6,l3
j l4
l3:
li $t8,1
add $t1,$t1,$t8
li $t8,1
add $t7,$t7,$t8
j l2
l4:
li $t8,1
add $t4,$t4,$t8
j l0
l6:
la $a0,str31
li $v0,4
syscall
li $v0,1
move $a0,$t1
syscall
li $v0,10
syscall
