.data
a: .word 0
bb: .word 0
c: .word 0
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
