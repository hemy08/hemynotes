python make_mkdocs_yml.py

xcopy /E /I /Y "themes" "docs\\themes"

mkdocs gh-deploy -f mkdocs.yml

pause