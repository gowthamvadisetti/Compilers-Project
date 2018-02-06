.data
a: .word 0
c: .word 0
d: .word 0
.text
main:
line1: 
li $t0,2
move $t0,$t0
line2: 
la $t1,a
line3: 
li $t2,7
move $t2,$t2
line4: 
sw $t2,0($t1)
line5: 
li $v0,1
move $a0,$t0
syscall
line6: 
li $v0,10
syscall
sw $t2,d
sw $t1,c
sw $t0,a
