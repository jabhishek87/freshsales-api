# freshsales-api
:memo: freshsales-api


### clone the repo
``` git clone https://github.com/jkabhishek/freshsales-api.git ```
### install the python dependencies
```
sudo pip install -r requirements.txt
```

### copy the settings template and update reuired values
``` cp settings.py.sample settings.py ```

```python
# your fresh sales url with api appended 
BASE_URI = "https://testfrshslscrm.freshsales.io/api/"

# your api key
api_key = "<your-api-key>"
```

### Run the command for help
``` python csfs.py --help ```

### commands example
``` 
# list all leads
python csfs.py listlead

# list all contacts
python csfs.py listcontacts

# update lead
python csfs.py addlead --email test3@gmail.com

# create notes
python csfs.py addnote --email test3@gmail.com --note "new node added \n update1"
```
