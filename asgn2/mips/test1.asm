.data
a: .word 0
.text
main:
line1: li $t0,40
move $t0,$t0
sw $t0,a
line2: lw $t0,a
li $t1,5
add $t0,$t0,$t1
sw $t0,a
line2: lw $t0,a
li $t1,50
ble $t0,$t1,line2
line3: li $v0,1
move $a0,$t0
syscall
sw $t0,a
