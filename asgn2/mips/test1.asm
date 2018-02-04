.data
a: .word 0
<<<<<<< HEAD
=======
<<<<<<< HEAD
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
=======
bb: .word 0
>>>>>>> 32682947373237c91de5d177f635be037ccef798
c: .word 0
bb: .word 0
.text
main:
li $t0,2
move $t0,$t0
li $t1,7
move $t1,$t1
or $t2,$t0,$t1
li $v0,1
move $a0,$t2
syscall
sw $t2,c
sw $t1,bb
sw $t0,a
<<<<<<< HEAD
=======
>>>>>>> 624a1cdbf94ebbf4f85045db6121099387e313d4
>>>>>>> 32682947373237c91de5d177f635be037ccef798
