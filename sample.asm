MAIN:
    MVRD R0, 25
    MVRD R1, 6
    MVRD R2, 0
    MVRD R3, 8

LOOP:
    MVRD R4,1
    AND R4,R1
    JRZ 1F
    ADD R2,R0
1F:
    SHL R0 ; 逻辑左移一位
    SHR R1 ; 逻辑右移一位
    DEC R3
    JRNZ LOOP
1B:
    JR 1B ; 跳转到往后第一个1标号处
