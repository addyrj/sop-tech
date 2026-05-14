@echo off
setlocal enabledelayedexpansion

:: Try multiple methods to get UUID (works on all Windows versions)
set "uuid="

:: Method 1: PowerShell (Windows 7+)
for /f "delims=" %%a in ('powershell -Command "Get-WmiObject Win32_ComputerSystemProduct | Select-Object -ExpandProperty UUID" 2^>nul') do (
    set "uuid=%%a"
)

:: Method 2: WMIC (Old Windows, if PowerShell fails)
if "!uuid!"=="" (
    for /f "skip=1 delims=" %%a in ('wmic csproduct get uuid 2^>nul') do (
        if not "%%a"=="" set "uuid=%%a" & goto :found
    )
)
:found

:: Method 3: Registry (Last resort)
if "!uuid!"=="" (
    for /f "delims=" %%a in ('reg query "HKLM\SOFTWARE\Microsoft\Cryptography" /v MachineGuid 2^>nul ^| findstr "REG_SZ"') do (
        set "line=%%a"
        set "uuid=!line:*REG_SZ=!"
        set "uuid=!uuid:~1!"
    )
)

:: Show and copy to clipboard
if not "!uuid!"=="" (
    echo !uuid! | clip
    msg * "UUID: !uuid! (Copied to clipboard)"
) else (
    msg * "ERROR: Could not retrieve UUID"
)