.data
a: .word 0
<<<<<<< HEAD
e: .word 0
d: .word 0
f: .word 0
c: .word 0
=======
>>>>>>> adfd2f66381806925e4c3d517231d50a16fa3661
.text
main:
line1: 
li $t0,40
move $t0,$t0
line2: 
<<<<<<< HEAD
li $t1,8
move $t1,$t1
line3: 
mult $t0,$t1
mflo $t2
sw $t2,d
=======
li $t1,5
add $t0,$t0,$t1
line3: 
li $t1,50
ble $t0,$t1,line2
>>>>>>> adfd2f66381806925e4c3d517231d50a16fa3661
line4: 
la $t3,d
line5: 
lw $t4,0($t3)
line6: 
li $v0,1
<<<<<<< HEAD
move $a0,$t4
syscall
line7: 
li $v0,10
=======
move $a0,$t0
>>>>>>> adfd2f66381806925e4c3d517231d50a16fa3661
syscall
