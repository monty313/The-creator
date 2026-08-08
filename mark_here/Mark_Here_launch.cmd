@echo off
REM MARK HERE — portable. Copy this whole mark_here folder anywhere.
REM Live chat if ARMY 01_SYSTEM is on the machine; else opens local knowledge pack.
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0open_markos_second_brain.ps1"
