@echo off
echo === Basic Test ===
echo Test 1: No parameters (interactive mode)
py main.py
echo.

echo Test 2: Only VFS root
py main.py --vfs-root .\test_vfs
echo.

echo Test 3: Only script
py main.py --start-script "start.py"
echo.

echo Test 4: Both parameters
py main.py --vfs-root .\test_vfs --start-script "start.py"
echo.

echo Test 5: Short flags
py main.py -r .\test_vfs -s "start.py"
echo.

echo Test 6: Help message
py main.py --help
echo.

echo Test 7: Code Test
py main.py -r vfs.xml -s start.txt
echo.

echo LCE test completed!
pause