@echo off
setlocal

:: --- 設定：実行したいPythonファイル名をここに記述 ---
set TARGET_PY=main_gui.py
:: -----------------------------------------------

echo [1/3] Pythonのインストール状態を確認中...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Pythonが見つかりません。インストールを開始します...
    :: wingetでPythonをインストール
    winget install Python.Python.3.12 --exact --silent --accept-source-agreements --accept-package-agreements
    
    if %errorlevel% neq 0 (
        echo [ERROR] インストールに失敗しました。インターネット接続や権限を確認してください。
        pause
        exit /b
    )
    
    echo [SUCCESS] インストール完了。環境変数を一時的に更新します。
    :: インストール直後はパスが通っていないため、標準的なパスを一時的に追加
    set "PATH=%LOCALAPPDATA%\Programs\Python\Python312\;%LOCALAPPDATA%\Programs\Python\Python312\Scripts\;%PATH%"
) else (
    echo [OK] Pythonは既にインストールされています。
)

echo [2/3] 依存ライブラリのチェック（必要に応じて追加）
:: 必要であればここで pip install を実行できます
:: python -m pip install -r requirements.txt

echo [3/3] %TARGET_PY% を実行します...
echo ---------------------------------------
if exist "%TARGET_PY%" (
    python "%TARGET_PY%"
) else (
    echo [ERROR] %TARGET_PY% が見つかりません。ファイル名を確認してください。
)

echo ---------------------------------------
echo 処理が終了しました。
pause