.data
a: .word 0
bb: .word 0
cc: .word 0
.text
main:
line1: 
li $t0,10
sll $a0,$t0,2
li $v0,9
syscall
sw $v0,a
line2: 
li $t0,5
move $t0,$t0
line3: 
lw $t1,a
li $t2,1
add $t2,$t2,$t2
add $t2,$t2,$t2
add $t1,$t1,$t2
sw $t0,0($t1)
lw $t1,a
line4: 
li $t3,1
add $t3,$t3,$t3
add $t3,$t3,$t3
add $t1,$t1,$t3
lw $t2,0($t1)
lw $t1,a
line5: 
li $v0,1
move $a0,$t2
syscall
