FROM python:3.11-slim

RUN git clone git@github.com:shallotpancake/gaimincalendator.git && \
    cd gaimincalendator && \
    pip install -r requirements.txt

CMD ["python", "gaimincalendator/main.py"]



