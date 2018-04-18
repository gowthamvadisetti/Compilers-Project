.data
jj: .word 0
t0: .word 0
t1: .word 0
t3: .word 0
t2: .word 0
.text
main:
li $t0,0
li $t1,0
li $t2,5
move $t3,$t1
l0:
bge $t3,$t1,l3
j l2
l3:
ble $t3,$t2,l1
j l2
l1:
li $t4,1
add $t4,$t0,$t4
move $t0,$t4
li $t5,1
add $t3,$t3,$t5
j l0
l2:
li $v0,1
move $a0,$t0
syscall
li $t0,10
li $v0,10
syscall
