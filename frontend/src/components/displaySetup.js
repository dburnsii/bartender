import React from 'react';
import { Card, Modal, Grid, Slider, Typography } from '@mui/material';
import '../App.css'

class DisplaySetup extends React.Component {
  constructor(props){
    super(props);
    this.handleScreenTimeout = this.handleScreenTimeout.bind(this);
    this.handleScreenBrightness = this.handleScreenBrightness.bind(this);
    this.state = {
      brightness: 50
    }
  }

  cardStyle() {
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

  handleScreenTimeout(event, value){this.props.updateScreenTimeout(value * 1000)}
  handleScreenBrightness(event, value){this.props.updateScreenBrightness(value)}

  componentDidMount(){}

  componentWillUnmount(){}

  render() {
    const styles = {
      settingsSlider : {
        width: "94%"
      }
    };

    return (
      <Modal open={this.props.open} onClose={this.props.hide}>
        <Card style={this.cardStyle()}>
          <Grid container style={{paddingTop: "16px"}}>
            <Grid item xs={4}>
              <Typography variant="h6">Screen timeout</Typography>
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
              <Typography variant="h6">Screen Brightness</Typography>
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
          </Grid>
        </Card>
      </Modal>
    );
  }
}

export default DisplaySetup
