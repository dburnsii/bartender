import React from 'react';
import { Button, Box, Typography, Grid, CircularProgress, Switch } from '@mui/material';
import RefreshIcon from '@mui/icons-material/Refresh';
import LockScreen from './components/lockScreen';
import WifiSetup from './components/wifiSetup';
import DisplaySetup from './components/displaySetup';

import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';

class SettingsPage extends React.Component {

  constructor(props){
    super(props);
    this.lockPinScreen = this.lockPinScreen.bind(this);
    this.clearPin = this.clearPin.bind(this);
    this.setPin = this.setPin.bind(this);
    this.cancelPin = this.cancelPin.bind(this);
    this.handleLockPinToggle = this.handleLockPinToggle.bind(this);
    this.hideWifi = this.hideWifi.bind(this);
    this.showWifi = this.showWifi.bind(this);
    this.hideDisplay = this.hideDisplay.bind(this);
    this.showDisplay = this.showDisplay.bind(this);
    this.wifiScanInterval = null;
    this.state = {
      settingPin: false,
      wifiMenu: false,
      displayMenu: false,
      currentSSID: "",
      availableNetworks: [],
      knownNetworks: []
    };
  }

  handleLockPinToggle(){
    this.setState({settingPin: true});
  }

  clearPin(){
    this.setState({settingPin: false});
    this.props.clearPin();
  }

  setPin(pin){
    this.setState({settingPin: false});
    this.props.setPin(pin);
  }

  cancelPin(){
    this.setState({settingPin: false});
  }

  hideWifi(){
    this.setState({wifiMenu: false});
  }

  showWifi(){
    this.setState({wifiMenu: true});
  }

  hideDisplay(){
    this.setState({displayMenu: false});
  }

  showDisplay(){
    this.setState({displayMenu: true});
  }


  lockPinScreen(pin, active){
    if(active){
      if(this.props.lockPin){
        // Disable the pin
        return (<LockScreen
                  open={true}
                  purpose="disable"
                  pin={pin}
                  cancel={this.cancelPin}
                  clearPin={this.clearPin} />)
      } else {
        // Enable the pin
        return (<LockScreen
                  open={true}
                  purpose="enable"
                  pin={pin}
                  cancel={this.cancelPin}
                  setPin={this.setPin}/>)
      }
    }
  }

  updateButton(updateAvailable) {
    const styles = {
      upgradeButton : {
      },
      upToDateText : {
        display: "inline-block"
      },
      checkForUpdateButton : {
        width: "20px",
        height: "20px",
        display: "inline-block"
      },
    };
    if(updateAvailable == null) {
      return <CircularProgress size={25}/>
    } else if (updateAvailable === true) {
      return <Button
                style={styles.upgradeButton}
                variant="contained"
                onClick={this.props.handleUpgrade}
                color="success">
                  Upgrade
              </Button>
    } else {
      return <>
              <Typography style={styles.upToDateText}>Up to Date</Typography>
              <Button onClick={this.props.handleCheckForUpdate}><RefreshIcon/></Button>
             </>
    }

  }

  componentDidMount() {
    this.props.socket.on('wifi_scan_results', (data) => {
      var networks = data['networks'];
      networks.sort((a, b) => a.signal < b.signal)
      this.setState({availableNetworks: networks})
      console.log("Got available wifi networks")
      console.log(data['networks'])
    });

    this.props.socket.on('wifi_known_network_results', (data) => {
      var networks = data['networks'];
      this.setState({knownNetworks: networks})
      console.log("Got known wifi networks")
      console.log(data['networks'])
    });

    this.props.socket.on('wifi_current_ssid', (data) => {
      this.setState({currentSSID: data['ssid']})
      console.log("Got current SSID")
      console.log(data['ssid'])
    });

    if(this.props.updateAvalable == null){
      this.props.socket.emit('apt_update', '');
    }
    this.props.socket.emit('wifi_get_networks', '');
    this.props.socket.emit('wifi_scan', '');
    this.wifiScanInterval = setInterval(() => {
      this.props.socket.emit('wifi_scan', '');
    }, 10000);
  }

  componentWillUnmount(){
    if(this.wifiScanInterval){
      clearInterval(this.wifiScanInterval);
      this.wifiScanInterval = null;
    }
  }

  render() {
    const styles = {
      box : {
        margin: "15px 15px 15px 110px"
      },
      refreshButton : {
        width: "30px"
      },
      resetPinButton : {
      },
      settingsSlider : {
        width: "94%"
      }
    };
    return (
        < Box position="relative" display="inline-block" style={styles.box}>
          <Typography variant="h4">Settings</Typography>
          <br/>
          <Grid container rowSpacing={4} columnSpacing={3}>
            <Grid item xs={4} onClick={this.showDisplay}>
              <Typography variant="h5">Display</Typography>
            </Grid>
            <Grid item xs={6} onClick={this.showDisplay}>
            </Grid>
            <Grid item xs={2} onClick={this.showDisplay}>
              <ArrowForwardIosIcon/>
            </Grid>
            <DisplaySetup
              open={this.state.displayMenu}
              hide={this.hideDisplay}
              updateScreenTimeout={this.props.updateScreenTimeout}
              updateScreenBrightness={this.props.updateScreenBrightness}
              blankTime={this.props.blankTime}
              screenBrightness={this.props.screenBrightness}
              socket={this.props.socket} />

            <Grid item xs={4}>
              <Typography variant="h5">Pin Lock</Typography>
            </Grid>
            <Grid item xs={8}>
              <Switch
                checked={this.props.lockPin && this.props.lockPin.length === 4}
                onChange={this.handleLockPinToggle} />
            </Grid>
            {this.lockPinScreen(this.props.lockPin, this.state.settingPin)}

            <Grid item xs={4}>
              <Typography variant="h5">Updates</Typography>
            </Grid>
            <Grid item xs={8}>
              {this.updateButton(this.props.updateAvalable)}
            </Grid>

            <Grid item xs={4} onClick={this.showWifi}>
              <Typography variant="h5">WiFi</Typography>
            </Grid>
            <Grid item xs={6} onClick={this.showWifi}>
              <Typography variant="h5" align="right">
                {this.state.currentSSID}
              </Typography>
            </Grid>
            <Grid item xs={2} onClick={this.showWifi}>
              <ArrowForwardIosIcon/>
            </Grid>
            <WifiSetup
              currentSSID={this.state.currentSSID}
              availableNetworks={this.state.availableNetworks}
              knownNetworks={this.state.knownNetworks}
              open={this.state.wifiMenu}
              hide={this.hideWifi}
              socket={this.props.socket} />

            <Grid item xs={4}>
            </Grid>
            <Grid item xs={4}>
              <Button style={styles.refresh} variant="contained" onClick={() => window.location.reload(false)}>Refresh</Button>
            </Grid>
            <Grid item xs={4}>
            </Grid>
          </Grid>
        </Box>
    );
  }
}

export default SettingsPage
