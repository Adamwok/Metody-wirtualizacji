7.1
    curl.exe -X GET http://localhost:5000/health
    {"status":"ok"}

    172.18.0.1 - - [13/Nov/2026 07:49:19] "GET /health HTTP/1.1" 200 -

7.2
    docker run --rm --network breach-net healthcheck-probe
    backend: OK

    docker run --rm healthcheck-probe
    backend: UNREACHABLE

    docker stop backend
    docker run --rm --network breach-net healthcheck-probe
    backend: UNREACHABLE

    Bez podania flagi --network breach-net kontener zostaje uruchomiony w domyślnej sieci bridge, która nie posiada wbudowanego serwera DNS tłumaczącego nazwy kontenerów na adresy IP oraz jest odizolowana od sieci breach-net. W rezultacie nazwa backend nie może zostać rozwiązana.

7.3
    docker exec backend cat /tmp/notatka.txt
    notatka

    docker exec backend cat /tmp/notatka.txt
    cat: /tmp/notatka.txt: No such file or directory

    docker run --rm -v breach-dane:/dane alpine sh -c "date >> /dane/historia.txt; cat /dane/historia.txt"
    Fri Nov 13 08:06:09 UTC 2026
    Fri Nov 13 08:06:18 UTC 2026

    Plik /tmp/notatnka.txt został zapisany w warstwie zapisywalnej kontenera, która jest zachowywana przy jego zatrzymaniu i restarcie, ale trwale usuwana podczas docker rm. Plik historia.txt przetrwał usunięcie obu kontenerów, ponieważ znajdował się w wolumenie breach-dane zarządzanym przez Dockera niezależnie od cyklu życia kontenerów. Lista wycieków również przetrwałaby docker rm ponieważ jest podłączona z dysku hosta za pomocą bind mount, więc fizycznie istnieje w systemie plików hosta.

10.

Reguły zapory sieciowej (firewall / iptables / ACL): gdy dostęp do bazy danych lub zewnętrznego serwisu jest filtrowany na poziomie warstwy sieciowej po konkretnym adresie źródłowym IP.

Starsze (legacy) oprogramowanie i certyfikaty: gdy aplikacja ma wpisany adres IP na sztywno w plikach konfiguracyjnych, nie obsługuje nazw domenowych lub używa certyfikatów TLS wystawionych wyłącznie na adres IP.

Integracja z siecią zewnętrzną (np. macvlan/ipvlan): gdy kontener jest podłączony bezpośrednio do fizycznej sieci LAN/VLAN i jego adres nie może kolidować z pulą lokalnego serwera DHCP.