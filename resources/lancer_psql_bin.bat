@echo off
REM Script pour lancer PowerShell et se positionner dans le répertoire bin de PostgreSQL.

SET PG_HOME="C:\Program Files\PostgreSQL\17"
SET PG_BIN=%PG_HOME%\bin

echo Lancement de PowerShell et positionnement dans %PG_BIN%...

REM Lance PowerShell, exécute la commande 'cd' vers le répertoire bin, et maintient la fenêtre ouverte (-NoExit)
PowerShell.exe -NoExit -Command "cd '%PG_BIN%'"