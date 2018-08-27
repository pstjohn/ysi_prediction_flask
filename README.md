# Flask App for YSI prediction


The only tricky dependency here is [`rdkit`](http://www.rdkit.org/docs/Install.html), but it can be installed with 
```
conda install -c conda-forge rdkit
```


The dependencies are therefore
* rdkit
* pandas
* seaborn (for colors)
* flask
* wtforms

## To update submodules (add new compounds)
`git submodule foreach git pull origin master`

## To launch a local server:
```
cd ysipred
gunicorn --bind 0.0.0.0:2222 main:app
```

Then browse to 0.0.0.0:2222 in a web browser


## To deploy new changes to website

```
heroku container:login
heroku container:push web --app ysipred
heroku container:release web --app ysipred
```
