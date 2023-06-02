FROM python:3.11-alpine

RUN addgroup -g 1001 -S appuser && adduser -u 1001 -S appuser -G appuser

USER appuser
COPY --chown=1001:1001 . /home/appuser/app/
WORKDIR /home/appuser/app/

ENV PATH="/home/appuser/.local/bin:$PATH"

#Update PIP and install dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

WORKDIR /home/appuser/app/financial/

EXPOSE 5000
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
CMD ["ping", "db"]