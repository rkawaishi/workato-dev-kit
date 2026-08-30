@echo off
rem Windows launcher for the workato-kit wk plugin.
rem wk resolves the extension-less entrypoint through PATHEXT.
python "%~dp0workato_kit.py" %*
