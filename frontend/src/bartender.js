import React from 'react';
import Menu from './menu';
import Manual from './manual';
import Search from './search';
import Favorites from './favorites';
import Lights from './lights';
import Settings from './settings';
import DrinkProgress from './components/drinkProgress';
import LockScreen from './components/lockScreen';
import ManualPourProgress from './components/manualPourProgress';
import UpgradeProgress from './components/upgradeProgress';
import ErrorScreen from './components/errorScreen';
import Screensaver from './components/screensaver';
import io from 'socket.io-client';
import throttle from 'lodash.throttle';


class Bartender extends React.Component {
  constructor(props){
    super(props);
    this.changePage = this.changePage.bind(this)
    this.getPage = this.getPage.bind(this)
    this.hideProgress = this.hideProgress.bind(this);
    this.clearError = this.clearError.bind(this);
    this.cancelPour = this.cancelPour.bind(this);
    this.skipManualPour = this.skipManualPour.bind(this);
    this.updateScreenTimeout = this.updateScreenTimeout.bind(this);
    this.updateScreenBrightness = this.updateScreenBrightness.bind(this);
    this.handleCheckForUpdate = this.handleCheckForUpdate.bind(this);
    this.handleAptUpgrade = this.handleAptUpgrade.bind(this);
    this.handleUnlock = this.handleUnlock.bind(this);
    this.setLockPin = this.setLockPin.bind(this);
    this.clearLockPin = this.clearLockPin.bind(this);
    this.socket = io("ws://" + window.location.hostname + ":8080");
    this.weight = 0;
    this.updateWeight = throttle(w => this.setState({weight: w}), 500);
    this.mouseDown = this.mouseDown.bind(this);
    this.state = {
      page: 'favorites',
      metric: false,
      weight: 0,
      presence: false,
      pour_active: false,
      manual_pour_active: false,
      pour_progress: 0,
      manual_pour_progress: 0,
      errorTitle: "",
      errorText: "",
      lastActive: Date.now(),
      idle: true,
      locked: false,
      blankTime: 60 * 1000,
      screenBrightness: 100,
      lockPin: "",
      updateAvailable: null,
      upgradeProgress: 0
    };
  }

  changePage(page){
    this.setState({
      page: page
    })
  }

  updateScreenTimeout(timeout){
    this.setConfig("blank_time", timeout);
    this.setState({blankTime: timeout});
  }

  updateScreenBrightness(brightness){
    this.setState({screenBrightness: brightness})
    this.backendScreenBrightnessUpdate(this, brightness)
  }

  backendScreenBrightnessUpdate = throttle((instance, brightness) => {
    instance.setConfig("screen_brightness", brightness);
    instance.socket.emit("screen_brightness", {"value": brightness})
  }, 500);

  handleCheckForUpdate() {
    this.setState({updateAvailable: null});
    this.socket.emit('apt_update', '');
    console.log("Checking for updates");
  }

  handleAptUpgrade() {
    this.setState({updateAvailable: null});
    this.setState({upgradeProgress: 0.1});
    this.socket.emit('apt_upgrade', '');
    console.log("Starting system upgrade");
  }

  handleUnlock() {
    console.log("Unlocking.")
    this.setState({locked: false});
  }

  setLockPin(pin) {
    this.setConfig("lock_pin", pin);
    this.setState({lockPin: pin});
  }

  clearLockPin() {
    this.deleteConfig("lock_pin");
    this.setState({lockPin: ""});
  }

  activatePump(pin){
  }

  deactivatePump(pin){
  }

  hideProgress(){
    this.setState({pour_active: false, pour_progress: 0})
  }

  hideManualPourProgress(){
    this.setState({manual_pour_active: false, pour_progress: 0})
  }

  clearError() {
    this.setState({errorTitle: "", errorText: ""})
  }

  cancelPour(){
    console.log("Canceling pour.")
    this.socket.emit('abort_pour', '')
  }

  skipManualPour(){
    console.log("Skip manual ingredient")
  }

  mouseDown(e) {
    this.setState({lastActive: Date.now()})
    if(this.state.idle === true){
      this.setState({idle: false});
      e.preventDefault();
      e.stopPropagation();
    }
  }

  getConfig(key, callback){
    fetch("http://" + window.location.hostname + ":5000/config/" + key)
      .then((r) => { console.log(r); console.log(r.ok); if (!r.ok) { console.log("nah") } else { return r }})
      .then((r) => r.json())
      .then((data) => {
        console.log("Got config");
        console.log(data);
        callback(data);
      })
      .catch((error) => {
        console.log("Missing config")
        console.error(error);
        callback(null);
      })
  }

  setConfig(key, value){
    var xhr = new XMLHttpRequest();
    xhr.open("PUT", "http://" + window.location.hostname + ":5000/config");
    xhr.setRequestHeader("key", key);
    xhr.setRequestHeader("value", value);
    xhr.send();
  }

  deleteConfig(key){
    var xhr = new XMLHttpRequest();
    xhr.open("DELETE", "http://" + window.location.hostname + ":5000/config/" + key);
    //xhr.setRequestHeader("key", key);
    xhr.send();
  }

  componentDidMount(){
    this.getConfig('blank_time', (data) => {
      this.setState({blankTime: parseInt(data)})
    })
    this.getConfig('screen_brightness', (data) => {
      this.setState({screenBrightness: parseInt(data)})
    })
    this.getConfig('lock_pin', (data) => {
      this.setState({lockPin: data});
      console.log("Pin: " + data)
    })

    this.socket.on('weight', (data) => {
      this.updateWeight(data['weight']);
      if(this.state.lastActive + this.state.blankTime < Date.now()
         && !this.state.idle
         && this.state.upgradeProgress == 0){
        console.log("Time for bed.");
        this.socket.emit('idle', {});
        this.setState({idle: true});
        if(this.state.lockPin){
          this.setState({locked: true});
        }
      }
    });
    this.socket.on('idle', (data) => {
      this.setState({idle: true});
      if(this.state.lockPin){
        this.setState({locked: true});
      }
    })
    this.socket.on('cup_presence', (data) => {
      this.setState({
        presence: data['present'],
        lastActive: Date.now(),
        idle: false
      });
      console.log("New presence: " + data['present']);
    });
    this.socket.on('connect', () => {
      console.log('Connected');
      this.socket.emit('cup_presence_request', {});
    });
    this.socket.on('error', (data) => {
      console.log("Error!")
      console.log(data)
      this.setState({errorTitle: data["title"], errorText: data["text"]});
    });
    this.socket.on('clear_error', (data) => {
      console.log("Clearing error!");
      console.log(data);
      if(this.state.errorTitle === data["title"]){
        this.setState({errorTitle: "", errorText: ""});
      }
    })
    this.socket.on('drink_pour_active', (data) => {
      console.log("Drink state updated:")
      console.log(data)
      this.setState({
        pour_active: data['status'],
      });
      if("progress" in data) {
        this.setState({
          pour_progress: data['progress']
        });
      }
    });
    this.socket.on('manual_pour_init', (data) => {
      console.log("Start manual pour");
      console.log(data)
      this.setState({manual_pour_active: true, manual_pour_progress: 0, manual_pour_name: data['name']})
    });
    this.socket.on('manual_pour_status', (data) => {
      console.log("Manual pour status update");
      console.log(data);
      this.setState({manual_pour_progress: data['percentage'] * 100, manual_pour_active: !data['complete']})
    });

    // Software updates
    this.socket.on('apt_updates_available', (data) => {
      console.log("Updates available: " + data['status']);
      this.setState({updateAvailable: data['status']});
    });

    this.socket.on('apt_update_progress', (data) => {
      console.log(data);
    });

    this.socket.on('apt_upgrade_progress', (data) => {
      console.log("Upgrade progress: " + data['progress']);
      if(data['progress'] >= 100){
        this.setState({upgradeProgress: data['progress'], updateAvailable: false});
      } else {
        this.setState({upgradeProgress: data['progress']});
      }
    });
  }

  componentWillUnmount(){}

  getPage(page){
    switch(page){
      case 'home':
        return <Favorites socket={this.socket}/>
      case 'search':
        return <Search socket={this.socket}/>
      case 'manual':
        return <Manual weight={this.state.weight} socket={this.socket}
                    presence={this.state.presence} metric={this.state.metric}/>
      case 'lights':
        return <Lights />
      case 'settings':
        return <Settings
                  socket={this.socket}
                  blankTime={this.state.blankTime}
                  screenBrightness={this.state.screenBrightness}
                  lockPin={this.state.lockPin}
                  updateScreenTimeout={this.updateScreenTimeout}
                  updateScreenBrightness={this.updateScreenBrightness}
                  updateAvalable={this.state.updateAvailable}
                  updateProgress={this.state.updateProgress}
                  handleCheckForUpdate={this.handleCheckForUpdate}
                  handleUpgrade={this.handleAptUpgrade}
                  setPin={this.setLockPin}
                  clearPin={this.clearLockPin}/>
      default:
        return <Favorites socket={this.socket}/>
    }
  }

  render() {
    return (
      <div style={{overflow: "hidden", width: "800px", height: "480px"}} onPointerDown={this.mouseDown}>
        <Menu page={this.state.page} changePage={this.changePage} />
        <DrinkProgress progress={this.state.pour_progress} open={this.state.pour_active} hide={this.hideProgress} cancelPour={this.cancelPour}/>
        <ManualPourProgress progress={this.state.manual_pour_progress} open={this.state.manual_pour_active} hide={this.hideManualPourProgress} cancelPour={this.cancelPour} skipPour={this.skipPour} name={this.state.manual_pour_name}/>
        <UpgradeProgress progress={this.state.upgradeProgress} />
        <ErrorScreen title={this.state.errorTitle} text={this.state.errorText} hide={this.clearError} open={this.state.errorText !== ""}/>
        <LockScreen open={this.state.locked && !this.state.idle} unlock={this.handleUnlock} pin={this.state.lockPin}/>
        <Screensaver idle={this.state.idle}/>
        {this.getPage(this.state.page)}
      </div>
    );
  }
}


export default Bartender;
