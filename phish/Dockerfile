FROM python:3.8.2-alpine3.11
WORKDIR /home/src
RUN apk update && apk add gcc libc-dev make git libffi-dev openssl-dev python3-dev libxml2-dev libxslt-dev
RUN pip install flask peewee gunicorn
COPY . .
ENV FLAG "we{e0df7105-edcd-4dc6-8349-f3bef83643a9@h0P3_u_didnt_u3e_sq1m4P}"
CMD ["gunicorn", "main:app", "--workers", "20", "--timeout", "2", "-b", "0.0.0.0:1002"]