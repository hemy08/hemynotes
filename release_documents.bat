python make_mkdocs_yml.py

git commit -m "更新文档"

git push

pause

xcopy /E /I /Y "themes" "docs\\themes"

git branch -D gh-pages

git push

pause

mkdocs gh-deploy -f mkdocs.yml

pause