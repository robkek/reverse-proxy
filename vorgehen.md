# Vorgehen

## Ordnerstruktur

- /apps
  - Um den Reverse Proxy auszuprobieren brauchen wir ja Anwendungen, auf die er weiterleiten soll
  - Dafür habe ich beispielhaft eine flask-app und Wordpress ausgewählt
  - Beide werden wir als Docker Container aufsetzen
  - Bei der flask-app haben wir den Source Code und eine Dockerfile
  - Wordpress holen wir uns als Image von [Docker Hub](https://hub.docker.com/_/wordpress)
- /nginx
  - Alles für den Reverse Proxy mit NGINX
- /traefik
  - Alles für den Reverse Proxy mit Traefik

## NGINX

### v1

- Verwendung von docker-compose zur komfortablen Verwaltung mehrerer Container (z.B. Hochfahren)
  - Bestandteil der Installation von Docker Desktop
Wir werden docker-compose verwenden
  - Alternative: Mit `docker run` jeden Container einzeln hochfahren
  - Vergleichbar mit helm-charts von Kevin
- docker-compose.yml erklären
  - Dieselben Attribute, die Kevin vorhin schon erklärt hat
  - Hovern für Erklärungen
- Hochfahren mit Konsole oder VSC Extension
- Im Browser darauf zugreifen
- Runterfahren
- Umständlich: Ports
  - Das lösen wir später

## v2

- Hinzufügen eines neuen Containers: NGINX
- Für NGINX haben wir nicht den Sourcecode und eine Dockerfile auf dem Computer sondern verwenden ein Image von [Docker Hub](https://hub.docker.com/_/nginx)
- Als Volume haben wir "static-content" gemountet
- Hochfahren und im Browser darauf zugreifen
- Runterfahren

## v3

- Als Volume mounten wir zusätzlich ../config/nginx.conf:/etc/nginx/nginx.conf:ro
- 