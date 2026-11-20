# 1.

 ✔ Image breach-checker-frontend       Built                            3.6s
 ✔ Image breach-checker-backend        Built                            3.6s
 ✔ Network breach-checker_default      Created                          0.1s
 ✔ Container breach-checker-db-1       Healthy                          6.6s
 ✔ Container breach-checker-backend-1  Started                          6.7s
 ✔ Container breach-checker-frontend-1 Started                          6.9s

 docker compose ps
NAME                        IMAGE                     COMMAND                  SERVICE    CREATED              STATUS                        PORTS
breach-checker-backend-1    breach-checker-backend    "python app.py"          backend    About a minute ago   Up About a minute (healthy)   5000/tcp
breach-checker-db-1         postgres:16-alpine        "docker-entrypoint.s…"   db         About a minute ago   Up About a minute (healthy)   5432/tcp
breach-checker-frontend-1   breach-checker-frontend   "/docker-entrypoint.…"   frontend   About a minute ago   Up About a minute             0.0.0.0:8080->80/tcp, [::]:8080->80/tcp

# 2.

docker compose exec db psql -U breach -d breachdb -c "INSERT INTO leaked_hashes VALUES ('bc45408273d7e1914b741c3407b0b559764f7876');"
INSERT 0 1

{"hash":"bc45408273d7e1914b741c3407b0b559764f7876"}' | curl.exe -X POST http://localhost:8080/api/check -H "Content-Type: application/json" -d '@-'
{"found":true}

docker compose down + docker compose up -d

'{"hash":"bc45408273d7e1914b741c3407b0b559764f7876"}' | curl.exe -X POST http://localhost:8080/api/check -H "Content-Type: application/json" -d '@-'
{"found":true}

docker compose down -v + docker compose up -d

'{"hash":"bc45408273d7e1914b741c3407b0b559764f7876"}' | curl.exe -X POST http://localhost:8080/api/check -H "Content-Type: application/json" -d '@-'
{"found":false}

Skrót przetrwał `down`, a nie przetrwał `down -v`, ponieważ db zapisywany jest w wolumenie. Polecenie `down` nie usuwa wolumenu tylko sam kontener, `down -v` usuwa kontener i wolumen, w którym znajduje się baza danych.

# 3.

docker compose ps
NAME                        IMAGE                     COMMAND                  SERVICE    CREATED              STATUS                        PORTS
breach-checker-backend-1    breach-checker-backend    "python app.py"          backend    19 minutes ago       Up 19 minutes (healthy)       5000/tcp
breach-checker-backend-2    breach-checker-backend    "python app.py"          backend    About a minute ago   Up About a minute (healthy)   5000/tcp
breach-checker-backend-3    breach-checker-backend    "python app.py"          backend    About a minute ago   Up About a minute (healthy)   5000/tcp
breach-checker-db-1         postgres:16-alpine        "docker-entrypoint.s…"   db         19 minutes ago       Up 19 minutes (healthy)       5432/tcp
breach-checker-frontend-1   breach-checker-frontend   "/docker-entrypoint.…"   frontend   19 minutes ago       Up 19 minutes                 0.0.0.0:8080->80/tcp, [::]:8080->80/tcp

 docker compose exec frontend nslookup backend
Server:         127.0.0.11
Address:        127.0.0.11:53

Non-authoritative answer:

Non-authoritative answer:
Name:   backend
Address: 172.19.0.3
Name:   backend
Address: 172.19.0.6
Name:   backend
Address: 172.19.0.5

Przed restartem

backend-1  | check: hash=bc454...
backend-1  | 172.19.0.4 - - [20/Nov/2026 09:24:41] "POST /check HTTP/1.1" 200 -
backend-1  | check: hash=bc454...
backend-1  | 172.19.0.4 - - [20/Nov/2026 09:24:41] "POST /check HTTP/1.1" 200 -
backend-1  | check: hash=bc454...
backend-1  | 172.19.0.4 - - [20/Nov/2026 09:24:41] "POST /check HTTP/1.1" 200 -
backend-1  | check: hash=bc454...
backend-1  | 172.19.0.4 - - [20/Nov/2026 09:24:41] "POST /check HTTP/1.1" 200 -

Po restarcie

backend-1  | check: hash=bc454...
backend-1  | 172.19.0.4 - - [20/Nov/2026 09:24:41] "POST /check HTTP/1.1" 200 -
backend-1  | check: hash=bc454...
backend-1  | 172.19.0.4 - - [20/Nov/2026 09:24:41] "POST /check HTTP/1.1" 200 -
backend-1  | check: hash=bc454...
backend-1  | 172.19.0.4 - - [20/Nov/2026 09:24:41] "POST /check HTTP/1.1" 200 -


Przed restartem nginx rozwiązuje nazwę backend w wewnętrznym DNS Dockera tylko raz podczas startu kontenera i zapisuje wynik w pamięci podręcznej. W momencie uruchomienia frontend istniała tylko jedna replika backend dlatego nginx zapamiętał wyłącnie jej adres IP. 
Po restarcie frontend wymusił odpytanie DNS przez nginx. DNS Dockera zwrócił adresy IP wszystkich trzech aktywnych replik backend.

W momencie gdyby backend nadal miał ports 5000:5000 to uruchomienie większej ilości replik byłoby niemożliwe ze względu na to że na dany port może nasłuchiwać tylko jeden proces - jeden kontener.