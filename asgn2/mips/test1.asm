.data
a: .word 0
c: .word 0
.text
main:
line1: 
li $t0,2
move $t0,$t0
line2: 
nor $t1,$t0,$t0
line3: 
li $v0,1
move $a0,$t0
syscall
line4: 
li $v0,1
move $a0,$t1
syscall
line5: 
li $v0,10
syscall
