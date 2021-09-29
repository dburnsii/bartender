import React from 'react';
import { Button, Divider , Box, Typography, Grid, Slider, Switch } from '@mui/material';
import throttle from 'lodash.throttle';

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

  componentDidMount() {

  }

  componentWillUnmount(){

  }

  render() {
    const styles = {
      box : {
        margin: "10px 10px 10px 100px"
      },
      refreshButton : {
        width: "30px"
      },
      resetPinButton : {
      },
    };
    return (
        < Box position="relative" display="inline-block" style={styles.box}>
          <Typography variant="h4">Settings</Typography>
          <br/>
          <Grid container spacing={2}>
            <Grid item xs={4}>
              <Typography>Screen timeout: </Typography>
            </Grid>
            <Grid item xs={8}>
              <Slider min={5} max={300} value={this.props.blankTime/1000} onChange={this.handleScreenTimeout} />
            </Grid>
            <Grid item xs={4}>
              <Typography>Screen Brightness</Typography>
            </Grid>
            <Grid item xs={8}>
              <Slider min={1} max={100} value={this.props.screenBrightness} onChange={this.handleScreenBrightness} />
            </Grid>
            <Grid item xs={4}>
              <Typography>Pin Lock</Typography>
            </Grid>
            <Grid item xs={4}>
                <Switch onChange={this.handleTogglePinLock} />
            </Grid>
            <Grid item xs={4}>
              <Button style={styles.resetPinButton} variant="contained" onClick={this.handleResetPin}>Reset Pin</Button>
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
