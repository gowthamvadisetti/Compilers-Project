.data
a: .word 0
bb: .word 0
t0: .word 0
c: .word 0
t1: .word 0
d: .word 0
t2: .word 0
e: .word 0
t3: .word 0
f: .word 0
.text
main:
li $t0,2
li $t1,3
or $t2,$t0,$t1
move $t3,$t2
or $t4,$t0,$t1
move $t5,$t4
and $t6,$t0,$t1
move $t7,$t6
and $t8,$t0,$t1
move $t9,$t8
li $v0,1
move $a0,$t3
syscall
li $v0,1
move $a0,$t5
syscall
li $v0,1
move $a0,$t7
syscall
li $v0,1
move $a0,$t9
syscall
li $v0,10
syscall
