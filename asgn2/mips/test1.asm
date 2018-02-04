.data
a: .word 0
e: .word 0
d: .word 0
f: .word 0
c: .word 0
.text
main:
li $t0,2
move $t1,$t0
add $t2,$t1,$t0
add $t3,$t2,$t1
add $t4,$t3,$t2
add $t5,$t4,$t2
li $v0,1
move $a0,$t5
syscall
