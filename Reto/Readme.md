# Analizador de respuestas


<h1>Hello!!!</h1>

Libreries

- pandas
- google-genai

<p>For this proyect u need creat a API Key in Google IA Studio,
Well intro to https://aistudio.google.com/ u need a count from google. 
Next click on Get API key.
Click on Generate API Key.
Select name of you key default "Gemini API Key 2".
Creat proyect and select the name example "buenasRespuestas".
click on Generate key.
Put attention: in this step copy de key, just in this time show all key of u proyect.</p>

Well, in u cmd or terminal ,like me, apply next command

--------------------------------------
$env:GEMINI_API_KEY="TU_API_KEY_AQUI"
--------------------------------------

to init API on u pc.

now u could run your script

--------------------------------------
python buenasRespuestas.py
--------------------------------------

u can look this in cmd if u make all steps correctly.

/*
Iniciando clasificación de 3 respuestas usando google-genai...
Procesando ID 1...
Procesando ID 2...
Procesando ID 3...

Proceso completado. Archivo guardado como 'resultados_sentimiento.csv'

------------------------------
      RESUMEN DE SENTIMIENTOS
------------------------------
Positivos   :1
Negativos   :1
Neutro      :1
Error       :0

------------------------------
*/
