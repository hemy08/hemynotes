# CISC与RISC

## 概述

!!! note "CISC与RISC"
    两种不同的指令系统设计哲学,CISC强调硬件功能,RISC强调简化优化。

## CISC(复杂指令集计算机)

<div style="background-color: #E3F2FD; padding: 15px; margin: 10px 0; border-left: 4px solid #2196F3; border-radius: 5px;">
    <strong>CISC特点</strong>
    <ul style="margin: 5px 0;">
        <li>指令系统复杂,指令数量多(100-300条)</li>
        <li>指令格式多样,长度不固定</li>
        <li>寻址方式复杂(10种以上)</li>
        <li>指令执行时间差异大</li>
        <li>强调硬件功能强大</li>
        <li>微程序控制</li>
    </ul>
</div>

### CISC优点

!!! tip "CISC优点"
    - 功能强大,编程方便
    - 目标代码短小
    - 向后兼容性好

### CISC缺点

<div style="background-color: #E8F5E9; padding: 15px; margin: 10px 0; border-left: 4px solid #4CAF50; border-radius: 5px;">
    <strong>CISC缺点</strong>
    <ul style="margin: 5px 0;">
        <li>指令系统复杂</li>
        <li>硬件实现困难</li>
        <li>执行效率低</li>
        <li>难以优化</li>
    </ul>
</div>

**代表:** Intel x86系列

## RISC(精简指令集计算机)

!!! info "RISC特点"
    - 指令系统简单,指令数量少(30-100条)
    - 指令格式固定,长度统一
    - 寻址方式简单(2-3种)
    - 指令执行时间相近
    - 强调编译器优化
    - 硬布线控制

### RISC优点

<div style="background-color: #FFF3E0; padding: 15px; margin: 10px 0; border-left: 4px solid #FF9800; border-radius: 5px;">
    <strong>RISC优点</strong>
    <ul style="margin: 5px 0;">
        <li>指令系统简单</li>
        <li>硬件实现容易</li>
        <li>执行效率高</li>
        <li>易于流水线</li>
        <li>适合优化</li>
    </ul>
</div>

### RISC缺点

!!! warning "RISC缺点"
    - 目标代码较长
    - 编译器要求高
    - 编程相对复杂

**代表:** ARM、MIPS、RISC-V、PowerPC

## CISC与RISC对比

<div style="overflow-x: auto;">
    <table style="width: 100%; border-collapse: collapse; margin: 10px 0;">
        <tr style="background-color: #4CAF50; color: white;">
            <th style="padding: 10px; border: 1px solid #ddd;">对比项</th>
            <th style="padding: 10px; border: 1px solid #ddd;">CISC</th>
            <th style="padding: 10px; border: 1px solid #ddd;">RISC</th>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">指令数量</td>
            <td style="padding: 10px; border: 1px solid #ddd;">多(100-300)</td>
            <td style="padding: 10px; border: 1px solid #ddd;">少(30-100)</td>
        </tr>
        <tr style="background-color: #f9f9f9;">
            <td style="padding: 10px; border: 1px solid #ddd;">指令格式</td>
            <td style="padding: 10px; border: 1px solid #ddd;">多样</td>
            <td style="padding: 10px; border: 1px solid #ddd;">固定</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">寻址方式</td>
            <td style="padding: 10px; border: 1px solid #ddd;">复杂</td>
            <td style="padding: 10px; border: 1px solid #ddd;">简单</td>
        </tr>
        <tr style="background-color: #f9f9f9;">
            <td style="padding: 10px; border: 1px solid #ddd;">控制方式</td>
            <td style="padding: 10px; border: 1px solid #ddd;">微程序</td>
            <td style="padding: 10px; border: 1px solid #ddd;">硬布线</td>
        </tr>
    </table>
</div>

## 参考资料

- [CISC 百度百科](https://baike.baidu.com/item/CISC)
- [RISC 百度百科](https://baike.baidu.com/item/RISC)
