# Proyecto Aurelion

## Información General

### Tema
Fidelización de clientes mediante promociones personalizadas en la tienda virtual "Aurelion"

### Problema
La tienda virtual _Aurelion_, líder en ventas de productos de limpieza y alimentos y bebidas en Argentina, enfrenta un desafío: muchos clientes realizan compras aisladas y no vuelven a comprar con frecuencia. Esto afecta los ratios de fidelización y limita el crecimiento de las ventas recurrentes.

### Solución propuesta
Implementar un sistema de promociones personalizadas enviadas por correo electrónico a cada cliente. Estas promociones se diseñarán a partir del análisis de datos de ventas, productos adquiridos y hábitos de compra de clientes.

### Dataset de referencia

La data se obtendrá desde fuentes primarias. Específicamente, desde el registro de ventas y clientes que colecciona la misma app, así como también desde una lista de productos que manejan las tiendas. Todos los registros se encuentran en archivos .xlsx, por tanto, se tratarán datos estructurados.

Dentro de la base de datos, se cuenta con las siguientes tablas: clientes, productos, ventas y detalle de ventas.

#### Tabla `clientes`
Es una tabla que almacena el registro de los clientes que compran en Aurelion, permitiendo identificar a cada cliente y sus diferentes atributos, como correo electrónico o ciudad.

A nivel de estructura cuenta con 5 campos (id_cliente, nombre_cliente, email, ciudad, fecha_alta) y con 100 registros. Asimismo, su primary key es id_cliente. No cuenta con foreign key.

Detalle de tipo y escala de los campos:
- id_cliente (PK): numérico tipo int, nominal
- nombre_cliente: texto, nominal
- email: texto, nominal
- ciudad: texto, nominal
- fecha_alta: numérico, intervalo

#### Tabla `productos`
Informa sobre el catálogo de productos que vende la tienda a través de su app, conteniendo información básica del producto y el precio unitario para cálculos de ventas y promociones.

A nivel de estructura cuenta con 4 campos (id_producto, nombre_producto, categoria, precio_unitario) y con 100 registros. Su primary key es id_producto. No cuenta con foreign key.

Detalle de tipo y escala de los campos:
- id_producto (PK): numérico tipo int, nominal
- nombre_producto: texto, nominal
- categoria: texto, nominal
- precio_unitario: numérico tipo int, razón

#### Tabla `ventas`
Es el registro de cada transacción/venta realizada en la tienda virtual, almancenando eventos de compra (cuándo, quién compró y cómo pagó).

A nivel de estructura cuenta con 6 campos (id_venta, fecha, id_cliente, nombre_cliente, email, medio_pago) y con 120 registros. Su primary key es id_venta, mientras que el foreign key es id_cliente.

Detalle de tipo y escala de los campos:

- id_venta (PK): numérico tipo int, nominal
- fecha: numérico, intervalo
- id_cliente (FK): numérico tipo int, nominal
- nombre_cliente: texto, nominal
- email: texto, nominal
- medio_pago: texto, nominal

#### Tabla `detalle_ventas`
Es el desglose de cada venta, representando los productos vendidos de una transacción concreta.

A nivel de estructura cuenta con 6 campos (id_venta, id_producto, nombre_producto, cantidad, precio_unitario, importe) y con 343 registros. No presenta primary key. Contiene dos foreign key id_venta y id_producto

Detalle de tipo y escala de los campos:

- id_venta (FK): numérico tipo int, nominal
- id_producto (FK): numérico tipo int, nominal
- nombre_producto: texto, nominal
- cantidad: numérico tipo int, razón
- precio_unitario: numérico tipo int, razón
- importe: numérico tipo int, razón

## Programa Interactivo

### Pasos
1. **Definición de objectivos**
Crear un menú ordenado e interactivo con el cual las partes interesadas del proyecto puedan consultar de manera interactiva información sobre el mismo.

2. **Listado de subtareas y dependencias**
```
Mostrar menú principal
Solicitar ingreso de opción
    Opción 1:
    Opción 2: 
        Opción 2a: 
        Opción 2b: 
    Opción 3: 
    Opción 4: 
    Opción 5: 
    Opción 6:
```

3. **Definición entradas y salidas de cada subtarea**
```
Mostrar menú principal
    Solicitar ingreso de opción
        Entrada: entrada de usuario (1 a 6)
        Salida: opción seleccionada

        Opción 1: Extraer parrafos 1 a 3
            Entrada: entrada de usuario (1), archivo markdown
            Salida: texto de los párrafos 1 a 3.

        Opción 2: Mostrar submenú (a/b)
            Entrada: entrada de usuario (2)
            Salida: submenú con opciones a y b
            Opción 2a: Extraer párrafos 4 y 5
                Entrada: entrada de usuario (a), archivo markdown
                Salida: texto de los parrafos 4 y 5
            Opción 2b: Extraer "Dataset" excluyendo párrafos 4 y 5
                Entrada: entrada de usuario (b), archivo markdown
                Salida: texto de la sección "### Dataset de referencia" sin parrafos 4 y 5

        Opción 3: Extraer sección "Pasos: descomposición de problemas"
            Entrada: entrada de usuario (3), archivo markdown
            Salida: texto de los párrafos 1 a 3.

        Opción 4: Extraer sección "Pseudocódigo y diagrama de flujo
            Entrada: entrada de usuario (4), archivo markdown
            Salida: texto de los párrafos 1 a 3.

        Opción 5: Extraer sección "Sugerencias Copilot"
            Entrada: entrada de usuario (5), archivo markdown
            Salida: texto de los párrafos 1 a 3.

        Opción 6: Extraer sección "Código"
            Entrada: entrada de usuario (6), archivo markdown
            Salida: texto de los párrafos 1 a 3.
```

4. **Estimación de reglas y excepciones**
Entrada inválida en menús -> pedir reentrada.
Criterio de éxito: el usuario puede leer y navegar interactivamente la documentación del proyecto.

### Pseudocódigo
```
INICIO
    REPETIR
        MOSTRAR menú principal
        SOLICITAR ingreso de opción (1 a 6)

        SEGÚN opción SELECCIONADA HACER
            OPCION 1:
                EXTRAER párrafos 1 a 3 del archivo markdown
                MOSTRAR opción SALIR
                SI usuario elige SALIR ENTONCES
                    CONTINUAR (volver al menú)

            OPCION 2:
                MOSTRAR submenú:
                    a) Ver párrafos 4 y 5
                    b) Ver sección "### Dataset de referencia" excluyendo párrafos 4 y 5
                SOLICITAR subopción

                SI subopción = a ENTONCES
                    EXTRAER párrafos 4 y 5 del archivo markdown
                SI subopción = b ENTONCES
                    EXTRAER sección " ### Dataset de referencia" EXCLUYENDO párrafos 4 y 5

                MOSTRAR opción SALIR
                SI usuario elige SALIR ENTONCES
                    CONTINUAR

            OPCION 3:
                EXTRAER sección "### Pasos: descomposición de problemas"
                MOSTRAR opción SALIR
                SI usuario elige SALIR ENTONCES
                    CONTINUAR

            OPCION 4:
                EXTRAER sección "### Pseudocódigo y diagrama de flujo"
                MOSTRAR opción SALIR
                SI usuario elige SALIR ENTONCES
                    CONTINUAR

            OPCION 5:
                EXTRAER sección "### Sugerencias Copilot"
                MOSTRAR opción SALIR
                SI usuario elige SALIR ENTONCES
                    CONTINUAR

            OPCION 6:
                MOSTRAR código
                MOSTRAR opción SALIR
                SI usuario elige SALIR ENTONCES
                    CONTINUAR

            OPCION INVÁLIDA:
                SOLICITAR reentrada

        FIN SEGÚN
    HASTA que usuario cierre manualmente el programa
FIN
``` 

### Diagrama de flujo

### Sugerencias Copilot
#### Aceptadas
#### Descartadas

### Programa Python
