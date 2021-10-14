FROM python:3.8

ADD ./requirements.txt ./
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt

COPY ./ ./
COPY assets assets

EXPOSE 8050
CMD ["python", "./app.py"]