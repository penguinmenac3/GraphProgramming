@set /p pathName=Enter GraphName: %=%
@python2 ../python/graphex.py data/%pathName%.graph.json
@pause