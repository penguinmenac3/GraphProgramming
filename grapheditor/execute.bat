@set /p pathName=Enter GraphName: %=%
@python ../python/graphex.py data/%pathName%.graph.json
@pause