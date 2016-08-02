# Hands-On con git
Ejercicios para practicar comandos básicos de git y cómo trabajar con github.

## El repositorio

La idea es trabajar sobre un fork del repositorio del curso. Entonces:

```
$ git https://github.com/pewen/wpc.git
$ cd wpc
```

Miramos los branches que existen

```
$ git branch 
    gh-pages
    master
  * original
```

Editamos el archivo de README agregando los datos personales y hacemos un nuevo commit

```
emacs README.md
.........
$ git add README.md
$ git commit
```

Ya hay un nuevo snapshot. Ahora creamos una branch donde vamos a poner todas nuestras soluciones.

```
$ git branch soluciones
```

Y nos movemos a ella

```
$ git checkout soluciones
```

En esta branch, editamos README.md de nuevo y explicamos que en este branch van a estar nuestras soluciones

```
$ emacs README.md
  ...
$ git add README.md
$ git commit
```

Ahora vamos a master (que no tiene estos cambios, porque es otra branch!)

```
$ git checkout master
```

Y a partir de master creamos una nueva branch donde vamos a trabajar el proyecto final

```
$ git branch tp_final
$ git checkout tp_final
```

Editamos un archivo nuevo, tp_final.md, donde explicamos cuál va a ser nuestro trabajo final

```
$ emacs tp_final.md
  ...
$ git add tp_final.md
$ git commit
```

Y ahora, en master, hacemos un merge de ambas branches por separado:
(fíjense que no importa que el orden sea el mismo que en el que 
las modificamos. Lo que es sensato, porque las branches no se comunican)

```
$ git merge --no-ff soluciones
$ git merge --no-ff tp_final
```

La opción --no-ff sirve para que no "mezcle" las dos branches, y queda más prolijo el network. Recomiendo que la usen siempre, pero no es fundamental.

Si quieren ver cómo quedó la historia del repo:

```
$ git log --oneline --graph
```

Finalmente, hacemos un push de todas las branches:

```
$ git push -u origin master
$ git push -u origin soluciones
$ git push -u origin tp_final
```

Y listo! en nuestra cuenta de github ya tiene que estar subido.


