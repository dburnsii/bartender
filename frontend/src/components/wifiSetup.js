import React from 'react';
import { Button, Card, LinearProgress, Box, Typography, Modal, List, ListItem, ListItemIcon, ListItemText } from '@mui/material';
import SignalWifi1BarIcon from '@mui/icons-material/SignalWifi1Bar';
import SignalWifi1BarLockIcon from '@mui/icons-material/SignalWifi1BarLock';
import SignalWifi2BarIcon from '@mui/icons-material/SignalWifi2Bar';
import SignalWifi2BarLockIcon from '@mui/icons-material/SignalWifi2BarLock';
import SignalWifi3BarIcon from '@mui/icons-material/SignalWifi3Bar';
import SignalWifi3BarLockIcon from '@mui/icons-material/SignalWifi3BarLock';
import SignalWifi4BarIcon from '@mui/icons-material/SignalWifi4Bar';
import SignalWifi4BarLockIcon from '@mui/icons-material/SignalWifi4BarLock';
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
    this.state = {
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

    var secured = (auth && auth.length) ? "secure" : "";
    return React.createElement(wifiIcons[`signal${strength}${secured}`], {

    });
  }

  currentNetwork(){
    if(this.state.currentSSID != ""){
      return(<ListItem>
              <ListItemText>
                {this.props.currentSSID}
              </ListItemText>
              <ListItemIcon>
                {this.wifiIcon(4, ['wep'])}
              </ListItemIcon>
            </ListItem>)
    }
  }

  componentDidMount(){
    console.log(this.props.networks)
  }

  componentWillUnmount(){
  }

  render() {
    const styles = {
      card : {
        width: "75%",
        height: "60%",
        margin: "15%"
      }
    };
    return (
      <Modal open={this.props.open} onClose={this.props.hide}>
        <Card style={styles.card}>
          <Typography>
            WiFi Networks
          </Typography>
          <List>
          {this.currentNetwork()}
          {this.props.networks.map((network) => {
            //logic goes here
            if(network.name == ""){
              return null
            } else if(network.name == this.props.currentSSID){
              return null
            }
            return (
              <ListItem>
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
        </Card>
      </Modal>
    );
  }
}

export default WifiSetup
