from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    "owner": "lucas",
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="pipeline_bets",
    description="Pipeline Bronze, Silver e Gold do projeto de odds",
    default_args=default_args,
    start_date=datetime(2026, 7, 1),
    schedule="0 * * * *",
    catchup=False,
    tags=["bets", "odds", "engenharia-dados"],
) as dag:

    bronze = BashOperator(
        task_id="bronze_coletar_odds",
        bash_command="cd /opt/airflow && python codigo-fonte/ingestao/coletar_odds.py",
    )

    silver = BashOperator(
        task_id="silver_processar_odds",
        bash_command="cd /opt/airflow && python codigo-fonte/processamento/silver.py",
    )

    gold = BashOperator(
        task_id="gold_melhores_odds",
        bash_command="cd /opt/airflow && python codigo-fonte/processamento/gold.py",
    )
    bronze >> silver >> gold
    
