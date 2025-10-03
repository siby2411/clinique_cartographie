@echo off
REM Script pour activer l'environnement virtuel et se positionner dans le répertoire du projet.

REM Change le répertoire vers l'emplacement actuel du script (C:\sante_dakar_api)
cd /d "%~dp0"

echo Activation de l'environnement virtuel...
REM Le chemin standard de l'activation sous Windows
call venv\Scripts\activate.bat

echo.
echo Vous êtes maintenant dans le répertoire C:\sante_dakar_api (venv)
echo.

REM Laissez la console ouverte après l'exécution
cmd /k