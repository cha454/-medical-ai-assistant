@echo off
echo ========================================
echo   CONFIGURATION API - ASSISTANT MEDICAL
echo ========================================
echo.

REM Vérifier si .env existe
if exist .env (
    echo [OK] Fichier .env existe deja
    echo.
    choice /C ON /M "Voulez-vous l'ouvrir pour editer"
    if errorlevel 2 goto TEST
    if errorlevel 1 goto EDIT
) else (
    echo [INFO] Creation du fichier .env...
    copy .env.example .env
    echo [OK] Fichier .env cree !
    echo.
    goto EDIT
)

:EDIT
echo.
echo ========================================
echo   EDITION DU FICHIER .env
echo ========================================
echo.
echo Instructions:
echo 1. Obtenir une cle API Google Gemini (GRATUIT):
echo    https://makersuite.google.com/app/apikey
echo.
echo 2. Copier la cle (commence par AIza...)
echo.
echo 3. Coller dans le fichier qui va s'ouvrir:
echo    GOOGLE_API_KEY=ta_cle_ici
echo.
echo 4. Sauvegarder et fermer
echo.
pause
notepad .env
echo.

:TEST
echo.
echo ========================================
echo   TEST DES INTEGRATIONS
echo ========================================
echo.
python test_api_integration.py
echo.
echo ========================================
echo   RESULTAT
echo ========================================
echo.
choice /C ON /M "Voulez-vous lancer l'application"
if errorlevel 2 goto END
if errorlevel 1 goto RUN

:RUN
echo.
echo Lancement de l'application...
echo Acces: http://localhost:5000
echo.
python app.py

:END
echo.
echo ========================================
echo   RESSOURCES UTILES
echo ========================================
echo.
echo - Guide complet: GUIDE_INTEGRATION_FR.md
echo - Obtenir cles API: OBTENIR_CLE_API.md
echo - Documentation API: API_DOCUMENTATION.md
echo.
pause
