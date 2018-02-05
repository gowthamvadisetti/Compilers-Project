.data
aa: .word 0
bb: .word 0
cc: .word 0
dd: .word 0
.text
main:
line1: 
li $t0,1
move $t0,$t0
line2: 
li $t1,0
move $t1,$t1
line3: 
li $t2,0
move $t2,$t2
line4: 
li $t3,0
move $t3,$t3
line5: 
add $t3,$t0,$t1
line6: 
move $t1,$t0
line7: 
move $t0,$t3
line8: 
li $t4,1
add $t2,$t2,$t4
line9: 
li $t4,10
ble $t2,$t4,line5
line10: 
li $v0,1
move $a0,$t0
syscall
line11: 
li $v0,10
syscall
