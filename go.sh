rm -rf dist/* && uv add --dev twine && uv build && twine upload dist/*
sleep 15
uv cache clear

sleep 15

uv tool install transpilatron==$VER