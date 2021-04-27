services:

  nginx:
    container_name: nginx
    hostname: nginx
    image: nginx
    ports:
      - "80:80"
    volumes:
      - ../static-content:/usr/share/nginx/html:ro
      - ../config/nginx.conf:/etc/nginx/nginx.conf:ro

  todo-list:
    container_name: todo-list
    build: ../../apps/todo-list
    ports:
      - "3000:3000"

  cats:
    container_name: cats
    build: ../../apps/flask-app
    ports:
      - "5000:5000"