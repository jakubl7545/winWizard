# Win Wizard #

* Autor: Oriol Gómez, dodatak trenutno održava Łukasz Golonka
* NVDA kompatibilnost: 2019.3 i noviji
* Preuzmi [stabilnu verziju ][1]

Ovaj dodatak vam dozvoljava da izvršite određene radnje sa fokusiranim
prozorom ili procesom koji je vezan uz njega.  Kada se zatvori proces, ili
prikaže/sakrije prozor čuće se zvučni signal potvrde ako je radnja uspešna.
Ako ovo ne želite možete da onemogućite ove zvučne signale iz panela Win
Wizarda iz dijaloga NVDA podešavanja.

## Tasterske prečice:
Sve ove prečice se mogu promeniti u dijalogu ulazne komande u kategoriji Win
wizard.
### Skrivanje i ponovno prikazivanje skrivenih prozora:
* NVDA+Windows+brojevi od 1 do 0 - krije trenutno fokusirani prozor na
  poziciji koja pripada pritisnutom broju
* NVDA plus Windows plus strelica levo - prebacuje se na prethodnu pregradu
  sa skrivenim prozorima
* NVDA plus Windows plus strelica desno - prebacuje se na sledeću pregradu
  sa skrivenim prozorima.
* Windows  plus šift plus H: Krije trenutno fokusirani prozor na prvoj
  dostupnoj poziciji.
* NVDA plus Windows plus H - prikazuje poslednji skriveni prozor.
* Windows plus šift plus L - prikazuje sve skrivene prozore grupisane po
  pregradama (molimo imajte na umu da je podrazumevano poslednji skriveni
  prozor izabran )

### Upravljanje procesima:
* Windows plus F4 - zatvara proces kojem trenutno fokusirani prozor pripada
* NVDA plus Windows plus P - otvara dijalog koji vam dozvoljava da podesite
  prioritet procesa kojem pripada trenutno fokusirani prozor

### Razne komande:
* NVDA+Windows+TAB - Prebacuje se između prozora aplikacije (korisno u
  programima foobar2000, Back4Sure i slično)
* CTRL+ALT+T - Dozvoljava vam da promenite naziv trenutno fokusiranog
  prozora

## Promene:

### Promene u 5.0.4:

* Kompatibilnost uz NVDA 2022.1
* Sada je moguće onemogućiti zvučne signale potvrde iz panela sa
  podešavanjima dodatka
* Ažurirani prevodi

### Promene u 5.0.3:

* Kompatibilnost uz NVDA 2021.1

### Promene u 5.0.2:

* Prva verzija dostupna na sajtu sa dodacima

[[!tag dev stable]]

[1]: https://addons.nvda-project.org/files/get.php?file=winwizard
