# DLandsat

Dlandsat es una herramienta de linea de comando (totalmente implementada en python) para buscar y descargar de forma simple imágenes de cualquier satélite Landsat.

Se agradece a Olivier Hagolle (y a todos sus colaboradores), ya que esta herramienta esta inspirada en su [trabajo](https://github.com/olivierhagolle/LANDSAT-Download).

## Autores:
* [Franco Bellomo](https://twitter.com/fnbellomo)
* [Lucas Bellomo](https://twitter.com/ucaomo)

## Instalación
Todas las herramientas utilizadas en DLansat son de la librería estandar de Python, con lo cual no hace falta ninguna instalación adicional.

## Funcionamiento

DLandsat posee 3 funciones principales:

### 1 Buscar y Descargar mediante coordinadas WRS-2
Teniendo una coordinada [WRS-2](http://landsat.usgs.gov/worldwide_reference_system_WRS.php), podemos buscar y descargar las imágenes mediante:

	$ python DLandsat_cli.py -o scene -b LE7_SLC_OFF -d 20130127 -f 20150901 -s 198030 -c 1 -output /home/user/Desktop/L

Donde:

	--conf:
		Archivo con el usuario y contraseña para conectarse al [USGS earthexplorer](http://earthexplorer.usgs.gov/).
		Opcionalmente, se puede dar la configuración (usuario, contraseña, host, port) para salir mediante un proxy.
		Por default este archivo se llama user.config
	-o, --option:
		Indica que vamos a buscar y descargar mediante un par de coordenadas WRS-2
	-b, --sat:
		El satélite que vamos a usar. Podemos optar entre: LT4_5_MSS, LT4_5_TM, LE7_SLC_OFF, LE7_SLC_ON o LC8.
	-d, --start_date:
		Fecha desde la que queremos empezar a buscar imágenes.
	-f, --end_date:
		Fecha hasta la que queremos buscar imágenes. Si no es dada, se toma como la fecha actual.
	-s, --scene:
		Coordenadas WRS-2. Ej. si el path es 198 y el row 030, -s 198030.
	-c, --cloudcover:
		Límite máximo de la imágen cubierta por nubes, donde 1 es 10%, 2 es 20%, ..., 9 es 90%. La opción por defecto no pone límite.
	--output:
		Path donde se van a guardar las imágenes. Por default es /tmp/Landsat.
	-z, --unzip:
		Descomprime el archivo después de bajarlo.
	-t, --timeout:
		Tiempo máximo sin conexión (en segundo). Default = 60 seg.
	-q:
		Solo imprime los progresos de las descargas y los errores.
	-qq:
		Solo imprime los errores.

La metadata es descargada de este [link](https://landsat.usgs.gov/consumer.php)

### 2 Descargar los catálogos
No implementada todavía.

### 3 Descargar de una lista
No implementada todavía.

## Documentación
Todas las funciones tienen su doc-string (en ingles) correspondiente.

## TODO
- [x] Portar el código a Python3.
- [x] Cuando esta descargando una imagen, agregar el tiempo aproximado que falta.
- [x] Cuando esta descargando una imagen, que sea en un archivo .tar.gz.part y que cuando termine lo mueva a un .tar.gz
- [ ] Si el archivo se descargo de forma incorrecta, que lo vuelva a hacer.
- [ ] Poder decir que te baje una sola imagen por mes, y también que no baje fotos de ciertos meses.
- [x] Implementar un connection time out. [Mirar esto](https://stackoverflow.com/questions/811446/reading-a-stream-made-by-urllib2-never-recovers-when-connection-got-interrupted?lq=1)
- [ ] Controlar que no allá bajado antes ese comprimido.
- [x] Función para descomprimir.
- [ ] Función que descargue en base a una lista de scenes.
- [ ] Hacer un log file.

## Licencia
