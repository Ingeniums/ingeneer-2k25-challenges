@echo off
setlocal enabledelayedexpansion

:: Collect categories
set "categories="
for /d %%d in (*) do (
    set "categories=!categories! %%d"
)
set "categories=%categories:~1%"

:: Prompt for category
:category_prompt
set "category="
set /p "category=category (values: %categories% )> "
if not defined category goto :category_prompt

:: Validate category
set "found="
for %%c in (%categories%) do (
    if "%%c"=="%category%" set "found=1"
)
if not defined found (
    echo Invalid category.
    exit /b 1
)

:: Prompt for author
:author_prompt
set "author="
set /p "author=author> "
if not defined author goto :author_prompt

:: Prompt for difficulty
:diff_prompt
set "diff="
set /p "diff=difficulty (values: warmup easy medium hard tough )> "
if not defined diff goto :diff_prompt

:: Validate difficulty
set "valid="
for %%d in (warmup easy medium hard tough) do (
    if "%%d"=="%diff%" set "valid=1"
)
if not defined valid (
    echo Invalid difficulty.
    exit /b 1
)

:: Prompt for challenge name
:name_prompt
set "name="
set /p "name=challenge name> "
if not defined name goto :name_prompt

:: Create directory structure
set "target_dir=%category%\%diff%-[%name%]"
mkdir "%target_dir%\challenge" 2>nul
mkdir "%target_dir%\solution" 2>nul
type nul > "%target_dir%\challenge\.gitkeep"
type nul > "%target_dir%\solution\.gitkeep"

:: Generate challenge.yml
if not exist "challenge.yml" (
    echo Error: challenge.yml template not found.
    exit /b 1
)

(
    for /F "usebackq delims=" %%L in ("challenge.yml") do (
        set "line=%%L"
        setlocal enabledelayedexpansion
        set "line=!line:{{name}}=%name%!"
        set "line=!line:{{difficulty}}={{%diff%}}!"
        set "line=!line:{{author}}=%author%!"
        set "line=!line:{{category}}=category!"
        echo(!line!
        endlocal
    )
) > "%target_dir%\challenge.yml"

echo Directory structure and challenge.yml created successfully.
endlocal
