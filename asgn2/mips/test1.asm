.data
aa: .word 0
.text
main:
line1: 
li $t0,1
move $t0,$t0
line2: 
li $t1,1
add $t0,$t0,$t1
line3: 
li $v0,1
move $a0,$t0
syscall
line4: 
li $t1,100
ble $t0,$t1,line2
