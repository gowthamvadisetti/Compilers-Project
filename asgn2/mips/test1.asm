.data
a: .word 0
c: .word 0
d: .word 0
bb: .word 0
i: .word 0
h: .word 0
k: .word 0
f: .word 0
p: .word 0
e: .word 0
.text
main:
li $t0,3
move $t0,$t0
li $t1,4
move $t1,$t1
li $t2,4
move $t2,$t2
move $t3,$t0
li $t4,2
lw $t4,a
mult $t4,$t4
mflo $t3
add $t3,$t4,$t0
lw $t5,f
li $v0,5
syscall
move $t5,$v0
add $t6,$t5,$t1
add $t7,$t0,$t2
mult $t0,$t5
mflo $t8
div $t0,$t7
mflo $t9
li $v0,1
move $a0,$t8
syscall
sw $t9,k
sw $t8,p
sw $t3,e
sw $t2,d
sw $t1,c
sw $t0,bb
sw $t7,i
sw $t6,h
sw $t5,f
sw $t4,a
