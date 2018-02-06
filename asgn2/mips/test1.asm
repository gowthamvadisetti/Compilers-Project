.data
a: .word 0
c: .word 0
.text
main:
line1: 
li $t0,2
move $t0,$t0
line2: 
la $t1,a
line3: 
li $t2,7
sw $t2,0($t1)
line4: 
li $v0,1
move $a0,$t0
syscall
line5: 
li $v0,10
syscall
sw $t1,c
sw $t0,a
