.data
a: .word 0
.text
main:
line1: 
li $t0,40
move $t0,$t0
line2: 
li $t1,5
add $t0,$t0,$t1
line3: 
li $t1,50
ble $t0,$t1,line2
line4: 
li $v0,1
move $a0,$t0
syscall
