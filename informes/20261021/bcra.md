# BCRA — informe 20261021
Resumen del día: una sola Comunicación "A" (8492), de índole informativa: ajusta el Régimen Informativo Contable Mensual de Efectivo Mínimo y Aplicación de Recursos (posición diaria, partida 102200 de saldos de PSPOCP). Sin cambio de tasas ni de exigencias.

## Comunicación "A" 8492/2026
- **Número / código GDE:** Com. "A" 8492. El aviso del BORA (id 349377, e. 21/10/2026 N° 77767/26) no trae código GDE. Ref.: Circular CONAU 1-1743, RUNOR 1-1978. Firma: 15/10/2026. Vigencia: 01/11/2026. Publicada en BORA el 21/10/2026.
- **Firmantes:** Mariana A. Díaz, Gerenta de Régimen Informativo; Rodrigo J. Danessa, Subgerente General de Régimen Informativo y Protección al Usuario de Servicios Financieros a/c.
- **Fuente del anexo:** el BORA no publica el anexo. Se bajó el texto ordenado de bcra.gob.ar (`A8492.pdf`, 6 páginas) y se leyó completo.

**Qué dispone**
- Adecúa la Sección 6 "Posición de Efectivo Mínimo Diaria" del R.I. E.M.-A.R. (v. 2a.). Para la partida 102200/001 (depósitos en pesos en cuentas de proveedores de servicios de pago que ofrecen cuentas de pago, PSPOCP, con fondos de clientes) se informan los saldos diarios efectivamente registrados en cada día. Los PSPOCP se presentan a diario con vencimiento a las 15 hs del 2.º día hábil posterior, para las entidades del grupo A y sucursales o subsidiarias de G-SIB no incluidas en ese grupo.
- Punto 6.2.2.1 (SALDOSPROMEDIO.TXT): no se admite la partida 102200. Para el total de la partida 100000 se suma el promedio de los saldos diarios de la 102200 informados en SALDOSDIARIOS.TXT o SALDOSMENSUALES.TXT.
- Punto 6.2.2.2 (SALDOSDIARIOS.TXT): se informa en este archivo el saldo diario de la 102200, con campo "Categoría" 3 (0 para el resto).
- Punto 6.2.2.3 (SALDOSMENSUALES.TXT): ídem con el saldo diario de la 102200, con "Categoría" 1.
- Control de validación 538 (inconsistencia en partidas 21010X): la suma de las 21010X/TP no puede superar la suma de las 824X00/001 y 825000/001 del período anterior más el 45% del saldo promedio de la 102200/001 del mes.
- No toca tasas, sujetos ni plazos de la norma de fondo. No se sabe qué decía la redacción anterior de las hojas: la Comunicación acompaña solo las hojas nuevas y no hay un cotejo en el repo.

**Lectura:** ajuste técnico de reporte que pasa la 102200 a informarse con saldos diarios efectivos y la incorpora al control de los títulos 21010X. Es el único antecedente de BCRA en el repo; el dossier arranca con esta norma, así que no hay línea previa con la cual compararla.

Atención: la vigencia es el 01/11/2026, y las entidades obligadas deben adecuar sus archivos de presentación antes del primer vencimiento posterior.
