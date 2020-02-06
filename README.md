* Bartender

The open-source, modular, autonomous drink making machine!

Installation notes:

```
npm install
pip3 install -r requirements.txt
sudo systemctl enable pigpiod
sudo sysetmctl start pigpiod
python3 manage.py migrate
python3 manage.py runserver
```
