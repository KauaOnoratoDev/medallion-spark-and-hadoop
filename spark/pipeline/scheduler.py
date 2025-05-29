import subprocess
import os
from dotenv import load_dotenv

load_dotenv()

stages = [
    ("ingestion", "[Bronze]"),
    ("transformation", "[Silver]"),
    ("serving", "[Gold]"),
]

for stage, medallion in stages:
    print(f'{stage.capitalize()} {medallion}'.center(100, '_'))
    script_path = f'./pipeline/notebooks/{stage}.py'
    
    env = os.environ.copy()
    
    if stage == 'ingestion':
        env['DB_USER'] = os.getenv('DB_USER')
        env['DB_PASSWORD'] = os.getenv('DB_PASSWORD')
        
    try:
        result = subprocess.run(
            ['spark-submit', '--packages', 'org.postgresql:postgresql:42.6.0', script_path],
            env=env,
            capture_output=True,
            text=True,
            check=True,
        )
        print(result.stdout)
        
    except subprocess.CalledProcessError as error:
        print(f'Erro ao executar {stage}')
        print(error.stderr)
        print(error.stdout)