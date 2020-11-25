sudo apt update
sudo apt upgrade -y
sudo apt install -y libsystemd-dev mongodb


curl -sL https://deb.nodesource.com/setup_10.x | sudo bash -
sudo apt update
sudo apt install -y nodejs

# Disable welcome prompt on login
sudo rm /etc/xdg/autostart/piwiz.desktop

# Disable screen sleep
echo "xset s 0 && xset -dpms" > ~/.xinitrc

# Enable backlight control for non-root user
echo 'SUBSYSTEM=="backlight",RUN+="/bin/chmod 666 /sys/class/backlight/%k/brightness /sys/class/backlight/%k/bl_power"' | sudo tee -a /etc/udev/rules.d/backlight-permissions.rules

# Install requirements for the backend
cd backend
pip3 install -r requirements.txt

# Setup mongodb database
cd database_server
python3 init_db.py

cd ..

cd ..

# Build the frontend into servable files
cd frontend
npm install
npm run build
cd ..

# Setup Arduino for Companion app
cd companion
pip3 install platformio
pio run
cd ..

# Install Systemd services
sed  's%\[BARTENDERDIR\]%'"$PWD"'%g' systemd/central.template | sudo tee /usr/lib/systemd/system/central.service
sudo systemctl enable central

sed  's%\[BARTENDERDIR\]%'"$PWD"'%g' systemd/database.template | sudo tee /usr/lib/systemd/system/database.service
sudo systemctl enable database

sed  's%\[BARTENDERDIR\]%'"$PWD"'%g' systemd/valve.template | sudo tee /usr/lib/systemd/system/valve.service
sudo systemctl enable valve

sed  's%\[BARTENDERDIR\]%'"$PWD"'%g' systemd/scale.template | sudo tee /usr/lib/systemd/system/scale.service
sudo systemctl enable scale

sed  's%\[BARTENDERDIR\]%'"$PWD"'%g' systemd/led.template | sudo tee /usr/lib/systemd/system/led.service
sudo systemctl enable led

sed  's%\[BARTENDERDIR\]%'"$PWD"'%g' systemd/frontend.template | sudo tee /usr/lib/systemd/system/frontend.service
sudo systemctl enable frontend

sed  's%\[BARTENDERDIR\]%'"$PWD"'%g' systemd/kiosk.template | sudo tee /usr/lib/systemd/system/kiosk.service
sudo systemctl enable kiosk

# TODO: add "-nocursor -s 0" to lightdm.conf, and set "EmulateThridButton 0" in /usr/share/xorg.conf.d/99-calibration.conf
