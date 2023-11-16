# B-LModel_Explorer

#### Modelo $B-L$.

Para construir el archivo de entrada del modelo $B-L$:
* En el archivo `paramSpace.py` modifique los parámetros de las variables `ZpMass_spec` y `g1p_spec` para especificar la región sobre la que se va a hacer el barrido. En la definición de la variable `allowed_params` ya está impuesta la condición $M_{Z'}/g'_1>7.1\ \text{TeV}$.
* Adapte la ruta en la línea `49` para que coincida con la carpeta principal de *SPheno* en su dispositivo.
* Dentro de la carpeta `B_L_Model` ejecute el comando `python3 paramsSpace.py <LesHouches_input_file_path> <SPheno_output_path> <input_card_file_path>`.

Para $\sim 300$ puntos de referencia el procesamiento tarda al rededor de $15$ minutos. Una vez generado el archivo en la dirección `input_card_file_path` copie su contenido en el archivo `incard/card_1.dat` del programa *Z'-explorer*.
