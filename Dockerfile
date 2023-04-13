#hugging face cpu transformer image
FROM huggingface/transformers-pytorch-cpu
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./app /app
ENV TRANSFORMERS_CACHE models/
EXPOSE 8000
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]