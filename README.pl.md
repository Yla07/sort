# Sort

Sort to niewielki wizualizator sortowania dostepny w czterech wersjach:

- interfejs wiersza polecen dla Pythona;
- aplikacja desktopowa Python/PyQt6;
- serwer HTTP w Pythonie z interfejsem w przegladarce;
- aplikacja Android wykorzystujaca Jetpack Compose.

Kazda wersja udostepnia sortowanie babelkowe, szybkie, przez wstawianie i przez wybieranie. Wersje Python i web korzystaja ze wspolnej implementacji w pliku `backend.py`. Wersja Android przechowuje algorytmy w `android/app/src/main/java/com/example/sortowanie/SortAlgorithms.kt`.

## Wymagania

- Python 3.10 lub nowszy. Testy korzystaja tylko ze standardowej biblioteki Pythona.
- PyQt6 dla aplikacji desktopowej: `python -m pip install PyQt6`.
- JDK i Android SDK dla aplikacji Android. Kompilacja Android korzysta z wrappera Gradle w katalogu `android/`.

## Uruchamianie aplikacji Python

Z katalogu glownego projektu:

```text
python cli.py
python gui.py
python server.py
```

Po uruchomieniu `server.py` aplikacja webowa jest dostepna pod adresem <http://127.0.0.1:8000>.

## Uruchamianie testow

Testy jednostkowe i integracyjne Pythona:

```text
python -m unittest discover -s tests -v
```

Testy obejmuja silnik sortowania, scenariusze CLI, walidacje API HTTP oraz pliki statyczne aplikacji webowej. GUI nie jest importowane przez testy automatyczne, poniewaz PyQt6 jest opcjonalna zaleznoscia desktopowa.

Lokalne testy jednostkowe Android:

```text
cd android
./gradlew testDebugUnitTest
```

Testy instrumentacyjne Android wymagaja podlaczonego urzadzenia lub emulatora:

```text
cd android
./gradlew connectedDebugAndroidTest
```

## API HTTP

- `GET /api/health` zwraca stan uslugi.
- `GET /api/data` zwraca biezaca liste.
- `POST /api/data` zastepuje liste danymi `{ "data": [1, 2, 3] }`.
- `POST /api/generate` przyjmuje pola `min`, `max` i `size`.
- `POST /api/sort` przyjmuje `algorithm`: `bubble`, `quick`, `insertion` albo `selection`.
- `DELETE /api/data` czysci liste.

## Struktura projektu

| Sciezka | Przeznaczenie |
| --- | --- |
| `backend.py` | Silnik sortowania i przechowywanie danych Python |
| `cli.py` | Interfejs terminalowy |
| `gui.py` | Interfejs desktopowy PyQt6 |
| `server.py` | API HTTP i serwer plikow statycznych |
| `web/` | Interfejs przegladarkowy |
| `android/` | Aplikacja Android Compose |
| `tests/` | Automatyczne testy Pythona |
