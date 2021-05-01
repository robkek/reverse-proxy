# Reverse Proxy am Beispiel von NGINX und Traefik

Mit den folgenden Erläuterungen könnt ihr die Übungen nochmal alleine wiederholen und euch vertieft mit dem Thema beschäftigen. 😊

## Vorbereitung

- [Visual Studio Code](https://code.visualstudio.com/Download) installieren ✅
- Git installieren (z.B. [git-scm](https://git-scm.com/downloads)) ✅
- [Lemonron/reverse-proxy](https://github.com/Lemonron/reverse-proxy) klonen ✅
- `WIN + R`: winver
  - Version 1903 oder höher
    1. [WSL II](https://docs.microsoft.com/en-us/windows/wsl/install-win10) einrichten
    2. [Docker Desktop](https://www.docker.com/products/docker-desktop) installieren
  - Version älter als 1903
    1. [VirtualBox](https://www.virtualbox.org/wiki/Downloads) mit [Ubuntu](https://ubuntu.com/download/server) aufsetzen
    2. [docker](https://docs.docker.com/engine/install/ubuntu/#install-using-the-convenience-script) und [docker-compose](https://docs.docker.com/compose/install/#install-compose) installieren
- [Docker Extension für Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker) installieren
- Optional für eine Übung: [Postman](https://www.postman.com/downloads/) installieren

## /apps

Der Ordner [/apps](/apps) enthält drei Beispielanwendungen, auf die unsere Reverse Proxies später lenken sollen:

- [todo-list](https://github.com/docker/getting-started/tree/master/app)
- [bulletin-board](https://github.com/dockersamples/node-bulletin-board/tree/master/bulletin-board-app)
- [cats](https://github.com/docker/labs/tree/master/beginner/flask-app)

## /nginx

Der Ordner [/nginx](/nginx) enthält alles, was wir zum Aufsetzen eines Reverse Proxys mit NGINX benötigen.

### v1

Wir werden im Folgenden das Tool [docker-compose](https://docs.docker.com/compose/) verwenden. Es bietet eine komfortable Möglichkeit, mehrere (evtl. zusammenhängende) Container zu definieren und zu steuern (z.B. Hochfahren). Zentrale Datei ist hierbei die sog. docker-compose.yml. Die `docker-compose` Befehle müssen immer im Verzeichnis der docker-compose.yml ausgeführt werden.

Zum Hochfahren der [docker-compose.yml in v1](/nginx/v1/docker-compose.yml) gibt es zwei Möglichkeiten:

- `docker-compose up -d`
- Nutzen der Docker Extension: Rechtsklick auf [docker-compose.yml in v1](/nginx/v1/docker-compose.yml) > Compose Up

Unsere drei Anwendungen sind über `localhost` und ihren jeweiligen **externen** Port erreichbar.

Der **interne** Port wird häufig von der Anwendung selbst vorgegeben, ließe sich aber im Quellcode verändern:

- [/apps/todo-list/src/index.js](/apps/todo-list/src/index.js) > Zeile 18
- [/apps/bulletin-board/server.js](/apps/bulletin-board/server.js) > Zeile 37
- [/apps/cats/Dockerfile](/apps/cats/Dockerfile) > Zeile 19

### v2

Bevor wir die [docker-compose.yml in v2](/nginx/v2/docker-compose.yml) starten, müssen wir [die aus v1](/nginx/v1/docker-compose.yml) herunterfahren, da ihre Container dieselben Containernamen und Ports belegen. Auch hierfür gibt es zwei Möglichkeiten:

- `docker-compose down`
- Nutzen der Docker Extension: Rechtsklick auf [docker-compose.yml in v1](/nginx/v1/docker-compose.yml) > Compose Down

Dasselbe gilt für das Neustarten. Beim Neustarten einer docker-compose.yml über die Docker Extension werden die Container allerdings nicht nur neugestartet, sondern auch *removed*, äquivalent zum Befehl `docker-compose rm`.

Neben unseren drei Anwendungen ist nun zusätzlich NGINX als Webserver auf dem externen Port 80 erreichbar. Er liefert unsere HTML-Dateien aus dem Ordner [/nginx/html](nginx/html) aus. Diesen Ordner haben wir NGINX als Volume mitgegeben.

Volumes können zum Persistieren von Daten verwendet werden, die der Container generiert oder verwendet. Beim *Removal* des Containers bleiben die Daten im Volume erhalten.

Im Gegensatz zu unseren drei Anwendungen in [/apps](/apps) haben wir für NGINX keinen Quellcode und keine Dockerfile auf unserem System, sondern verwenden ein Image von [Docker Hub](https://hub.docker.com/_/nginx). Dort ist z.B. auch aufgeführt, wo die auszuliefernden HTML-Dateien liegen müssen.

Docker Hub ist ein open-source und kostenloses Registry für Docker Images. Man kann sich aber auch ein [eigenes Registry](https://hub.docker.com/_/registry) hosten.

Da wir NGINX in keinster Weise konfiguriert haben, wird die /etc/nginx/conf.d/default.conf im Container verwendet. Diese können wir uns mit der Docker Extension auf mehrere Arten anschauen:

- Daten des Containers bis zu /etc/nginx/conf.d aufklappen und default.conf öffnen oder herunterladen
- Rechtsklick auf den Container > Attach Shell > `cat /etc/nginx/conf.d/default.conf`
- Rechtsklick auf den Container > Attach Visual Studio Code > Open Folder > / > Nach /etc/nginx/conf.d navigieren und default.conf öffnen

### v3

Um NGINX nicht nur als Webserver, sondern zusätzlich als **Reverse Proxy** zu verwenden, sind weitere Konfigurationen notwendig.

Nach der Anleitung auf [Docker Hub](https://hub.docker.com/_/nginx) geben wir NGINX die [nginx_v3.conf](/nginx/config/nginx_v3.conf) als Volume mit. Bei deren Gestaltung orientieren wir uns an der /etc/nginx/conf.d/default.conf aus [v2](###v2). Zur Konfiguration des Reverse-Proxys nutzen wir das Modul [ngx_http_proxy_module](https://nginx.org/en/docs/http/ngx_http_proxy_module.html) bzw. dessen Anweisung *proxy_pass*.

Docker Container bekommen bei jedem Removal eine neue interne IP-Adresse zugewiesen. Das können wir uns z.B. in der Kommandozeile anschauen:

- `docker container inspect nginx | grep IPAddress`
- Rechtsklick auf [docker-compose.yml](/nginx/v3/docker-compose.yml) > Compose Restart
- `docker container inspect nginx | grep IPAddress`

Aus diesem Grund können wir in der [nginx_v3.conf](/nginx/config/nginx_v3.conf) nicht die IP-Adresse verwenden, um auf einen anderen Container zu verweisen. Container im selben Netzwerk können sich allerdings gegenseitig mit ihrem Namen und **internen** Port aufrufen. Spezifiziert man in der [docker-compose.yml](nginx/v3/docker-compose.yml) kein Netzwerk, so fügt Docker alle Container der Datei in ein Standardnetzwerk. Auch das können wir uns anschauen:

- `docker container inspect todo-list bulletin-board cats nginx | grep NetworkMode`

Mit NGINX lassen sich auch sehr viel komplexere Szenarien als unseres lösen. Wer sich dafür interessiert, kann sich z.B. die [NGINX Documentation](https://www.nginx.com/resources/wiki/start/) anschauen.

NGINX enthält eine integrierte Lösung für Reverse-Proxies. Als dedizierte Lösungen wollen wir uns [Traefik](https://doc.traefik.io/traefik/) anschauen.

## /traefik

Der Ordner [/traefik](/traefik) enthält alles, was wir zum Aufsetzen eines Reverse Proxys mit Traefik benötigen.

### v1

Neben unseren drei Anwendungen ist das Dashboard von Traefik über `localhost:8080` erreichbar.

[Hier](https://doc.traefik.io/traefik/routing/overview/) gibt es einen guten Überblick über die Traefik Architektur. Das Wichtigste möchte ich im Folgenden zusammenfassen. Begriffe von Traefik sind dabei *kursiv* gedruckt.

- *Router* analysieren die Requests und entscheiden, an welchen *Service* sie weitergeleitet werden. Diese Entscheidung wird anhand von *Rules* getroffen.
- *Services* sind die Schnittstellen zu den tatsächlichen Containern im Hintergrund

Traefik unterstützt Docker als *Provider*. Das gibt uns die Möglichkeit, Konfigurationen mithilfe von Docker Labels direkt in der docker-compose.yml unter den betroffenen Container zu schreiben.

Um Docker als *Provider* zu aktivieren, geben wir in der [docker-compose.yml in v1](/traefik/v1/docker-compose.yml) den Command "--providers.docker" mit.

Ohne zusätzliche Konfigurationen erstellt Traefik bereits *Router* (ohne sinnvolle *Rules*) und *Services* für unsere drei Anwendungen.

### v2

Allen drei Anwendungen geben wir ein Docker Label folgender Form mit:
`"traefik.http.routers.ROUTER_NAME.rule=Host(SUBDOMAIN.localhost)"`

ROUTER_NAME ist der Name des *Routers*. Wir definieren für den *Router* eine *Rule*. Erfüllt eine Request die *Rule*, so leitet der *Router* die Request an den zugehörigen *Service*, also die Anwendung, weiter.

In diesem Fall verwenden wir die *Rule* 'Host'. Diese prüft, ob die Request Domain SUBDOMAIN.localhost ist. SUBDOMAIN ist die Subdomain, unter der unsere Anwendung erreichbar sein soll.

Neben 'Host' gibt es noch [andere Arten](https://doc.traefik.io/traefik/routing/routers/#rule) von *Rules*.

### v3

v3 ist eine Übung für euch. Kopiert euch den Ordner [v2](/traefik/v2) und probiert euch an folgenden Aufgaben:

1. NGINX als Webserver wie in [v2 von /nginx](/nginx/v2), der unter nginx.localhost erreichbar ist und HTML-Dateien ausliefert
2. [phpMyAdmin](https://hub.docker.com/_/phpmyadmin) mit MariaDB, phpMyAdmin erreichbar unter phpmyadmin.localhost  
    **Tipp:** Bei der Anmeldung unter phpmyadmin.localhost entspricht Host dem Servicenamen des MariaDB-Containers (hier: db)
3. MariaDB ein Volume zum Persistieren der Daten mitgeben

```yml
...
    volumes:
      - ../../apps/db:/var/lib/mysql
...
```

4. [wordpress](https://hub.docker.com/_/wordpress) mit bereits vorhandener MariaDB, erreichbar unter wordpress.localhost
    - Vorher müssen wir in phpMyAdmin den User mit Password und die Datenbank für wordpress anlegen, auf die wir beim wordpress-Container mit Environment-Variablen referenzieren
    - Auch beim wordpress-Container müssen wir ein Volume mitgeben

```yml
...
    volumes:
      - ../../apps/wordpress:/var/www/html
...
```

- Nutzen [anderer Arten](https://doc.traefik.io/traefik/routing/routers/#rule) von *Rules* und Testen mit Postman

## Hilfreiche Links

- [Überblick über Docker Extension für Visual Studio Code](https://code.visualstudio.com/docs/containers/overview)
- [NGINX Dokumentation](https://www.nginx.com/resources/wiki/start/)
- [ngx_http_proxy_module](https://nginx.org/en/docs/http/ngx_http_proxy_module.html)
- [Traefik Dokumentation](https://doc.traefik.io/traefik/)
- [Docker Hub](https://hub.docker.com)
- [https://docker-curriculum.com/](Docker Curriculum)
- [Docker run to docker-compose converter](https://8gwifi.org/dc1.jsp)
