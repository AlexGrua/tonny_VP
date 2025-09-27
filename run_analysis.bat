@echo off
echo Установка зависимостей...
python -m pip install pandas numpy matplotlib seaborn

echo.
echo Запуск анализа...
python weekly_pricing.py

echo.
echo Анализ завершен! Проверьте папку output/ для результатов.
pause

