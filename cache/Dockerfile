FROM python:3.8.10-alpine

WORKDIR /usr/src/app
RUN pip install django gunicorn
COPY . .
ENV FLAG "we{adecbd5c-a02c-4d85-883e-caee34760745@b3TTer_u3e_cl0uDF1are}"
ENV ADMIN_TOKEN CroRQgDwMmJdybKa
CMD ["gunicorn", "cache.wsgi", "-b", "0.0.0.0:1006"]