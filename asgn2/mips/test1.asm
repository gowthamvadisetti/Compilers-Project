.data
a: .word 0
str5: .asciiz "output should be fifty five \n"
.text
main:
line1: 
li $t0,40
move $t0,$t0
line2: 
li $t1,5
add $t0,$t0,$t1
line3: 
li $v0,1
move $a0,$t0
syscall
line4: 
li $t1,50
ble $t0,$t1,line2
sw $t0,a
line5: 
la $a0,str5
li $v0,4
syscall
line6: 
lw $t0,a
li $v0,1
move $a0,$t0
syscall
line7: 
li $v0,10
syscall
sw $t0,a
