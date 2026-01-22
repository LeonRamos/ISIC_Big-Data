# Instalación del Arduino IDE y drivers para placas ESP32 en Windows 11.

---

## Contenido

- [Objetivo](#objetivo)
- [Requisitos previos](#requisitos-previos)
- [Instalación del Arduino IDE](#instalación-del-arduino-ide)
- [Configuración del IDE para ESP32](#configuración-del-ide-para-esp32)
- [Instalación de drivers USB](#instalación-de-drivers-usb)
- [Verificación del puerto COM](#verificación-del-puerto-com)
- [Prueba de funcionamiento](#prueba-de-funcionamiento)

---

## Objetivo

Configurar correctamente el entorno de desarrollo necesario para realizar **todas las prácticas del semestre**, utilizando el **Arduino IDE** y placas **ESP32**, asegurando que el estudiante pueda programar, compilar y cargar código sin errores desde su equipo con **Windows 11**.

---

## Requisitos previos

Antes de iniciar, asegúrate de contar con:

- Computadora con **Windows 11**
- Conexión a Internet
- Cable USB (datos, no solo carga)
- Placa de desarrollo **ESP32**
- Permisos de administrador en el equipo

---

## Instalación del Arduino IDE

1. Ingresa al sitio oficial de Arduino:
   https://www.arduino.cc/en/software

2. Descarga la versión:
   - **Windows Win 10 and newer (64-bit)**

3. Ejecuta el instalador descargado:
   - Acepta los términos de licencia.
   - Marca todas las opciones:
     - Install USB driver
     - Associate `.ino` files
   - Finaliza la instalación.

4. Abre el **Arduino IDE** para verificar que inicia correctamente.

---

## Configuración del IDE para ESP32

### Agregar el gestor de tarjetas ESP32

1. En el Arduino IDE, ve a:

```
File → Preferences
```

2. En el campo **Additional Boards Manager URLs**, agrega la siguiente URL:

```
https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
```

> Si ya existe otra URL, sepárala con una coma.

3. Presiona **OK** y reinicia el Arduino IDE.

---

### Instalar la tarjeta ESP32

1. Ve a:

```
Tools → Board → Boards Manager
```

2. En el buscador escribe:

```
esp32
```

3. Selecciona **esp32 by Espressif Systems** y presiona **Install**.

4. Espera a que finalice la instalación (puede tardar algunos minutos).

---

## Instalación de drivers USB

Dependiendo del modelo de ESP32, puede requerirse un driver adicional.

### Driver CH340 / CP210x

1. Descarga los drivers desde alguno de los siguientes enlaces oficiales:
   - CP210x: https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers
   - CH340: https://www.wch.cn/downloads/CH341SER_ZIP.html

2. Ejecuta el instalador correspondiente.
3. Reinicia la computadora al finalizar.

---

## Verificación del puerto COM

1. Conecta la placa ESP32 al equipo mediante USB.
2. En Arduino IDE, ve a:

```
Tools → Port
```

3. Selecciona el puerto disponible (ejemplo: `COM3`).

Si **no aparece ningún puerto**, revisa:

- Cable USB
- Driver instalado
- Administrador de dispositivos de Windows

---

## Prueba de funcionamiento

1. Selecciona la placa:

```
Tools → Board → ESP32 Arduino → ESP32 Dev Module
```

2. Abre el ejemplo:

```
File → Examples → Basics → Blink
```

3. Presiona **Upload**.
4. Si el código se carga correctamente y el LED parpadea, la instalación fue exitosa.

---

