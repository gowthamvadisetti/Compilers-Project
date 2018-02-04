.data
a: .word 0
d: .word 0
f: .word 0
i: .word 0
h: .word 0
k: .word 0
c: .word 0
p: .word 0
b: .word 0
e: .word 0
.text
main:
li $t0,2
move $t0,$t0
li $t1,3
move $t1,$t1
li $t2,4
move $t2,$t2
li $t3,4
move $t3,$t3
move $t4,$t1
mult $t4,$t0
mflo $t4add $t4,$t0,$t1
lw $t5,f
li $v0,5
syscall
move $t5,$v0
add $t6,$t5,$t2
add $t7,$t1,$t3
mult $t0,$t5
mflo $t8div $t1,$t7
mflo $t9li $v0,1
move $a0,$t9
syscall
sw $t9,k
sw $t8,p
sw $t3,d
sw $t2,c
sw $t1,b
sw $t0,a
sw $t7,i
sw $t6,h
sw $t5,f
sw $t4,e
