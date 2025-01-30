# Examen BentoML
Please execute the following commands for running the BentoML application
```bash       
python3 -m venv .venv
pip install -r requirements.txt 

python3 src/data/split_data.py
python3 src/data/normalize_data.py
python3 src/model/predict_parameters.py
python3 src/model/traib_model.py
python3 src/model/evaluate_model.py

bentoml build
bentoml containerize uni_acceptance_service:latest
docker run --rm -p 8888:3000 uni_acceptance_service:latest

pytest tests/
```