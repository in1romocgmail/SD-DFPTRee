# SD-DFPTRee
Código fuente Phython de la aplicación presentada en el artículo: J. M. Luna, H. M. Fardoun, F. Padillo, C. Romero &amp; S. Ventura (2022) Subgroup discovery in MOOCs: a big data application for describing different types of learners, Interactive Learning Environments, 30:1, 127-145, https://doi.org/10.1080/10494820.2019.1643742

## Estructura
 README.md                  # Descripción e instrucciones de uso  
 requirements.txt           # Dependencias de Python  
 src/                       # Código fuente  
 ├── preprocess_data.py     # Script para preprocesar datos  
 ├── discover_rules.py      # Script SD-DFPTRee secuencial descubrir reglas  
 ├── sd_dfptree.py          # Script SD-DFPTRee Spark descubrir reglas  
 ├── postprocess_rules.py   # Script para el posprocesamiento de reglas  

## Requisitos
Instala las dependencias utilizando:  
pip install -r requirements.txt`

## Uso

### Paso 1: Preprocesar datos

python src/preprocess_data.py --input data/input/raw_data.csv --output data/output/preprocessed_data.csv


### Paso 2: Descubrir reglas

python src/discover_rules.py --input data/output/preprocessed_data.csv --output data/output/rules.csv


### Paso 3: Descubrir reglas con Spark

python src/sd_dfptree.py --input data/output/preprocessed_data.csv --output data/output/spark_rules.csv


### Paso 4: Posprocesar reglas

python src/postprocess_rules.py --input data/output/spark_rules.csv --output data/output/final_rules.csv


