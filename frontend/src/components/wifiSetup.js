import React from 'react';
import { Button, Card, LinearProgress, Box, Typography, Modal, List, ListItem, ListItemIcon, ListItemText, TextField } from '@mui/material';
import SignalWifi1BarIcon from '@mui/icons-material/SignalWifi1Bar';
import SignalWifi1BarLockIcon from '@mui/icons-material/SignalWifi1BarLock';
import SignalWifi2BarIcon from '@mui/icons-material/SignalWifi2Bar';
import SignalWifi2BarLockIcon from '@mui/icons-material/SignalWifi2BarLock';
import SignalWifi3BarIcon from '@mui/icons-material/SignalWifi3Bar';
import SignalWifi3BarLockIcon from '@mui/icons-material/SignalWifi3BarLock';
import SignalWifi4BarIcon from '@mui/icons-material/SignalWifi4Bar';
import SignalWifi4BarLockIcon from '@mui/icons-material/SignalWifi4BarLock';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import { titleCase } from "title-case";

const wifiIcons = {
  signal1: SignalWifi1BarIcon,
  signal1secure: SignalWifi1BarLockIcon,
  signal2: SignalWifi2BarIcon,
  signal2secure: SignalWifi2BarLockIcon,
  signal3: SignalWifi3BarIcon,
  signal3secure: SignalWifi3BarLockIcon,
  signal4: SignalWifi4BarIcon,
  signal4secure: SignalWifi4BarLockIcon,
}

class WifiSetup extends React.Component {
  constructor(props){
    super(props);
    this.wifiIcon = this.wifiIcon.bind(this);
    this.wifiSetupScreen = this.wifiSetupScreen.bind(this);
    this.selectNetwork = this.selectNetwork.bind(this);
    this.deselectNetwork = this.deselectNetwork.bind(this);
    this.authNetwork = this.authNetwork.bind(this);
    this.cancelAuthNetwork = this.cancelAuthNetwork.bind(this);
    this.forgetNetwork = this.forgetNetwork.bind(this);
    this.connectNetwork = this.connectNetwork.bind(this);
    this.disconnectNetwork = this.disconnectNetwork.bind(this);
    this.state = {
      screen: "list",
      selectedNetwork: ""
    }
  }

  /*
  -30 dBm: This is the maximum signal strength.
  -50 dBm: This is considered an excellent signal strength. - level 4
  -60 dBm: This is a good signal strength. - level 3
  -67 dBm: This is a reliable signal strength.
  -70 dBm: This is not a strong signal strength. - level 2
  -80 dBm: This is an unreliable signal strength. - level 1
  */
  wifiIcon(signal, auth){
    var strength = "1";
    if(signal <= -80){
      strength = "1";
    } else if(signal <= -70) {
      strength = "2";
    } else if(signal <= -60 ) {
      strength = "3";
    } else {
      strength = "4";
    }

    var secured = (auth && auth.length && auth[0].length) ? "secure" : "";
    return React.createElement(wifiIcons[`signal${strength}${secured}`], {

    });
  }

  currentNetwork(){
    if(this.props.currentSSID != ""){
      var currentNetwork =
          this.props.availableNetworks.find(x => x.name == this.props.currentSSID);
      return(
        <ListItem
          divider={true}
          onClick={(e) => this.selectNetwork(this.props.currentSSID, e)}>
              <ListItemText>
                {this.props.currentSSID}
              </ListItemText>
              <ListItemIcon>
                {this.wifiIcon(currentNetwork.signal, currentNetwork.auth)}
              </ListItemIcon>
            </ListItem>
            )
    }
  }

  selectNetwork(ssid, e){
    this.setState({screen: "info", selectedNetwork: ssid});
  }

  deselectNetwork(){
    this.setState({screen: "list"})
  }

  authNetwork(ssid){
    this.setState({screen: "auth"})
  }

  cancelAuthNetwork(){
    this.setState({screen: "info"})
  }

  forgetNetwork(ssid){
    this.props.socket.emit('wifi_forget', {name: ssid})
    this.setState({screen: "list"})
  }

  connectNetwork(ssid, e){
    if(this.props.knownNetworks.find(x => x == ssid)){
      this.props.socket.emit('wifi_connect', {name: ssid})
      this.setState({screen: 'loading'})
    } else {
      this.setState({screen: 'auth'})
    }
  }

  disconnectNetwork(){
    this.props.socket.emit('wifi_disconnect', '');
  }

  wifiSetupScreen(){
    if(this.state.screen == "list"){
      return (
        <div>
          <Typography variant="h4">
            WiFi Networks
          </Typography>
          <div style={{overflowY: "scroll"}}>
          <List>
            {this.currentNetwork()}
            {this.props.availableNetworks.map((network) => {
              //logic goes here
              if(network.name === ""){
                return null
              } else if(network.name === this.props.currentSSID){
                return null
              }
              return (
                <ListItem onClick={(e) => this.selectNetwork(network.name, e)}>
                  <ListItemText>
                    {network.name}
                  </ListItemText>
                  <ListItemIcon>
                    {this.wifiIcon(network.signal, network.auth)}
                  </ListItemIcon>
                </ListItem>
              )
            })}
          </List>
          </div>
        </div>
      )
    } else if (this.state.screen == "info") {
      return(
        <div>
          <ArrowBackIcon onClick={this.deselectNetwork} fontSize="large"/>
          <Typography>
            {this.state.selectedNetwork}
          </Typography>
          {this.props.knownNetworks.includes(this.state.selectedNetwork) &&
            this.props.currentSSID !== this.state.selectedNetwork
            ? <Button
                variant="contained"
                color="error"
                onClick={(e) => this.forgetNetwork(this.state.selectedNetwork, e)}>
                Forget</Button> : null
           }
          {this.props.currentSSID !== this.state.selectedNetwork
            ? <Button
                variant="contained"
                color="success"
                onClick={(e) => this.connectNetwork(this.state.selectedNetwork, e)}>
                Connect
                </Button>
            : <Button
                  variant="contained"
                  color="error"
                  onClick={this.disconnectNetwork}>Disconnect</Button>
          }
        </div>
      )
    } else if (this.state.screen == "auth") {
      return(
        <div>
          <TextField></TextField>
          <Button onClick={this.cancelAuthNetwork}>Cancel</Button>
        </div>
        )
    } else if (this.state.screen == "loading") {
      return(<Button onClick={this.cancelAuthNetwork}>CANCEL LOADING</Button>)
    }
  }

  cardStyle(auth) {
    if(auth){
      return(
        {
          width: "80%",
          height: "40%",
          marginLeft: "10%",
          marginRight: "10%",
          marginTop: "5%",
          padding: "3%",
          transition: "height 1s"
        }
      )
    } else {
      return(
        {
          width: "80%",
          height: "80%",
          marginLeft: "10%",
          marginRight: "10%",
          marginTop: "5%",
          padding: "3%",
          transition: "height 0.5s"
        }
      )
    }
  }

  componentDidMount(){
    console.log(this.props.availableNetworks)
  }

  componentWillUnmount(){
  }

  render() {
    const styles = {

    };
    return (
      <Modal open={this.props.open} onClose={this.props.hide}>
        <Card style={this.cardStyle(this.state.screen == "auth")}>
          {this.wifiSetupScreen()}
        </Card>
      </Modal>
    );
  }
}

export default WifiSetup
