# Simple MIPS program to test optimizer
.text
.globl main

main:
    # Inefficient code that can be optimized
    add $t0, $s0, $zero      # Can be optimized to move
    move $t1, $t0            # Redundant move
    sw $t1, 0($sp)           # Store
    lw $t2, 0($sp)           # Redundant load
    add $t3, $t2, $zero      # Another add with zero

    # Some arithmetic operations
    addi $t4, $zero, 10
    add $t5, $t4, $t3
    sub $t6, $t5, $t4

    # Exit program
    li $v0, 10              # Exit syscall
    syscall