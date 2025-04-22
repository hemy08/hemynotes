python make_mkdocs_yml.py

REM git commit -m "更新文档"

REM git push

REM pause

xcopy /E /I /Y "themes" "docs\\themes"

git branch -D gh-pages

git push

pause

mkdocs gh-deploy -f mkdocs.yml

git checkout gh-pages

git add *

git commit -m "更新发布文档"

git push

pause