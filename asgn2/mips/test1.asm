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
add $t2,$t0,$t1
add $t3,$t2,$t0
add $t4,$t3,$t2
add $t5,$t4,$t2
li $v0,1
move $a0,$t5
syscall
li $v0,1
move $a0,$t3
syscall
