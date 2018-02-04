.data
a: .word 0
e: .word 0
d: .word 0
f: .word 0
c: .word 0
.text
main:
lw $t0,a
li $v0,5
syscall
move $t0,$v0
li $t1,2
add $t1,$t0,$t1
add $t2,$t1,$t0
add $t3,$t2,$t1
add $t4,$t3,$t1
li $v0,1
move $a0,$t4
syscall
li $v0,1
move $a0,$t2
syscall
sw $t3,e
sw $t2,d
sw $t1,c
sw $t0,a
sw $t4,f
