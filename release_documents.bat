python make_mkdocs_yml.py

git add *

git commit -m "更新发布文档"

git push

xcopy /E /I /Y "themes" "docs\\themes"

git branch -D gh-pages

git push

pause

mkdocs gh-deploy -f mkdocs.yml

pause