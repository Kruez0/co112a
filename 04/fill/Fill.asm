// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
@8192 
D=A
@0
M=D 
@24576
D=M
@18
D;JNE 
@0 
D=M 
M=M-1 
@0
D;JEQ 
@16383
A=D+A 
M=0 
@8
0;JMP 
@0 
D=M
M=M-1
@0
D;JEQ
@24576
A=A-D 
M=-1 
@18
0;JMP 