.data
a: .word 0
e: .word 0
d: .word 0
f: .word 0
c: .word 0
.text
main:
line1: 
li $t0,2
move $t0,$t0
line2: 
li $t1,8
move $t1,$t1
line3: 
mult $t0,$t1
mflo $t2
sw $t2,d
line4: 
la $t3,d
line5: 
lw $t4,0($t3)
line6: 
li $v0,1
move $a0,$t4
syscall
line7: 
li $v0,10
syscall
