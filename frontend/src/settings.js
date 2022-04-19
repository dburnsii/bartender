import React from 'react';
import { Button, Box, Typography, Grid, Slider, CircularProgress } from '@mui/material';
import RefreshIcon from '@mui/icons-material/Refresh';

class SettingsPage extends React.Component {

  constructor(props){
    super(props);
    this.handleScreenTimeout = this.handleScreenTimeout.bind(this);
    this.handleScreenBrightness = this.handleScreenBrightness.bind(this);
    this.state = {
      brightness: 50
    };
  }

  handleScreenTimeout(event, value){this.props.updateScreenTimeout(value * 1000)}
  handleScreenBrightness(event, value){this.props.updateScreenBrightness(value)}
  handleTogglePinLock(){}
  handleResetPin(){}

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
    if(this.props.updateAvalable == null){
      this.props.socket.emit('apt_update', '');
    }
  }

  componentWillUnmount(){

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
            <Grid item xs={4}>
              <Typography variant="h5">Screen timeout</Typography>
            </Grid>
            <Grid item xs={8}>
              <Slider
                min={5}
                max={300}
                style={styles.settingsSlider}
                valueLabelFormat={(x) => x + "s"}
                value={this.props.blankTime/1000}
                valueLabelDisplay="on"
                onChange={this.handleScreenTimeout} />
            </Grid>

            <Grid item xs={4}>
              <Typography variant="h5">Screen Brightness</Typography>
            </Grid>
            <Grid item xs={8}>
              <Slider
                min={1}
                max={100}
                style={styles.settingsSlider}
                valueLabelFormat={(x) => x + "%"}
                value={this.props.screenBrightness}
                valueLabelDisplay="on"
                onChange={this.handleScreenBrightness} />
            </Grid>

            <Grid item xs={8}>
              <Typography variant="h5">Updates</Typography>
            </Grid>
            <Grid item xs={4}>
              {this.updateButton(this.props.updateAvalable)}
            </Grid>

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
