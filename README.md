# CivicSafe AI

**Report local civic issues with location and photos, and use computer vision to help classify them for review.**

CivicSafe AI is a Flutter client and FastAPI service for submitting and managing civic issue reports. Citizens can submit a photo with GPS coordinates; the backend runs the included YOLO weights, stores reports and image data in PostgreSQL, and provides role-restricted review and analytics endpoints.

## The problem and approach

Civic issues are difficult to route and track when reports lack consistent locations, evidence, and status updates. CivicSafe AI combines photo-based reporting, location capture, issue classification, and status tracking in one application. Its configured geographic area is Hyderabad, India.

## Implemented features

- Email/password registration and JWT-based sign-in.
- Citizen report submission with an image, GPS coordinates, and optional description.
- YOLO-based image classification using the model weight files included with the backend.
- Report history for citizens; report lists and summary charts for administrators.
- Authority endpoint to mark a report resolved.
- PostgreSQL-backed records and image storage, plus an Excel analytics export.
- Interactive FastAPI/OpenAPI documentation.

New registrations are citizens only. Admin and authority access must be granted out of band; public registration must not be used to create privileged accounts.

## Architecture and technology

- **Client:** Flutter/Dart, Material Design, Provider, `http`, `geolocator`, `image_picker`, and `fl_chart`.
- **API:** Python 3.11 or 3.12, FastAPI, Pydantic Settings, SQLAlchemy async, and Uvicorn.
- **Data and detection:** PostgreSQL via `asyncpg`; Pillow, NumPy, and Ultralytics YOLO.
- **Analytics export:** `openpyxl`.

The Flutter app sends REST requests to FastAPI. The API verifies JWTs and role permissions, persists reports/detections/images in PostgreSQL, and loads the available `.pt` model weights at startup.

## Repository layout

```text
.
├── civicsafe-backend-main/
│   └── civicsafe-backend-main/       # FastAPI API, models, and YOLO weights
└── civicSafe-frontend-master/
    └── civicSafe-frontend-master/   # Flutter app for web, Android, and iOS
```

The repeated directory names are retained from the supplied project layout. Run commands from the inner application directory shown below.

## Requirements

- Python 3.11 or 3.12 and [uv](https://docs.astral.sh/uv/) (or pip).
- Flutter SDK compatible with the Dart SDK constraint in `pubspec.yaml`; Chrome for web.
- A PostgreSQL database. Local PostgreSQL may use `sslmode=disable`; hosted databases should use TLS.
- For mobile builds, the corresponding Android or macOS/iOS toolchain.
- On mobile, grant location and photo/camera access when prompted; local device builds also need a reachable API URL.

## Local setup

### 1. Configure and run the API

From the repository root:

```powershell
Set-Location civicsafe-backend-main\civicsafe-backend-main
Copy-Item .env.example .env
```

Edit `.env` and set `DATABASE_URL` to a `postgresql+asyncpg://` PostgreSQL connection string and `SECRET_KEY` to a long, random value. For example, generate a key with:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

The local example connection uses `sslmode=disable`; do not use that setting for a hosted database. Keep `.env` and database credentials private.

Install and start the API:

```powershell
uv sync
uv run uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

The API docs are available at `http://127.0.0.1:8000/docs`; interactive ReDoc is at `http://127.0.0.1:8000/redoc`.

For pip instead of uv, create and activate a virtual environment in the backend directory, then run:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

### 2. Run the Flutter client

In a second terminal, from the repository root:

```powershell
Set-Location civicSafe-frontend-master\civicSafe-frontend-master
flutter pub get
flutter run -d chrome --web-port 8080 --dart-define=API_BASE_URL=http://127.0.0.1:8000
```

Set `API_BASE_URL` to the reachable API origin when using another host or device. `API_URL` in the backend `.env` must also be that reachable origin because report responses include image URLs. Add the browser origin to `CORS_ORIGINS` in the backend `.env` when changing the web host or port.

## Checks and production builds

Run Flutter analysis and tests from the frontend directory:

```powershell
flutter analyze
flutter test
flutter build web --release --dart-define=API_BASE_URL=https://your-api-host
```

The current Flutter test is only a placeholder smoke test. No automated backend test suite is included. An Android APK can be built with:

```powershell
flutter build apk --release --dart-define=API_BASE_URL=https://your-api-host
```

Release signing is not configured in this project.

## Limitations and release notes

- The area classification and client location defaults are specific to Hyderabad.
- Admin and authority users require trusted out-of-band provisioning; there is no account-management or initial-admin workflow.
- SQLAlchemy `create_all` creates missing tables but does not migrate existing schemas. Back up data and apply a proper migration before changing a deployed database schema.
- Detection quality depends on the included weights and image quality. Treat classifications as assistance, not verified findings.
- Upload size limits, production deployment configuration, and mobile release signing are not set up here. Configure and test these before public use.
- No project license file or genuine screenshots were present. Choose a license only after confirming rights to all source code and model weights; no author or model ownership is claimed here.

## Before publishing

Review the configuration and model asset licensing, set up role provisioning and production database/CORS settings, then create a new repository without copying any pre-existing Git history. These are the commands once the remote repository has been created:

```powershell
git init -b main
git add .
git status
git commit -m "Prepare CivicSafe AI portfolio project"
git remote add origin https://github.com/<YOUR_USERNAME>/civicsafe-ai.git
git push -u origin main
```

Replace `<YOUR_USERNAME>` with your GitHub username. These commands are provided for you to run; this workspace has not been initialized as a Git repository, and nothing has been published.
