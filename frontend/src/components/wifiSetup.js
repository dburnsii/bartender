import React from 'react';
import { FormControl, InputLabel, InputAdornment, Input, IconButton, Button, Card, LinearProgress, Box, Typography, Modal, List, ListItem, ListItemIcon, ListItemText, TextField } from '@mui/material';
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
import VisibilityIcon from '@mui/icons-material/Visibility';
import VisibilityOffIcon from '@mui/icons-material/VisibilityOff';
import { titleCase } from "title-case";
import Keyboard, {KeyboardReactInterface} from 'react-simple-keyboard';
import 'react-simple-keyboard/build/css/index.css';
import '../App.css'

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
    this.inputField = React.createRef();
    this.keyboard = React.createRef();
    this.onAuthChange = this.onAuthChange.bind(this);
    this.onAuthKeyPress = this.onAuthKeyPress.bind(this);
    this.toggleHidePassword = this.toggleHidePassword.bind(this);
    this.submitAuth = this.submitAuth.bind(this);
    this.state = {
      screen: "list",
      selectedNetwork: "",
      authInput: "",
      hidePassword: true
    }
  }

  keyboardLayout = {
    'default': [
      '` 1 2 3 4 5 6 7 8 9 0 - =',
      'q w e r t y u i o p [ ] \\',
      'a s d f g h j k l ; \'',
      '{shift} z x c v b n m , . / {shift}',
      '{bksp} {space} {enter}'
    ],
    'shift' : [
      '~ ! @ # $ % ^ & * ( ) _ +',
      'Q W E R T Y U I O P { } |',
      'A S D F G H J K L : "',
      '{shift} Z X C V B N M < > ? {shift}',
      '{bksp} {space} {enter}'
    ]
  }

  keyboardDisplay = {
    '{shift}' : 'shift',
    '{bksp}': "backspace",
    "{enter}": "enter"
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

  submitAuth(){
    this.props.socket.emit('wifi_connect',
                           {name: this.state.selectedNetwork,
                            password: this.state.authInput})
    this.setState({screen: "list", authInput: ""});
  }

  forgetNetwork(ssid){
    this.props.socket.emit('wifi_forget', {name: ssid})
    this.setState({screen: "list"})
  }

  connectNetwork(ssid, e){
    if(this.props.knownNetworks.find(x => x == ssid)){
      this.props.socket.emit('wifi_connect', {name: ssid})
      this.setState({screen: 'list'})
    } else {
      this.setState({screen: 'auth'})
    }
  }

  disconnectNetwork(){
    this.props.socket.emit('wifi_disconnect', '');
  }

  onAuthChange(input){
    this.setState({authInput: input});
  }

  onAuthKeyPress(button){
    if(button === "{shift}"){
      this.keyboardShift = !this.keyboardShift
    } else if(this.keyboardShift){
      this.keyboardShift = false;
    }
    this.keyboard.setOptions({layoutName: this.keyboardShift ? 'shift' : 'default'})

    if(button === "{enter}"){
      console.log("Submit!")
      console.log(this.state.authInput);
      this.submitAuth();
    }
  }

  toggleHidePassword(){
    this.setState({hidePassword: !this.state.hidePassword});
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
          <IconButton style={{display: "inline-block", width: "20%", textAlign: "left"}}
            onClick={this.cancelAuthNetwork}>
            <ArrowBackIcon
              fontSize="large" />
          </IconButton>
          <FormControl
            variant="outlined"
            style={{width: "60%", marginRight: "20%"}}>
            <InputLabel>
              Password
            </InputLabel>
            <Input
              value={this.state.authInput}
              type={this.state.hidePassword ? 'password' : 'text'}
              autoFocus={true}
              endAdornment={
                <InputAdornment position="end">
                  <IconButton
                    onClick={this.toggleHidePassword}>
                    {this.state.hidePassword ?
                      <VisibilityOffIcon/> :
                      <VisibilityIcon/>}
                  </IconButton>
                </InputAdornment>
              }
            />
          </FormControl>
          <Keyboard
            onChange={this.onAuthChange}
            onKeyPress={this.onAuthKeyPress}
            layout={this.keyboardLayout}
            preventMouseDownDefault={true}
            preventMouseUpDefault={true}
            stopMouseDownPropagation={true}
            stopMouseUpPropagation={true}
            useMouseEvents={true}
            keyboardRef={(r) => (this.keyboard = r)}
            theme={"wifiAuthKeyboard"}
            buttonTheme={"wifiAuthButton"} />
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
          height: "20%",
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
