.data
a: .word 0
bb: .word 0
*bb: .word 0
.text
main:
line1: 
li $t0,1
move $t0,$t0
line2: 
la $t1,a
line3: 
li $t2,2
move $t2,$t2
line4: 
li $v0,1
move $a0,$t0
syscall
sw $t2,*bb
sw $t1,bb
sw $t0,a
