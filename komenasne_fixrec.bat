@echo off
setlocal enabledelayedexpansion

rem �o�b�`�t�@�C���̃f�B���N�g�����擾
set "currentDir=%~dp0"

if "%~1"=="" (
    echo �t�@�C�������̃o�b�`�t�@�C���Ƀh���b�O���h���b�v���Ă��������B
    pause
    exit /b
)

rem �h���b�O���ꂽ�t�@�C���̖��O��\��
for %%i in (%*) do (
    set "file=%%~i"
    set "filename=%%~nxi"
    echo �h���b�O���ꂽ�t�@�C����: !filename!
)

:input_minutes
set /p minutes=������͂��Ă��������i��: 30�j: 
rem ���͂������ł��邱�Ƃ��m�F
set "isnum=1"
for /l %%i in (0,1,9) do (
    if "!minutes:~%%i,1!" geq "0" if "!minutes:~%%i,1!" leq "9" (
        rem �������Ȃ�
    ) else (
        set "isnum=0"
    )
)

if "!isnum!"=="1" (
    goto run_command
) else (
    echo ��������͂��Ă��������B
    goto input_minutes
)

:run_command
rem �h���b�O���h���b�v���ꂽ�t�@�C��������
for %%i in (%*) do (
    set "file=%%~i"
    set "filename=%%~nxi"
    echo Running: "%currentDir%komenasne.exe" --fixrec !minutes! "!filename!"
    "%currentDir%komenasne.exe" --fixrec !minutes! "!filename!"
)

pause
endlocal
exit /b
