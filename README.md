![Pytest](https://github.com/dburnsii/bartender/actions/workflows/pytest.yml/badge.svg)
# The Bartender

[![Product Video](https://imgur.com/6ZcyR7p.png)](https://youtu.be/YWqvJ5PAxSI)

The Bartender is an intelligent, robotic, drink-making machine. It's made to
display your bottles and pour you a cocktail just the way you like. The scale
ensures your ingredients are measured precisely, and the touchscreen interface
makes it easy to use. Each led in the light strip above the bottle deck can be
controlled individually, meaning they can highlight an empty bottle for you,
or they can put on a gentle light show to provide ambiance to a room. All told,
the Bartender is the perfect addition to any bar setup to make it quick, easy,
and fun to enjoy a casual drink, or to keep your guests glasses full.

## Contents
 - [About the Project](#About-the-Project)
 - [Getting Started](#Getting-Started)
 - [Hardware](#Hardware)
 - [Software](#Software)
 - [Contributing](#Contributing)
 - [Roadmap](#Roadmap)
 - [Contacts](#Contacts)

### About the Project
**The Bartender**'s design is made to integrate into a room first, and to easily
pour drinks second. The problem with many drink making machines is the need for
dedicated table space, which makes it feel like an appliance rather than a part
of your setup. With two drawers for storage, and knobs or handles on the front
side, **The Bartender** feels like a cabinet with some extra wizardry, and can
also hold things like Margarita Salt or tools like a stirrer.

[Demo Video](https://youtu.be/VJUhfgaUki0)

### Getting Started
The Bartender calls for equal parts hardware and software, so some woodworking
and soldering is required. Currently you'll have to buy the components and
assemble yourself, but if the project gains popularity, kits may become available.

### Hardware
As mentioned above, you'll need to do some woodworking to get the drinks
flowing. The cut list is available in the `hardware` directory, and the BOM
is available there as well. After purchasing and assembling the required
hardware, you can move on to getting the Raspberry Pi set up.

### Software
#### Build Time
- [**Kicad**](https://www.kicad.org/) - PCBs
- [**FreeCad**](https://www.freecadweb.org/) - 3D Models
- [**Platform.io**](https://platformio.org/) - For Arduino Companion

#### Run Time
 - [**Raspberry Pi OS**](https://www.raspberrypi.org/software/) - Operating System
 - [**React**](https://reactjs.org/) - Frontend
 - [**Python**](https://www.python.org/) - Backend Microservices

#### Installation
 1. Install [Raspberry Pi OS](https://www.raspberrypi.org/software/) on your Pi
 2. Clone this repo into your Home Directory of choice
 3. Run the `./install.sh` script from inside the bartender directory to get
 set up.
 4. Reboot and grab a glass!

#### Updating
  1. `git pull` this repo to get the latest changes
  2. Rerun the `./install.sh` script
  3. Reboot the pi (Note: The reinstallation currently wipes out the pump database, so you'll need to repopulate the list of loaded bottles).

### Contributing
This project is still in the early phases and the repo is subject
to changes and reorganization. Feel free to make suggestions and
submit a pull request for any desired features.

### Roadmap
The end goal for this project is to provide assembled units for anyone to use,
but getting there is a huge undertaking. With the help of contributors,
**The Bartender** can get there, but even if it doesn't, it's a fun project
to play with, and a great way to learn many different skills.

### License

See [LICENSE](LICENSE)

### Contacts
Desone Burns II - dburnsii@live.com - https://desone.dev
