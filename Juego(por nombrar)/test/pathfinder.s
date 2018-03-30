	.file	"pathfinder.c"
	.comm	test_path, 1024, 5
	.comm	path, 1024, 5
	.def	__main;	.scl	2;	.type	32;	.endef
	.section .rdata,"dr"
.LC0:
	.ascii "r+\0"
.LC1:
	.ascii "map.txt\0"
.LC2:
	.ascii "No path found\12Quitting\0"
	.text
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
	pushq	%rbp
	.seh_pushreg	%rbp
	subq	$1136, %rsp
	.seh_stackalloc	1136
	leaq	128(%rsp), %rbp
	.seh_setframe	%rbp, 128
	.seh_endprologue
	call	__main
	leaq	.LC0(%rip), %rdx
	leaq	.LC1(%rip), %rcx
	call	fopen
	movq	%rax, 952(%rbp)
	movl	$0, 1000(%rbp)
	movl	$0, 996(%rbp)
	jmp	.L2
.L11:
	movl	$0, 992(%rbp)
	jmp	.L3
.L8:
	movq	952(%rbp), %rax
	movq	%rax, %rcx
	call	fgetc
	movl	%eax, 1004(%rbp)
	cmpl	$10, 1004(%rbp)
	je	.L4
	cmpl	$-1, 1004(%rbp)
	jne	.L5
.L4:
	cmpl	$0, 1000(%rbp)
	jne	.L29
	movl	992(%rbp), %eax
	addl	$1, %eax
	movl	%eax, 1000(%rbp)
	jmp	.L29
.L5:
	movl	996(%rbp), %eax
	leal	1(%rax), %edx
	movl	992(%rbp), %eax
	leal	1(%rax), %ecx
	movl	1004(%rbp), %eax
	movl	%eax, %r8d
	movslq	%ecx, %rax
	movslq	%edx, %rdx
	salq	$5, %rdx
	leaq	1008(%rbp), %rcx
	addq	%rcx, %rdx
	addq	%rdx, %rax
	subq	$1088, %rax
	movb	%r8b, (%rax)
	addl	$1, 992(%rbp)
.L3:
	cmpl	$31, 992(%rbp)
	jle	.L8
	jmp	.L7
.L29:
	nop
.L7:
	cmpl	$-1, 1004(%rbp)
	je	.L30
	movl	996(%rbp), %eax
	addl	$1, %eax
	cltq
	movb	$88, -80(%rbp,%rax)
	movl	996(%rbp), %eax
	addl	$1, %eax
	cltq
	salq	$5, %rax
	leaq	1008(%rbp), %rcx
	addq	%rcx, %rax
	subq	$1088, %rax
	movb	$88, (%rax)
	movl	1000(%rbp), %eax
	leal	-1(%rax), %edx
	movl	996(%rbp), %eax
	addl	$1, %eax
	cltq
	movslq	%edx, %rdx
	salq	$5, %rdx
	leaq	1008(%rbp), %rcx
	addq	%rcx, %rdx
	addq	%rdx, %rax
	subq	$1088, %rax
	movb	$88, (%rax)
	movl	996(%rbp), %eax
	leal	1(%rax), %edx
	movl	1000(%rbp), %eax
	subl	$1, %eax
	cltq
	movslq	%edx, %rdx
	salq	$5, %rdx
	leaq	1008(%rbp), %rcx
	addq	%rcx, %rdx
	addq	%rdx, %rax
	subq	$1088, %rax
	movb	$88, (%rax)
	addl	$1, 996(%rbp)
.L2:
	cmpl	$31, 996(%rbp)
	jle	.L11
	jmp	.L10
.L30:
	nop
.L10:
	movb	$88, -80(%rbp)
	movl	1000(%rbp), %eax
	subl	$1, %eax
	cltq
	salq	$5, %rax
	leaq	1008(%rbp), %rcx
	addq	%rcx, %rax
	subq	$1088, %rax
	movb	$88, (%rax)
	movl	1000(%rbp), %eax
	subl	$1, %eax
	cltq
	movb	$88, -80(%rbp,%rax)
	movl	1000(%rbp), %eax
	leal	-1(%rax), %edx
	movl	1000(%rbp), %eax
	subl	$1, %eax
	cltq
	movslq	%edx, %rdx
	salq	$5, %rdx
	leaq	1008(%rbp), %rcx
	addq	%rcx, %rdx
	addq	%rdx, %rax
	subq	$1088, %rax
	movb	$88, (%rax)
	movl	$0, 980(%rbp)
	movl	$1, 976(%rbp)
	jmp	.L12
.L19:
	movl	$1, 972(%rbp)
	jmp	.L13
.L16:
	movl	972(%rbp), %eax
	cltq
	movl	976(%rbp), %edx
	movslq	%edx, %rdx
	salq	$5, %rdx
	leaq	1008(%rbp), %rcx
	addq	%rcx, %rdx
	addq	%rdx, %rax
	subq	$1088, %rax
	movzbl	(%rax), %eax
	cmpb	$73, %al
	jne	.L14
	movl	972(%rbp), %eax
	movl	%eax, 988(%rbp)
	movl	976(%rbp), %eax
	movl	%eax, 984(%rbp)
	movl	$1, 980(%rbp)
	jmp	.L15
.L14:
	addl	$1, 972(%rbp)
.L13:
	movl	972(%rbp), %eax
	cmpl	1000(%rbp), %eax
	jl	.L16
.L15:
	cmpl	$1, 980(%rbp)
	je	.L31
	addl	$1, 976(%rbp)
.L12:
	movl	976(%rbp), %eax
	cmpl	1000(%rbp), %eax
	jl	.L19
	jmp	.L18
.L31:
	nop
.L18:
	movl	$128, -84(%rbp)
	leaq	test_path(%rip), %rax
	movl	988(%rbp), %edx
	movl	%edx, (%rax)
	leaq	test_path(%rip), %rax
	movl	984(%rbp), %edx
	movl	%edx, 4(%rax)
	leaq	-84(%rbp), %rdx
	leaq	-80(%rbp), %rax
	movq	%rdx, %r8
	movl	$1, %edx
	movq	%rax, %rcx
	call	backtracking_step
	movl	-84(%rbp), %eax
	cmpl	$128, %eax
	jne	.L20
	leaq	.LC2(%rip), %rcx
	call	puts
	movl	$1, %eax
	jmp	.L28
.L20:
	movl	$1, 968(%rbp)
	jmp	.L22
.L23:
	leaq	path(%rip), %rax
	movl	968(%rbp), %edx
	movslq	%edx, %rdx
	movl	4(%rax,%rdx,8), %ecx
	leaq	path(%rip), %rax
	movl	968(%rbp), %edx
	movslq	%edx, %rdx
	movl	(%rax,%rdx,8), %eax
	cltq
	movslq	%ecx, %rdx
	salq	$5, %rdx
	leaq	1008(%rbp), %rcx
	addq	%rcx, %rdx
	addq	%rdx, %rax
	subq	$1088, %rax
	movb	$79, (%rax)
	addl	$1, 968(%rbp)
.L22:
	movl	-84(%rbp), %eax
	subl	$1, %eax
	cmpl	968(%rbp), %eax
	jg	.L23
	movq	952(%rbp), %rax
	movq	%rax, %rdx
	movl	$10, %ecx
	call	fputc
	movl	$1, 964(%rbp)
	jmp	.L24
.L27:
	movl	$1, 960(%rbp)
	jmp	.L25
.L26:
	movl	960(%rbp), %eax
	cltq
	movl	964(%rbp), %edx
	movslq	%edx, %rdx
	salq	$5, %rdx
	leaq	1008(%rbp), %rcx
	addq	%rcx, %rdx
	addq	%rdx, %rax
	subq	$1088, %rax
	movzbl	(%rax), %eax
	movsbl	%al, %eax
	movq	952(%rbp), %rdx
	movl	%eax, %ecx
	call	fputc
	addl	$1, 960(%rbp)
.L25:
	movl	1000(%rbp), %eax
	subl	$1, %eax
	cmpl	960(%rbp), %eax
	jg	.L26
	movq	952(%rbp), %rax
	movq	%rax, %rdx
	movl	$10, %ecx
	call	fputc
	addl	$1, 964(%rbp)
.L24:
	movl	1000(%rbp), %eax
	subl	$1, %eax
	cmpl	964(%rbp), %eax
	jg	.L27
	movq	952(%rbp), %rax
	movq	%rax, %rcx
	call	fclose
	movl	$0, %eax
.L28:
	addq	$1136, %rsp
	popq	%rbp
	ret
	.seh_endproc
	.globl	eval_path
	.def	eval_path;	.scl	2;	.type	32;	.endef
	.seh_proc	eval_path
eval_path:
	pushq	%rbp
	.seh_pushreg	%rbp
	movq	%rsp, %rbp
	.seh_setframe	%rbp, 0
	subq	$16, %rsp
	.seh_stackalloc	16
	.seh_endprologue
	movq	%rcx, 16(%rbp)
	movl	%edx, 24(%rbp)
	movq	%r8, 32(%rbp)
	movq	32(%rbp), %rax
	movl	(%rax), %eax
	cmpl	24(%rbp), %eax
	jg	.L33
	movl	$0, %eax
	jmp	.L34
.L33:
	movl	24(%rbp), %eax
	leal	-1(%rax), %edx
	leaq	test_path(%rip), %rax
	movslq	%edx, %rdx
	movl	4(%rax,%rdx,8), %eax
	sall	$5, %eax
	movslq	%eax, %rcx
	movl	24(%rbp), %eax
	leal	-1(%rax), %edx
	leaq	test_path(%rip), %rax
	movslq	%edx, %rdx
	movl	(%rax,%rdx,8), %eax
	cltq
	leaq	(%rcx,%rax), %rdx
	movq	16(%rbp), %rax
	addq	%rdx, %rax
	movzbl	(%rax), %eax
	cmpb	$88, %al
	jne	.L35
	movl	$0, %eax
	jmp	.L34
.L35:
	movl	$0, -4(%rbp)
	jmp	.L36
.L38:
	leaq	test_path(%rip), %rax
	movl	-4(%rbp), %edx
	movslq	%edx, %rdx
	movl	(%rax,%rdx,8), %ecx
	movl	24(%rbp), %eax
	leal	-1(%rax), %edx
	leaq	test_path(%rip), %rax
	movslq	%edx, %rdx
	movl	(%rax,%rdx,8), %eax
	cmpl	%eax, %ecx
	jne	.L37
	leaq	test_path(%rip), %rax
	movl	-4(%rbp), %edx
	movslq	%edx, %rdx
	movl	4(%rax,%rdx,8), %ecx
	movl	24(%rbp), %eax
	leal	-1(%rax), %edx
	leaq	test_path(%rip), %rax
	movslq	%edx, %rdx
	movl	4(%rax,%rdx,8), %eax
	cmpl	%eax, %ecx
	jne	.L37
	movl	$0, %eax
	jmp	.L34
.L37:
	addl	$1, -4(%rbp)
.L36:
	movl	24(%rbp), %eax
	subl	$1, %eax
	cmpl	-4(%rbp), %eax
	jg	.L38
	movl	24(%rbp), %eax
	leal	-1(%rax), %edx
	leaq	test_path(%rip), %rax
	movslq	%edx, %rdx
	movl	4(%rax,%rdx,8), %eax
	sall	$5, %eax
	movslq	%eax, %rcx
	movl	24(%rbp), %eax
	leal	-1(%rax), %edx
	leaq	test_path(%rip), %rax
	movslq	%edx, %rdx
	movl	(%rax,%rdx,8), %eax
	cltq
	leaq	(%rcx,%rax), %rdx
	movq	16(%rbp), %rax
	addq	%rdx, %rax
	movzbl	(%rax), %eax
	cmpb	$69, %al
	jne	.L39
	movl	$0, -8(%rbp)
	jmp	.L40
.L41:
	leaq	test_path(%rip), %rax
	movl	-8(%rbp), %edx
	movslq	%edx, %rdx
	movl	(%rax,%rdx,8), %ecx
	leaq	path(%rip), %rax
	movl	-8(%rbp), %edx
	movslq	%edx, %rdx
	movl	%ecx, (%rax,%rdx,8)
	leaq	test_path(%rip), %rax
	movl	-8(%rbp), %edx
	movslq	%edx, %rdx
	movl	4(%rax,%rdx,8), %ecx
	leaq	path(%rip), %rax
	movl	-8(%rbp), %edx
	movslq	%edx, %rdx
	movl	%ecx, 4(%rax,%rdx,8)
	addl	$1, -8(%rbp)
.L40:
	movl	-8(%rbp), %eax
	cmpl	24(%rbp), %eax
	jle	.L41
	movq	32(%rbp), %rax
	movl	24(%rbp), %edx
	movl	%edx, (%rax)
	movl	$0, %eax
	jmp	.L34
.L39:
	movl	$1, %eax
.L34:
	addq	$16, %rsp
	popq	%rbp
	ret
	.seh_endproc
	.globl	backtracking_step
	.def	backtracking_step;	.scl	2;	.type	32;	.endef
	.seh_proc	backtracking_step
backtracking_step:
	pushq	%rbp
	.seh_pushreg	%rbp
	movq	%rsp, %rbp
	.seh_setframe	%rbp, 0
	subq	$32, %rsp
	.seh_stackalloc	32
	.seh_endprologue
	movq	%rcx, 16(%rbp)
	movl	%edx, 24(%rbp)
	movq	%r8, 32(%rbp)
	movl	24(%rbp), %eax
	leal	-1(%rax), %edx
	leaq	test_path(%rip), %rax
	movslq	%edx, %rdx
	movl	(%rax,%rdx,8), %eax
	leal	1(%rax), %ecx
	leaq	test_path(%rip), %rax
	movl	24(%rbp), %edx
	movslq	%edx, %rdx
	movl	%ecx, (%rax,%rdx,8)
	movl	24(%rbp), %eax
	leal	-1(%rax), %edx
	leaq	test_path(%rip), %rax
	movslq	%edx, %rdx
	movl	4(%rax,%rdx,8), %ecx
	leaq	test_path(%rip), %rax
	movl	24(%rbp), %edx
	movslq	%edx, %rdx
	movl	%ecx, 4(%rax,%rdx,8)
	movl	24(%rbp), %eax
	addl	$1, %eax
	movq	32(%rbp), %rdx
	movq	%rdx, %r8
	movl	%eax, %edx
	movq	16(%rbp), %rcx
	call	eval_path
	cmpl	$1, %eax
	jne	.L43
	movl	24(%rbp), %eax
	addl	$1, %eax
	movq	32(%rbp), %rdx
	movq	%rdx, %r8
	movl	%eax, %edx
	movq	16(%rbp), %rcx
	call	backtracking_step
.L43:
	movl	24(%rbp), %eax
	leal	-1(%rax), %edx
	leaq	test_path(%rip), %rax
	movslq	%edx, %rdx
	movl	(%rax,%rdx,8), %ecx
	leaq	test_path(%rip), %rax
	movl	24(%rbp), %edx
	movslq	%edx, %rdx
	movl	%ecx, (%rax,%rdx,8)
	movl	24(%rbp), %eax
	leal	-1(%rax), %edx
	leaq	test_path(%rip), %rax
	movslq	%edx, %rdx
	movl	4(%rax,%rdx,8), %eax
	leal	-1(%rax), %ecx
	leaq	test_path(%rip), %rax
	movl	24(%rbp), %edx
	movslq	%edx, %rdx
	movl	%ecx, 4(%rax,%rdx,8)
	movl	24(%rbp), %eax
	addl	$1, %eax
	movq	32(%rbp), %rdx
	movq	%rdx, %r8
	movl	%eax, %edx
	movq	16(%rbp), %rcx
	call	eval_path
	cmpl	$1, %eax
	jne	.L44
	movl	24(%rbp), %eax
	addl	$1, %eax
	movq	32(%rbp), %rdx
	movq	%rdx, %r8
	movl	%eax, %edx
	movq	16(%rbp), %rcx
	call	backtracking_step
.L44:
	movl	24(%rbp), %eax
	leal	-1(%rax), %edx
	leaq	test_path(%rip), %rax
	movslq	%edx, %rdx
	movl	(%rax,%rdx,8), %eax
	leal	-1(%rax), %ecx
	leaq	test_path(%rip), %rax
	movl	24(%rbp), %edx
	movslq	%edx, %rdx
	movl	%ecx, (%rax,%rdx,8)
	movl	24(%rbp), %eax
	leal	-1(%rax), %edx
	leaq	test_path(%rip), %rax
	movslq	%edx, %rdx
	movl	4(%rax,%rdx,8), %ecx
	leaq	test_path(%rip), %rax
	movl	24(%rbp), %edx
	movslq	%edx, %rdx
	movl	%ecx, 4(%rax,%rdx,8)
	movl	24(%rbp), %eax
	addl	$1, %eax
	movq	32(%rbp), %rdx
	movq	%rdx, %r8
	movl	%eax, %edx
	movq	16(%rbp), %rcx
	call	eval_path
	cmpl	$1, %eax
	jne	.L45
	movl	24(%rbp), %eax
	addl	$1, %eax
	movq	32(%rbp), %rdx
	movq	%rdx, %r8
	movl	%eax, %edx
	movq	16(%rbp), %rcx
	call	backtracking_step
.L45:
	movl	24(%rbp), %eax
	leal	-1(%rax), %edx
	leaq	test_path(%rip), %rax
	movslq	%edx, %rdx
	movl	(%rax,%rdx,8), %ecx
	leaq	test_path(%rip), %rax
	movl	24(%rbp), %edx
	movslq	%edx, %rdx
	movl	%ecx, (%rax,%rdx,8)
	movl	24(%rbp), %eax
	leal	-1(%rax), %edx
	leaq	test_path(%rip), %rax
	movslq	%edx, %rdx
	movl	4(%rax,%rdx,8), %eax
	leal	1(%rax), %ecx
	leaq	test_path(%rip), %rax
	movl	24(%rbp), %edx
	movslq	%edx, %rdx
	movl	%ecx, 4(%rax,%rdx,8)
	movl	24(%rbp), %eax
	addl	$1, %eax
	movq	32(%rbp), %rdx
	movq	%rdx, %r8
	movl	%eax, %edx
	movq	16(%rbp), %rcx
	call	eval_path
	cmpl	$1, %eax
	jne	.L48
	movl	24(%rbp), %eax
	addl	$1, %eax
	movq	32(%rbp), %rdx
	movq	%rdx, %r8
	movl	%eax, %edx
	movq	16(%rbp), %rcx
	call	backtracking_step
	nop
.L48:
	nop
	addq	$32, %rsp
	popq	%rbp
	ret
	.seh_endproc
	.ident	"GCC: (GNU) 6.4.0"
	.def	fopen;	.scl	2;	.type	32;	.endef
	.def	fgetc;	.scl	2;	.type	32;	.endef
	.def	puts;	.scl	2;	.type	32;	.endef
	.def	fputc;	.scl	2;	.type	32;	.endef
	.def	fclose;	.scl	2;	.type	32;	.endef
