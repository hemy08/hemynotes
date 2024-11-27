python make_mkdocs_yml.py

xcopy /E /I /Y "themes" "docs\\themes"

mkdocs serve --dirty -a localhost:14520 -o -f mkdocs.yml

pause