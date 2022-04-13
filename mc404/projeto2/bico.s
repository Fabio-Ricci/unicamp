.org 0x0
.align 4
.text
.globl set_motor_speed
.globl read_sonar
.globl set_time
.globl get_time

set_motor_speed:
	push {lr}
	mov r7, #20
	ldrb r2, [r0]
	ldrb r1, [r0, #1]
	mov r0, r2
	svc 0x0
	pop {lr}
	mov pc, lr

read_sonar:
	push {lr}
	mov r7, #21
	svc 0x0
	pop {lr}
	mov pc, lr

get_time:
	push {lr}
	mov r7, #17
	svc 0x0
	pop {lr}
	mov pc, lr

set_time:
	push {lr}
	mov r7, #18
	svc 0x0
	pop {lr}
	mov pc, lr
