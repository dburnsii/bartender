import React from 'react';
import { FormControl, InputLabel, InputAdornment, Input, IconButton, Button, Card, Typography, Modal, List, ListItem, ListItemIcon, ListItemText, Grid } from '@mui/material';
import SignalWifi1BarIcon from '@mui/icons-material/SignalWifi1Bar';
import SignalWifi1BarLockIcon from '@mui/icons-material/SignalWifi1BarLock';
import SignalWifi2BarIcon from '@mui/icons-material/SignalWifi2Bar';
import SignalWifi2BarLockIcon from '@mui/icons-material/SignalWifi2BarLock';
import SignalWifi3BarIcon from '@mui/icons-material/SignalWifi3Bar';
import SignalWifi3BarLockIcon from '@mui/icons-material/SignalWifi3BarLock';
import SignalWifi4BarIcon from '@mui/icons-material/SignalWifi4Bar';
import SignalWifi4BarLockIcon from '@mui/icons-material/SignalWifi4BarLock';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import VisibilityIcon from '@mui/icons-material/Visibility';
import VisibilityOffIcon from '@mui/icons-material/VisibilityOff';
import BlockIcon from '@mui/icons-material/Block';
import LeakAddIcon from '@mui/icons-material/LeakAdd';
import Keyboard from 'react-simple-keyboard';
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
      screen: props.currentSSID ? "info" : "list",
      selectedNetwork: props.currentSSID,
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

  wifiIcon(signal, auth){
    var strength = "1";
    if(signal >= 80){
      strength = "4";
    } else if(signal >= 60) {
      strength = "3";
    } else if(signal >= 40 ) {
      strength = "2";
    } else {
      strength = "1";
    }

    var secured = (auth > 0) ? "secure" : "";
    return React.createElement(wifiIcons[`signal${strength}${secured}`], {

    });
  }

  currentNetwork(){
    if(this.props.currentSSID !== ""){
      var currentNetwork =
          this.props.availableNetworks.find(x => x.name === this.props.currentSSID);
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
    if(this.props.knownNetworks.find(x => x === ssid)){
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

  authString(auth){
    /*
    NM_802_11_AP_SEC_NONE = 0x00000000 the access point has no special security requirements
    NM_802_11_AP_SEC_PAIR_WEP40 = 0x00000001 40/64-bit WEP is supported for pairwise/unicast encryption
    NM_802_11_AP_SEC_PAIR_WEP104 = 0x00000002 104/128-bit WEP is supported for pairwise/unicast encryption
    NM_802_11_AP_SEC_PAIR_TKIP = 0x00000004 TKIP is supported for pairwise/unicast encryption
    NM_802_11_AP_SEC_PAIR_CCMP = 0x00000008 AES/CCMP is supported for pairwise/unicast encryption
    NM_802_11_AP_SEC_GROUP_WEP40 = 0x00000010 40/64-bit WEP is supported for group/broadcast encryption
    NM_802_11_AP_SEC_GROUP_WEP104 = 0x00000020 104/128-bit WEP is supported for group/broadcast encryption
    NM_802_11_AP_SEC_GROUP_TKIP = 0x00000040 TKIP is supported for group/broadcast encryption
    NM_802_11_AP_SEC_GROUP_CCMP = 0x00000080 AES/CCMP is supported for group/broadcast encryption
    NM_802_11_AP_SEC_KEY_MGMT_PSK = 0x00000100 WPA/RSN Pre-Shared Key encryption is supported
    NM_802_11_AP_SEC_KEY_MGMT_802_1X = 0x00000200 802.1x authentication and key management is supported
    */
    return "WPA"
  }

  wifiSetupScreen(){
    const styles = {
      wifiActionButton : {
        height: '100%',
        paddingLeft: '16px',
        paddingRight: '16px'
      }
    };

    if(this.state.screen === "list"){
      return (
        <div>
          <Typography variant="h4">
            WiFi Networks
          </Typography>
          <div style={{overflowY: "scroll"}}>
          <List>
            {this.currentNetwork()}
            {this.props.availableNetworks.map((network) => {
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
    } else if (this.state.screen === "info") {
      const my_network = this.props.availableNetworks.find(x => x.name === this.state.selectedNetwork);
      return(
        <div>
          <ArrowBackIcon onClick={this.deselectNetwork} fontSize="large"/>
          <Grid container spacing={2} style={{paddingLeft: "32px", paddingTop: "24px"}}>
            <Grid item xs={3}>
              <Typography variant="h5">
                SSID:
              </Typography>
            </Grid>
            <Grid item xs={9}>
              <Typography variant="h5">
                {my_network.name}
              </Typography>
            </Grid>
            <Grid item xs={3}>
              <Typography variant="h5">
                Strength:
              </Typography>
            </Grid>
            <Grid item xs={9}>
              <Typography variant="h5">
                {my_network.signal}%
              </Typography>
            </Grid>
            <Grid item xs={3}>
              <Typography variant="h5">
                Security:
              </Typography>
            </Grid>
            <Grid item xs={9}>
              <Typography variant="h5">
                {this.authString(my_network.auth)}
              </Typography>
            </Grid>
          </Grid>
          <Grid container item xs={12} spacing={2} justifyContent="center" style={{position: 'absolute', bottom: '16px', left: '16px', right: '16px', height: '20%'}}>
            {this.props.knownNetworks.includes(this.state.selectedNetwork) &&
              this.props.currentSSID !== this.state.selectedNetwork
              ? <Grid item xs={6}>
                  <Button
                    variant="contained"
                    color="error"
                    fullWidth={true}
                    style={styles['wifiActionButton']}
                    onClick={(e) => this.forgetNetwork(this.state.selectedNetwork, e)}>
                    Forget</Button>
                  </Grid> : null
             }
             <Grid item xs={6}>
              {this.props.currentSSID !== this.state.selectedNetwork
                ? <Button
                    variant="contained"
                    color="success"
                    fullWidth={true}
                    style={{height: '100%'}}
                    onClick={(e) => this.connectNetwork(this.state.selectedNetwork, e)}>
                    <LeakAddIcon/>
                    Connect
                    </Button>
                : <Button
                      variant="contained"
                      color="error"
                      fullWidth={true}
                      style={{height: '100%'}}
                      onClick={this.disconnectNetwork}>
                      <BlockIcon/>Disconnect
                  </Button>
              }
            </Grid>
          </Grid>
        </div>
      )
    } else if (this.state.screen === "auth") {
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
    } else if (this.state.screen === "loading") {
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
          transition: "height 0.5s",
          position: "relative"
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
    return (
      <Modal open={this.props.open} onClose={this.props.hide}>
        <Card style={this.cardStyle(this.state.screen === "auth")}>
          {this.wifiSetupScreen()}
        </Card>
      </Modal>
    );
  }
}

export default WifiSetup
