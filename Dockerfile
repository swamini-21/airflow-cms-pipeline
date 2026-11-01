FROM astrocrpublic.azurecr.io/runtime:3.3-11

RUN python -m venv /usr/local/airflow/dbt_venv && \
    /usr/local/airflow/dbt_venv/bin/pip install --no-cache-dir dbt-core==1.12.6 dbt-postgres==1.11.0
RUN python -m venv /usr/local/airflow/soda_venv && \
    /usr/local/airflow/soda_venv/bin/pip install --no-cache-dir "setuptools<81" soda-core-postgres==3.5.6