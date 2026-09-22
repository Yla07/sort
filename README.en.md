# Sort

Sort is a small sorting visualizer implemented in three editions:

- a Python command-line interface;
- a Python/PyQt6 desktop interface;
- a Python HTTP server with a browser interface;
- an Android Jetpack Compose application.

All editions provide bubble, quick, insertion, and selection sorting. The Python and web editions share the implementation in `backend.py`. The Android edition keeps its algorithms in `android/app/src/main/java/com/example/sortowanie/SortAlgorithms.kt`.

## Requirements

- Python 3.10 or newer. The test suite uses only the Python standard library.
- PyQt6 for the desktop GUI: `python -m pip install PyQt6`.
- A JDK and Android SDK for the Android application. Android builds use the Gradle wrapper in `android/`.

## Run the Python applications

From the project root:

```text
python cli.py
python gui.py
python server.py
```

The web application is available at <http://127.0.0.1:8000> after starting `server.py`.

## Run the tests

Python unit and integration tests:

```text
python -m unittest discover -s tests -v
```

This covers the sorting engine, CLI flows, HTTP API validation, and static web files. The GUI is not imported by automated tests because PyQt6 is an optional desktop dependency.

Android local unit tests:

```text
cd android
./gradlew testDebugUnitTest
```

Android instrumentation tests require a connected device or emulator:

```text
cd android
./gradlew connectedDebugAndroidTest
```

## HTTP API

- `GET /api/health` returns the service status.
- `GET /api/data` returns the current list.
- `POST /api/data` replaces the list with `{ "data": [1, 2, 3] }`.
- `POST /api/generate` accepts `min`, `max`, and `size`.
- `POST /api/sort` accepts `algorithm`: `bubble`, `quick`, `insertion`, or `selection`.
- `DELETE /api/data` clears the list.

## Repository layout

| Path | Purpose |
| --- | --- |
| `backend.py` | Python sorting engine and data store |
| `cli.py` | Terminal interface |
| `gui.py` | PyQt6 desktop interface |
| `server.py` | HTTP API and static file server |
| `web/` | Browser interface |
| `android/` | Android Compose application |
| `tests/` | Python automated tests |
