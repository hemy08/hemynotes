python make_mkdocs_yml.py

xcopy /E /I /Y "themes" "docs\\themes"

git branch -D gh-pages

git push

mkdocs gh-deploy -f mkdocs.yml

pause