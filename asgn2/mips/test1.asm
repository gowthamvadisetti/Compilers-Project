.data
a: .word 0
bb: .word 0
cc: .word 0
dd: .word 0
str3: .asciiz "enter 6 numbers \n"
.text
main:
line1: 
li $t0,6
sll $a0,$t0,2
li $v0,9
syscall
sw $v0,a
line2: 
li $t0,0
move $t0,$t0
line3: 
la $a0,str3
li $v0,4
syscall
line4: 
li $t1,1
add $t0,$t0,$t1
line5: 
li $v0,1
move $a0,$t0
syscall
line6: 
lw $t1,cc
li $v0,5
syscall
move $t1,$v0
line7: 
lw $t2,a
sw $t0,bb
add $t0,$t0,$t0
add $t0,$t0,$t0
add $t2,$t2,$t0
sw $t1,0($t2)
lw $t2,a
lw $t0,bb
line8: 
li $t3,4
ble $t0,$t3,line4
line9: 
li $t4,4
add $t4,$t4,$t4
add $t4,$t4,$t4
add $t2,$t2,$t4
lw $t3,0($t2)
lw $t2,a
line10: 
li $v0,1
move $a0,$t3
syscall
line11: 
li $v0,10
syscall
