@ Este arquivo é um modelo para atividade 9/Trabalho 2
@ Você pode utilizar todo/qualquer trecho deste arquivo
@
@ Este arquivo é segmentado 4 partes (questão de legibilidade)
@   * Seção para declaração de contantes    : Onde as contantes são declaradas
@   * Seção do vetor de interrupções        : Código referente ao vetor de interrupções
@   * Seção de texto                        : Onde as rotinas são escritas
@   * Seção de dados                        : Onde são adicionadas as variáveis (.word, .skip) utilizadas neste arquivo


@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@      Seção de Constantes/Defines           @@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

@ Constantes para os Modos de operação do Processador, utilizados para trocar entre modos de operação (5 bits menos significativos)
    .set MODE_USER,                 0x10
    @ Você pode definir as outras....
    .set MODE_IRQ,                  0x12
    .set MODE_SUPERVISOR,           0x13
    .set MODE_SYSTEM,               0x1F

@ Constantes referentes aos endereços
    .set USER_ADDRESS,              0x77812000      @ Endereço do código de usuário
    .set STACK_POINTER_IRQ,         0x7E000000      @ Endereço inicial da pilha do modo IRQ
    .set STACK_POINTER_SUPERVISOR,  0x7F000000      @ Endereço inicial da pilha do modo Supervisor
    .set STACK_POINTER_USER,        0x80000000      @ Endereço inicial da pilha do modo Usuário

@ Constantes Referentes ao TZIC
    .set TZIC_BASE,                 0x0FFFC000
    .set TZIC_INTCTRL,              0x00
    .set TZIC_INTSEC1,              0x84
    .set TZIC_ENSET1,               0x104
    .set TZIC_PRIOMASK,             0x0C
    .set TZIC_PRIORITY9,            0x424

@ Constantes Referentes ao GPT
    .set GPT_CR,                    0x53FA0000
    .set GPT_PR,                    0x53FA0004
    .set GPT_SR,                    0x53FA0008
    .set GPT_OCR1,                  0x53FA0010
    .set GPT_IR,                    0x53FA000C

@ Constantes Referentes ao GPIO
    .set GPIO_DR,                   0x53F84000
    .set GPIO_GDIR,                 0x53F84004
    .set GPIO_PSR,                  0x53F84008


@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@      Seção do Vetor de Interrupções        @@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@ Este vetor possui entradas das rotinas para o tratamento de cada tipo de interrupção
.align 4
.org 0x0                    @ 0x0 --> salto para rotina de tratamento do RESET
.section .iv,"a"
_start:
interrupt_vector:
    b reset_handler        @ Rotina utilizada para interrupção RESET

.org 0x08                  @ 0x8 --> salto para rotina de tratamento de syscalls (interrupções svc)
    b svc_handler          @ Rotina utilizada para interrupção SVC

.org 0x18                  @ 0x18 --> salto para rotina de tratamento de interrupções do tipo IRQ
    b irq_handler          @ Rotina utilizada para interrupção IRQ (GPT, ...)



@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@      Seção de Texto                        @@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

.org 0x100
.text

@ Rotina de tratamento da interrupção RESET.
@ Esta rotina é unicamente invocada assim que o processador é iniciado (interrupção reset). O processador é iniciado no modo de operação de sistema, com as flags zeradas e as INTERRUPÇÕES DESABILITADAS!
@ Esta rotina é utilizada para configurar todo o sistema, antes de executar o código de usuário (ronda, segue-parede), que esta localizado em USER_ADDRESS.
@ Uma vez que o código de usuário é executado, syscalls são utilizadas para voltar aos modo de operação de sistema.
@
@ Essa rotina deve configurar:
@   1)  Inicializar o contador de tempo (variável contador) e o endereço base do vetor de interrupções no coprocessador p15    -- (OK)
@
@   2)  Inicializar as pilhas dos modos de operação
@          * Alterar o registrador sp, dos modos IRQ e SVC (cada modo tem seus próprios registradores!), com endereços definidos. Assim, sempre que chavearmos de modo, este tera um endereço para sua pilha, separadamente.
@          * Lembre-se que, o registrador CPRS (que pode ser acessado por instruções mrs/msr) contém o modo de operação atual do processador. Para trocar de modo, basta escrever os bits referentes ao novo modo, no CPRS. Apenas o modo de operação USER possui restrições quanto a escrever no CPRS. Para retornar a um modo de operação de sistema, o usuário deve realizar uma syscall (que é tratada pelo svc_handler)
@
@   3)  Configurar os dispositivos:
@          * Configurar o GPT para gerar uma interrupção do tipo IRQ (que será tratada por irq_handler) assim que o contador atingir um valor definido. O GPT é um contador de propósito geral e deve-se configurar a frequencia e o valor que será contado. Cada interrupção gerada deste contador representa uma unidade de tempo do seu sistema (quanto mais alto ou baixo o valor de contagem, seu tempo passará mais rapído ou devagar)
@          * Configurar GPIO: Definir em GDIR quais portas do GPIO são de entrada e saída.
@
@   4)  Configurar o TZIC (Controlador de Interrupções)         -- (OK)
@          * Após configurar as interrupções dos dispositivos, a configuração do TZIC deve ser realizada para permitir que as interrupções dos periféricos cheguem a CPU.
@          * Nesta parte, estamos cadastrando as interrupcões do GPT como habilitadas para o TZIC
@
@   5)  Habilitar interrupções e executar o código do usuário
@           * Uma vez que o sistema foi configurado, devemos executar (saltar para) o código do usuário (segue-parede/ronda), que esta localizado em USER_ADDRESS
@           * Lembre-se também de habilitar as interrupções antes de executar o código usuário. Para habilitar as interrupções escreva nos bits do CPRS (bit de IRQ e FIQ. Feito isso, as interrupções cadastradas no TZIC irão interromper o processador, que irá parar o que estiver fazendo, chavear de modo e executar a rotina de tratamento adequada para cada interrupção.
@           * Uma vez que o código de usuário é executado, a rotina reset_handler não é mais usada (até reinicar). Apenas as rotinas irq_handler (para interrupções do GPT) e svc_handler (para syscalls feitas pelo usuário) são utilizadas.

reset_handler:
@   1) ----------- Inicialização do contador e do IV -------------------------
    @ zera contador de tempo
    mov r0, #0
    ldr r1, =counter
    str r0, [r1]
    @Faz o registrador que aponta para a tabela de interrupções apontar para a tabela interrupt_vector
    ldr r0, =interrupt_vector @ carrega vetor de interrupcoes
    mcr p15, 0, r0, c12, c0, 0 @ no co-processador 15

@   2) ----------- Inicialização das pilhas modos de operação  ---------------
    @ Você pode inicializar as pilhas aqui (ou, pelo menos, antes de executar o código do usuário)
    @ Inicializa a pilha do modo SVC
    MRS    R0, CPSR                    @ Read the CPSR
    BIC    R0, R0, #0x1F               @ Clear the mode bits
    ORR    R0, R0, #0x13               @ Set the mode bits to FIQ mode
    MSR    CPSR_c, R0                  @ Update the control bits in the CPSR
                                       @ now in SVC mode    @ inicializar a pilha
    ldr r13, =STACK_POINTER_SUPERVISOR

    @ Inicializa a pilha do modo IRQ
    MRS    R0, CPSR                    @ Read the CPSR
    BIC    R0, R0, #0x1F               @ Clear the mode bits
    ORR    R0, R0, #0x12               @ Set the mode bits to FIQ mode
    MSR    CPSR_c, R0                  @ Update the control bits in the CPSR
                                       @ now in FIQ mode    @ inicializar a pilha
    ldr r13, =STACK_POINTER_IRQ

@    3) ----------- Configuração dos periféricos (GPT/GPIO) -------------------
    @ Configuração GPT
    mov r3, #0x41
    ldr r0, =GPT_CR
    str r3, [r0]

    mov r3, #0x0
    ldr r0, =GPT_PR
    str r3, [r0]

    mov r3, #100
    ldr r0, =GPT_OCR1
    str r3, [r0]

    mov r3, #0x1
    ldr r0, =GPT_IR
    str r3, [r0]

    @ Configuração GPIO
    ldr r0, =GPIO_GDIR
    ldr r1, =0xFFFC003E
    str r1, [r0] 

    ldr r0, =GPIO_DR
    mov r1, #0x0
    str r1, [r0]

@    4) ----------- Configuração do TZIC  -------------------------------------
    @ Liga o controlador de interrupcoes
    @ R1 <= TZIC_BASE
    ldr r1, =TZIC_BASE

    @ Configura interrupcao 39 do GPT como nao segura
    mov r0, #(1 << 7)
    str r0, [r1, #TZIC_INTSEC1]

    @ Habilita interrupcao 39 (GPT)
    @ reg1 bit 7 (gpt)
    mov r0, #(1 << 7)
    str r0, [r1, #TZIC_ENSET1]

    @ Configure interrupt39 priority as 1
    @ reg9, byte 3
    ldr r0, [r1, #TZIC_PRIORITY9]
    bic r0, r0, #0xFF000000
    mov r2, #1
    orr r0, r0, r2, lsl #24
    str r0, [r1, #TZIC_PRIORITY9]

    @ Configure PRIOMASK as 0
    eor r0, r0, r0
    str r0, [r1, #TZIC_PRIOMASK]

    @ Habilita o controlador de interrupcoes
    mov r0, #1
    str r0, [r1, #TZIC_INTCTRL]

    @ habilita interrupções
    ldr r0, =MODE_SUPERVISOR
    msr CPSR_c, r0

@    5) ----------- Execução de código de usuário -----------------------------
    @ Inicializa a pilha do modo USER
    MRS    R0, CPSR                    @ Read the CPSR
    BIC    R0, R0, #0x1F               @ Clear the mode bits
    ORR    R0, R0, #0x10               @ Set the mode bits to USER mode
    MSR    CPSR_c, R0                  @ Update the control bits in the CPSR
                                       @ now in USER mode    @ inicializar a pilha
    ldr r13, =STACK_POINTER_USER
    ldr r4, =USER_ADDRESS
    bx r4


@   Rotina para o tratamento de chamadas de sistemas, feitas pelo usuário
@   As funções na camada BiCo fazem syscalls que são tratadas por essa rotina
@   Esta rotina deve, determinar qual syscall foi realizada e realizar alguma ação (escrever nos motores, ler contador de tempo, ....)
svc_handler:
    push {lr}
    cmp r7, #21
    bleq read_sonar
    cmp r7, #20 
    bleq set_motor_speed
    cmp r7, #17
    bleq get_time
    cmp r7, #18
    bleq set_time

   
    pop {lr}
    movs pc, lr

@   Rotina para o tratamento de interrupções IRQ
@   Sempre que uma interrupção do tipo IRQ acontece, esta rotina é executada. O GPT, quando configurado, gera uma interrupção do tipo IRQ. Neste caso, o contador de tempo pode ser incrementado (este incremento corresponde a 1 unidade de tempo do seu sistema)
irq_handler:
    push {r0-r3}
    ldr r0, =counter
    ldr r1, [r0]
    add r1, r1, #1
    str r1, [r0]

    sub lr, lr, #4

    mov r3, #0x1
    ldr r2, =GPT_SR
    str r3, [r2]
    pop {r0-r3}
    movs pc, lr

read_sonar:
    mov r1,r0
    mov r0,#-1
    
    cmp r1,#15
    bhi end_read_sonar
    
    ldr r0,=GPIO_DR
    ldr r2,[r0]
    ldr r3,=0x3C
    bic r2, r2, r3
    lsl r1, r1, #2
    orr r2, r2, r1
    str r2, [r0]

    ldr r2,[r0]
    bic r2, r2, #0x2
    str r2, [r0]

    ldr r2, =100
    loop1_read_sonar:
        cmp r2, #0
        sub r2, r2, #1
        bhi loop1_read_sonar

    ldr r2,[r0]
    ldr r3,=0x2
    bic r2, r2, r3
    orr r2, r2, #2
    str r2, [r0]

    ldr r2, =100
    loop2_read_sonar:
        cmp r2, #0
        sub r2, r2, #1
        bhi loop2_read_sonar

    ldr r2,[r0]
    bic r2, r2, #0x2
    str r2, [r0]

    loop3_read_sonar:
        ldr r0,=GPIO_DR
        ldr r2,[r0]
        ldr r3, =0xfffffffe
        bic r2, r2, r3
        cmp r2, #1
        bne loop3_read_sonar

    ldr r2,[r0]
    ldr r3,=0xfffc003f
    bic r2, r2, r3
    lsr r2, r2, #6
    mov r0, r2

    end_read_sonar:
        mov pc, lr

set_motor_speed:
    cmp r0, #0
    beq dir_set_motor_speed
    cmp r0, #1
    beq esq_set_motor_speed
    mov r0, #-1

    b end_set_motor_speed
    esq_set_motor_speed:
        mov r0, #-2
        cmp r1, #63
        bhi end_set_motor_speed

        ldr r0, =GPIO_DR
        ldr r2, [r0]
        ldr r3, =0xFE000000
        bic r2, r2, r3
        lsl r1, r1, #26
        orr r2, r2, r1
        str r2, [r0] 

        mov r0, #0
        b end_set_motor_speed

    dir_set_motor_speed:
        mov r0, #-2
        cmp r1, #63
        bhi end_set_motor_speed

        ldr r0, =GPIO_DR
        ldr r2, [r0]
        ldr r3, =0x1FC0000
        bic r2, r2, r3
        lsl r1, r1, #19
        orr r2, r2, r1
        str r2, [r0] 

        mov r0, #0
        b end_set_motor_speed

end_set_motor_speed:
    mov pc, lr

get_time:
    ldr r0, =counter 
    ldr r0, [r0]   
    mov pc, lr

set_time:
    ldr r1, =counter
    str r0, [r1]
    mov pc, lr

@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@      Seção de Dados                        @@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@ Nesta seção ficam todas as váriaveis utilizadas para execução do código deste arquivo (.word / .skip)
.align 4
.data
counter: .word 0x00000000
