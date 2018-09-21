Raloy Product Viscosity 2
=========================

<https://docs.google.com/document/d/1rqiXN7MbjuDHSrvSss7J4-cI9x3fwBiZi4qzLzK0MbA>

Definición
Cada proveedor, tiene una relación hacia los productos que nos vende, con los siguientes parámetros adicionales a los estándar de Odoo.

Unidad de Medida de Compra (Puede ser diferente de la Unidad de Almacenamiento Local, estrictamente no debe ser el campo de Unidad de Almacenamiento Local de la MP)
Múltiplos, es decir x cantidad de unidades por presentación en la que nos vende el producto. Ejemplo. 205 Kg = 1 Tambor, si pedimos 410 Kg, en la orden de compra impresa debe aparecer como 2 piezas sin embargo la cantidad pedido sigue siendo 410 Kg.
Unidad para el Multiplo. Un campo texto libre.
Factor de conversión, esto es para poder convertir entre unidades. Ejemplo, convertir de KG a Litros a través de una densidad o 3.7854 para convertir de Galones a Litros.
Densidad, es un valor lógico que determina si al recibo de la MP se pedirá un valor que sustituirá el Factor de Conversión para realizar la conversión de unidad del proveedor a unidad local.
Costo, es expresado en unidad del proveedor.

Estos valores se deben llevar a nivel de las líneas de la Orden de Compra, para que en el formato PDF de orden de compra se exprese en los valores del proveedor.

NOTA Esto aplica tanto en las cantidades ordenadas, como para el precio unitario del producto ordenado, Es decir que el costo unitario debe ser también convertido a unidad local.
Ejemplo Proveedor - Producto:
Producto: M7420
Unidad Local: Lt
Unidad del Proveedor: Kg
Precio por Unidad del Proveedor: 3.19
Múltiplo de Compra: 1
Factor de Conversión: 1.06300
Densidad: Falso

Ejemplo de Compra:
Qty en Unidad del Proveedor: 1000 Kg
Qty en Unidad Local: 1063 Lts (1000 * Factor de Conversión)
Precio por Unidad Proveedor: 3.19000
Precio por Unidad Local: 3.00094 (3.19 / Factor de Conversión)
Total en unidad Proveedor: 3,190.00
Total en unidad Local: 3,189.99922 (3,190.00 redondeado)
Recibo de Materia Prima
Al recibir un material este podría ser recibido introduciendo la cantidad en unidad local o bien en cantidad del proveedor, aplicando las conversiones necesarias a través de los campos Múltiplos y Factor de Conversión.
En caso de que la relación Producto - Proveedor, en el campo Densidad exista un valor verdadero, se deberá pedir al usuario el valor para el Factor de Conversión con el que se hará la conversión a unidad Local.

Este cálculo solo aplica para albaranes de entrada (IN).
Afectación al Inventario.
Para los movimientos de Inventario de recibo de materiales se debe usar el valor en unidad local.
Cuentas x Pagar
Al hacer las conversiones de acuerdo a la regla mencionada, el importe de la entrada en Odoo, deberá corresponder con el importe de la factura del proveedor.
