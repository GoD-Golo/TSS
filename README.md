# T1 - Testare unitara in Python

[![ShoppingCart CI](https://github.com/GoD-Golo/TSS/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/GoD-Golo/TSS/actions/workflows/ci.yml)

Proiectul testeaza clasa `ShoppingCart`, o componenta simpla pentru un magazin online. Clasa permite adaugarea produselor in cos si calculeaza subtotalul, discountul, TVA-ul, costul transportului si totalul final al comenzii.

## Structura repository

| Cale | Rol |
|---|---|
| `tss_project/shopping_cart.py` | Codul sursa al clasei testate |
| `tests/test_shopping_cart_base.py` | Suita initiala de teste |
| `tests/test_shopping_cart_extra.py` | Teste suplimentare adaugate dupa analiza de acoperire si mutatie |
| `scripts/coverage_report.py` | Raport simplu de acoperire, fara dependinte externe |
| `scripts/mutation_report.py` | Generator local de mutanti si raport de mutatie |
| `docs/diagrams/decision_flow.drawio` | Diagrama fluxului de calcul al comenzii, editabila in diagrams.net |
| `docs/results/test_results.md` | Rezultate salvate pentru teste, acoperire si mutatie |

## Descrierea clasei testate

`ShoppingCart` modeleaza regulile de calcul pentru o comanda online:

| Regula | Valoare |
|---|---:|
| TVA | 19% |
| Prag discount | 500 lei |
| Discount | 10% din subtotal |
| Prag transport gratuit | 300 lei, dupa aplicarea discountului |
| Cost transport standard | 20 lei |

Metode principale:

| Metoda | Rol |
|---|---|
| `add_item(name, unit_price, quantity)` | Adauga un produs valid in cos |
| `subtotal()` | Calculeaza suma produselor fara taxe, discount si transport |
| `discount()` | Aplica discount pentru comenzi de minimum 500 lei |
| `shipping_cost()` | Decide daca transportul este gratuit sau standard |
| `vat()` | Calculeaza TVA-ul dupa aplicarea discountului |
| `total()` | Calculeaza totalul final al comenzii |
| `classify_cart()` | Clasifica cosul: gol, standard, transport gratuit, discount aplicat |

## Configuratie

Configuratie software folosita:

| Componenta | Versiune |
|---|---|
| Sistem de operare | Windows |
| Python | 3.13.7 |
| Framework testare | `unittest`, inclus in biblioteca standard Python |
| Masina virtuala | Nu a fost folosita |
| Dependinte externe | Nu sunt necesare |

Configuratia hardware trebuie completata cu datele calculatorului pe care se face predarea finala, de exemplu: procesor, memorie RAM si tip stocare.

## Rulare

Din radacina repository-ului:

```powershell
python -m unittest discover -s tests -p "test_*.py"
python scripts\mutation_report.py --suite base
python scripts\mutation_report.py --suite full
```

Pentru raport de coverage cu biblioteca `coverage.py`:

```powershell
pip install -r requirements.txt
python -m coverage run -m unittest discover -s tests -p "test_*.py"
python -m coverage report -m
python -m coverage html
```

Raportul HTML se genereaza local in `htmlcov/index.html`. Folderul `htmlcov/`
nu se urca pe Git, deoarece este generat automat.

Exista si un raport local simplificat, fara dependinte externe:

```powershell
python scripts\coverage_report.py
```

Rezultat teste unitare:

```text
Ran 16 tests
OK
```

Rezultat acoperire:

```text
Statement coverage for shopping_cart.py: 100.00%
Covered executable lines: 31/31
Missing executable lines: none
```

## Strategii de generare a testelor

### Partitionare in clase de echivalenta

| Functionalitate | Clase valide | Clase invalide | Exemple teste |
|---|---|---|---|
| Nume produs | sir nevid dupa eliminarea spatiilor | sir gol, doar spatii | `"Mouse"`, `""`, `"   "` |
| Pret unitar | numar pozitiv | zero sau negativ | `100`, `0`, `-1` |
| Cantitate | intreg pozitiv | zero, negativ, numar neintreg | `1`, `2`, `0`, `-1`, `1.5` |
| Subtotal | sub 300, intre 300 si 499.99, minimum 500 | cos gol | `0`, `299.99`, `300`, `499.99`, `500` |

### Analiza valorilor de frontiera

| Granita | Valori testate | Motiv |
|---|---:|---|
| pret valid minim | `0`, `-1`, valori pozitive | verifica respingerea preturilor invalide |
| cantitate valida minima | `0`, `-1`, `1`, `1.5` | verifica validarea cantitatii |
| prag transport gratuit | `299.99`, `300` | diferentiaza transport standard de transport gratuit |
| prag discount | `499.99`, `500` | diferentiaza lipsa discountului de discount 10% |
| cos gol | `0` | verifica total, transport si clasificare pentru cos fara produse |

### Acoperire instructiuni, decizii si conditii

Raportul local arata 100% acoperire pe liniile executabile ale clasei. Deciziile importante acoperite sunt:

| Decizie | Ramura adevarata | Ramura falsa |
|---|---|---|
| nume produs invalid | testata | testata |
| pret invalid | testata | testata |
| cantitate invalida | testata | testata |
| cantitate non-int | testata | testata |
| subtotal peste prag discount | testata | testata |
| cos gol pentru transport | testata | testata |
| subtotal dupa discount peste prag transport gratuit | testata | testata |
| clasificare cos gol/standard/transport gratuit/discount | testata | testata |

### Circuite independente

Fluxurile independente principale sunt:

1. Produs invalid: metoda `add_item` arunca exceptie.
2. Cos gol: subtotal, transport si total sunt zero.
3. Comanda mica: se adauga transport standard.
4. Comanda la pragul de 300 lei: transportul devine gratuit.
5. Comanda sub 500 lei: nu se aplica discount.
6. Comanda la pragul de 500 lei: se aplica discount.
7. Comanda mare: discountul se aplica inainte de TVA.

Aceste fluxuri sunt acoperite in `tests/test_shopping_cart_base.py` si `tests/test_shopping_cart_extra.py`.

## Analiza de mutanti

Scriptul `scripts/mutation_report.py` modifica temporar codul sursa in copii izolate si ruleaza testele. Mutantii sunt considerati omorati cand suita de teste esueaza pe varianta modificata.

Suita initiala:

| Mutant | Status |
|---|---:|
| M01_vat_19_to_20 | KILLED |
| M02_discount_threshold_500_to_600 | KILLED |
| M03_discount_rate_10_to_5 | KILLED |
| M04_free_shipping_300_to_400 | SURVIVED |
| M05_standard_shipping_20_to_10 | KILLED |
| M06_discount_boundary_ge_to_gt | KILLED |
| M07_shipping_boundary_ge_to_gt | SURVIVED |
| M08_allow_zero_price | KILLED |
| M09_remove_name_trim | SURVIVED |
| M10_classification_boundary_300_to_301 | SURVIVED |

Scor mutatie initial: 6/10 = 60%.

Dupa adaugarea testelor suplimentare:

| Mutant | Status |
|---|---:|
| M01_vat_19_to_20 | KILLED |
| M02_discount_threshold_500_to_600 | KILLED |
| M03_discount_rate_10_to_5 | KILLED |
| M04_free_shipping_300_to_400 | KILLED |
| M05_standard_shipping_20_to_10 | KILLED |
| M06_discount_boundary_ge_to_gt | KILLED |
| M07_shipping_boundary_ge_to_gt | KILLED |
| M08_allow_zero_price | KILLED |
| M09_remove_name_trim | KILLED |
| M10_classification_boundary_300_to_301 | KILLED |

Scor mutatie final: 10/10 = 100%.

Exemple de teste adaugate ca sa omoare mutanti neechivalenti ramasi in viata:

| Mutant | Test suplimentar | Explicatie |
|---|---|---|
| M04 | `test_free_shipping_boundary` | Verifica exact pragul de 300 lei pentru transport gratuit. |
| M07 | `test_free_shipping_boundary` | Diferentiaza `>= 300` de `> 300`. |
| M09 | `test_item_name_is_trimmed` | Verifica eliminarea spatiilor din numele produsului. |
| M10 | `test_cart_classification_boundaries` | Verifica incadrarea corecta la pragul de 300 lei. |

## Raport despre folosirea unui tool de AI

Tool folosit: ChatGPT / Codex, https://chatgpt.com/, data generarii: 2 mai 2026.

Am folosit pentru verificari, explicatii bug-uri, etc.

## Diagrama

Diagrama fluxului de calcul este in `docs/diagrams/decision_flow.drawio` si poate fi deschisa cu https://app.diagrams.net. Ea nu este imagine fotografiata sau scanata, ci fisier editabil creat cu un instrument dedicat.

## L5 - CI/CD

Pipeline-ul GitHub Actions din `.github/workflows/ci.yml` ruleaza automat la
fiecare push sau pull request pe ramura `main`/`master`.

Pipeline-ul:

1. instaleaza dependintele din `requirements.txt`;
2. ruleaza toate testele unitare;
3. genereaza coverage cu branch coverage;
4. esueaza daca acoperirea scade sub 80%;
5. publica raportul HTML de coverage ca artefact;
6. ruleaza mutation testing intr-un job separat, optional;
7. publica rezultatele mutation testing ca artefact.

## Referinte

[1] Python Software Foundation, `unittest` - Unit testing framework, https://docs.python.org/3/library/unittest.html, Data ultimei accesari: 2 mai 2026.

[2] Python Software Foundation, `trace` - Trace or track Python statement execution, https://docs.python.org/3/library/trace.html, Data ultimei accesari: 2 mai 2026.

[3] Aniche, Mauricio, Effective Software Testing: A developer's guide, Manning Publications, 2022.

[4] Khorikov, Vladimir, Unit Testing Principles, Practices, and Patterns, Manning Publications, 2020.
