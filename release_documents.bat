python make_mkdocs_yml.py

REM git add *

REM git commit -m "更新发布文档"

REM git push

xcopy /E /I /Y "themes" "docs\\themes"

git branch -D gh-pages

git push

pause

mkdocs gh-deploy -f mkdocs.yml

pause