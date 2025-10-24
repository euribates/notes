---
title: Notas sobre CHIP-8
tags:
    - hardware
    - cpu
    - learning
---

## Arquitectura de la máquina virtual

Normalmente se considera que un sistema CHIP-8 consta de una memoria RAM
de **4 KB** (4096 bytes de 8 bits). El interprete de CHIP-8 ocupa los
primeras 512 bytes. Por esa razón, la mayoría de los programas empiezan
en la dirección 500 (0x200) y nunca acceden a direcciones por debajo de
512.

Las 256 direcciones más altas (`0xF00-0xFFF`) se reservan para la memoria
de refresco de la pantalla, y los 96 bytes anteriores (`0xEA0-0xEFF`) se
reservan para la pila de llamadas, usos internos y otras variables.

## Registros

CHIP-8 dispone de 16 registros de 8 bits, nombrados desde `V0` a `VF`.  El
registro 'VF' sirve como registro de _flags_ para determinadas operaciones, por
lo que debe evitarse su uso de forma directa. Por ejemplo, en una operación de
suma, `VF` es el _flag_ de acarreo, en las operaciones de dibujo en pantalla,
sirve para detectar colisiones.

## La pila

La pila o _stack_ solo se usa para almacenar las direcciones de regreso
de las subrutinas, cuando son llamadas.

## Timers

El CHIP-8 tiene 2 _timers_ o temporizadores. Ambos corren hacia atrás hasta
llegar a 0 y lo hacen a 60 hertz.

- Timer para Delay: este timer se usado para sincronizar los eventos de los
  juegos. Este valor puede ser escrito y leído.

- Timer para Sonido: Este timer es usado para efectos de sonidos. Cuando el
  valor **no es 0**, se escucha un _beep_.

## Entradas

La entrada consta de un teclado de tipo hexadecimal con 16 teclas desde `0`
hasta `F`. Las teclas `8`, `4`, `6` y `2` son usadas habitualmente para las
direcciones. Se usan 3 opcodes para detectar la entrada. Una se activa si la
tecla es presionada, el segundo hace lo mismo cuando la no ha sido presionada y
el tercero espera que se presione una tecla. Estos 3 opcodes se almacenan en uno
de los registros de datos.

## Gráficos y Sonido

La Resolución de Pantalla estándar es de 64×32 píxeles, y la profundidad
del color es Monocromo (solo 2 colores, en general blanco y negro). Los
gráficos se dibujan en pantalla mediante _sprites_ los cuales son de 8
pixels de ancho por 1 a 15 pixels de alto. Si un pixel del sprite está
activo, entonces se pinta el color del respectivo pixel en la pantalla;
en cambio, si no lo está, no se hace nada. El indicador de acarreo o
_carry flag_ (Registro `VF`, como vimos) se pone a 1 si cualquier pixel
de la pantalla se borra (se pasa de 1 a 0) mientras un pixel se está
pintando.

Como se explicó antes, suena un beep cuando el temporizador de sonido no
es 0. Para quien esté desarrollando un emulador o intérprete de Chip-8,
debe recordar que el sonido debe ser de un solo tono, quedando la
frecuencia de dicho tono a decisión del autor del intérprete. 

## Conjunto de instrucciones

CHIP-8 tiene **35** instrucciones, las cuales tienen un tamaño de 2
bytes. Estos opcodes se listan a continuación, en hexadecimal y con los
siguientes símbolos:

- `NNN`: Dirección
- `KK`: constante de 8-bit
- `N`: constante de 4-bit
- `X` e `Y`: registro de 4-bit
- `PC`: Contador de programa (del inglés _Program Counter_)
- `SP`: Puntero de pila (del inglés _Stack Pointer_)

| Opcode | Tipo   | Explicación     |
|--------|--------|-----------------|
| `0NNN` | `Call` | Salta a un código de rutina en NNN. Se usaba en los viejos computadores que implementaban Chip-8. Los intérpretes actuales lo ignoran |
| `00E0` | `Display` | Limpia la pantalla |
| `00EE` | `Flow` | Retorna de una subrutina. Se decrementa en 1 el _Stack Pointer_ (SP). Se establece el _Program Counter_ como la dirección donde apunta el SP en la Pila |
| `1NNN` | `Flow` | Salta a la dirección NNN. El intérprete establece el Program Counter a NNN |
| `2NNN` | `Flow` | Llama a la subrutina NNN. El intérprete incrementa el Stack Pointer, luego pone el actual PC en el tope de la Pila. El PC se establece a NNN |
| `3XNN` | `Cond` | Salta la siguiente instrucción si VX = NN. Si el contenido del registro VX es NN, incrementa el PC en 2[^1] |
| `4XKK` | `Cond` | Salta la siguiente instrucción si VX != KK. Si el contenido del registro VX **no es** KK, incrementa el PC en 2[^1] |
| `5XY0` | `Cond` | Salta la siguiente instrucción si VX = VY. Si el contenido de los registro VX y VY es el mismo, incrementa el PC en 2[^1] |
| `6XKK` | `Const` | Hace VX = KK. El intérprete coloca el valor KK dentro del registro VX |
| `7XKK` | `Const` | Hace VX = VX + KK. Suma el valor de KK al valor de VX y el resultado lo deja en VX |
| `8XY0` | `Assign` | Hace VX = VY. Almacena el valor del registro VY en el registro VX |
| `8XY1` | `BitOP` | Hace VX = VX OR VY. Realiza un OR sobre los valores de VX y VY, entonces almacena el resultado en VX |
| `8XY2` | `BitOP` | Hace VX = VX AND VY |
| `8XY3` | `BitOP` | Hace VX = VX XOR VY |
| `8XY4` | `Math` | Suma VY a VX. VF se pone a 1 cuando hay un acarreo (carry), y a 0 cuando no |
| `8XY5` | `Math` | VY se resta de VX. VF se pone a 0 cuando hay que restarle un dígito al número de la izquierda, más conocido como "pedir prestado" o borrow, y se pone a 1 cuando no es necesario |
| `8XY6` | `BitOp` | Establece VF = 1 o 0 según bit menos significativo de VX. Divide VX por 2 |
| `8XY7` | `Math` | Si VY > VX => VF = 1, sino 0. VX = VY - VX |
| `8XYE` | `BitOp` | Establece VF = 1 o 0 según bit más significativo de VX. Multiplica VX por 2 |
| `9XY0` | `Cond` | Salta a la siguiente instrucción si VX != VY |
| `ANNN` | `MEM` | Establece I = NNN |
| `BNNN` | `Flow` | Salta a la ubicación V[0]+ NNN |
| `CXKK` | `Rand` | Establece VX = un Byte Aleatorio más KK |
| `DXYN` | `Display` | Pinta un sprite en la pantalla[^2] |
| `EX9E` | `KeyOp` | Salta a la siguiente instrucción si valor de VX coincide con tecla presionad |
| `EXA1` | `KeyOp` | Salta a la siguiente instrucción si valor de VX no coincide con tecla presionada (soltar tecla) |
| `FX07` | `Timer` | Establece Vx = valor del delay timer |
| `FX0A` | `KeyOp` | Espera por una tecla presionada y la almacena en el registro |
| `FX15` | `Timer` | Establece _Delay Timer_ a VX |
| `FX18` | `Delay` | Establece _Sound Timer_ a VX |
| `FX1E` | `MEM`   | Índice = Índice + VX |
| `FX29` | `MEM`   | Establece I = VX * largo Sprite Chip-8 |
| `FX33` | `BCD`   | Guarda la representación de VX en formato humano. Poniendo las centenas en la posición de memoria I, las decenas en I + 1 y las unidades en I + 2 |
| `FX55` | `MEM`   | Almacena el contenido de V0 a VX en la memoria empezando por la dirección I |
| `FX65` | `MEM`   | Almacena el contenido de la dirección de memoria I en los registros del V0 al VX |


[^1]: El contador `PC` se incrementa automáticamente en 2 cada ciclo de reloj,
    por eso, para saltarse la siguiente instrucción, se incrementa en 2
    manualmente, lo que produce un incremento total de 4 bytes. 


[^2]: El intérprete lee `N` bytes desde la memoria, comenzando desde el
    contenido del registro `I`, y se muestra dicho byte en las posiciones
    `VX`, `VY` de la pantalla. A los _sprites_ que se pintan se le aplica `XOR`
    con lo que está en pantalla. Si esto causa que algún pixel se borre,
    el registro `VF` se pone a 1, de otra forma se pone a 0. Si el
    _sprite_ se posiciona fuera de las coordenadas de la pantalla, se le hace
    aparecer en el lado opuesto de la pantalla
