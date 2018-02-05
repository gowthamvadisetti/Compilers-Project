.data
a: .word 0
c: .word 0
b: .word 0
.text
main:
line1: 
li $t0,10
sll $a0,$t0,2
li $v0,9
syscall
sw $v0,a
line2: 
li $t0,1
move $t0,$t0
line3: 
line4: 
line5: 
lw $t1,c
li $v0,1
move $a0,$t1
syscall
