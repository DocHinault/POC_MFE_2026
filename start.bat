@echo off
REM MG - POC V1 - Script de démarrage pour Windows

echo.
echo 🚀 Démarrage de MG - POC V1 - Social Media Reporting
echo ==================================================
echo.

REM Vérifier Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé ou n'est pas sur le PATH
    pause
    exit /b 1
)

echo ✅ Python trouvé
echo.

REM Installer les dépendances
echo 📦 Installation des dépendances...
pip install -r requirements.txt >nul 2>&1

if errorlevel 1 (
    echo ❌ Erreur lors de l'installation des dépendances
    pause
    exit /b 1
)

echo ✅ Dépendances installées
echo.

REM Tester la configuration
echo 🔍 Vérification de la configuration...
python test_config.py

if errorlevel 1 (
    echo ❌ Configuration incomplète
    pause
    exit /b 1
)

echo.
echo 🎉 Configuration OK!
echo.
echo Lancement de l'application...
echo L'application sera disponible sur: http://localhost:8501
echo.
echo Appuyez sur Ctrl+C pour arrêter l'application
echo.

REM Lancer l'application
streamlit run streamlit_app.py

pause
