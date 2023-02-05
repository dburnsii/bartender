import React from 'react';
import { Card, Modal, Grid, Typography, Button, Slider, Select, MenuItem } from '@mui/material';
import '../App.css'

class HardwareSetup extends React.Component {
  constructor(props){
    super(props);
    this.handleScaleType = this.handleScaleType.bind(this);
    this.handleScaleCalibrationBegin = this.handleScaleCalibrationBegin.bind(this);
    this.handleScaleTare = this.handleScaleTare.bind(this);
    this.handleScaleCalibration = this.handleScaleCalibration.bind(this);
    this.handleScaleChange = this.handleScaleChange.bind(this);
    this.handleValveChange = this.handleValveChange.bind(this);
    this.cardContent = this.cardContent.bind(this);
    this.queryControllers = this.queryControllers.bind(this);
    
    this.state = {
      screen: "menu",
      scaleController: "",
      valveController: ""
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

  handleScaleType(event, value){}
  handleScaleCalibrationBegin(event){this.setState({screen: "tare"})}
  
  handleScaleTare(event){
    this.props.socket.emit('tare_scale', '');
    this.setState({screen: "calibrate"});
  }

  handleScaleCalibration(event){
    this.props.socket.emit('calibrate_scale', {'weight': 100});
    this.setState({screen: "success"});
    this.setTimeout(() => {this.setState({screen: "menu"}, 2000)});
  }

  handleScaleChange(event){
    fetch(this.configURL, 
      { method: 'PUT',
        headers : {
          key: "scale_controller",
          value: event.target.value
        }
      })
    .then((response) => this.queryControllers());
  }

  handleValveChange(event){
    fetch(this.configURL, 
      { method: 'PUT',
        headers : {
          key: "valve_controller",
          value: event.target.value
        }
      })
    .then((response) => this.queryControllers());
  }

  queryControllers(){
    console.log(this.configURL)
    fetch(this.configURL + "/valve_controller")
      .then((response) => response.json())
      .then((json) => this.setState({"valveController": json}));
    fetch(this.configURL + "/scale_controller")
      .then((response) => response.json())
      .then((json) => this.setState({"scaleController": json}));
  }

  componentDidMount(){
    this.configURL = "http://" + window.location.hostname + ":5000/config"
    this.queryControllers();
  }

  componentWillUnmount(){}

  cardContent(screen){
    if (screen === "menu"){
      return (<Card style={this.cardStyle()}>
              <Grid container style={{paddingTop: "16px"}}>
                <Grid item xs={6}>
                  <Typography variant="h6">Scale Type</Typography>
                </Grid>
                <Grid item xs={6}>
                  <Select
                    value={this.state.scaleController}
                    onChange={this.handleScaleChange} >
                    <MenuItem value="nau7802">NAU7802</MenuItem>
                    <MenuItem value="hx711">HX711</MenuItem>
                    <MenuItem value="simulation">Simulator</MenuItem>
                  </Select>
                </Grid>

                <Grid item xs={6}>
                  <Typography variant="h6">Scale Calibration</Typography>
                </Grid>
                <Grid item xs={6}>
                  <Button
                    onClick={this.handleScaleCalibrationBegin}
                    variant="contained"
                    style={{marginBottom: "16px", marginTop: "16px"}}
                    >
                    Calibrate</Button>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="h6">Valve Type</Typography>
                </Grid>
                <Grid item xs={6}>
                  <Select
                    value={this.state.valveController}
                    onChange={this.handleValveChange}
                    autoWidth={true} >
                    <MenuItem value="pcal6416a">PCAL6416A</MenuItem>
                    <MenuItem value="mcp23017">MCP23017</MenuItem>
                    <MenuItem value="gpio">GPIO</MenuItem>
                    <MenuItem value="simulation">Simulator</MenuItem>
                  </Select>
                </Grid>
              </Grid>
            </Card>);
    } else if (screen === "tare"){
      return (<Card style={this.cardStyle()}>
      <Grid container style={{paddingTop: "16px"}}>
        <Grid item xs={4}>
          <Typography variant="h6">Tare Scale</Typography>
          <Typography>Please clear the scale, and press the button below</Typography>
        </Grid>
        <Grid item xs={8}>
        </Grid>

        <Grid item xs={4}>
          <Button variant="h6" onClick={this.handleScaleTare}>Tare</Button>
        </Grid>
      </Grid>
    </Card>);
    } else if (screen === "calibrate"){
      return (<Card style={this.cardStyle()}>
      <Grid container style={{paddingTop: "16px"}}>
        <Grid item xs={4}>
          <Typography variant="h6">Calibrate Scale</Typography>
          <Typography>Please place an object with a known weight on the scale, and enter the weight below</Typography>
        </Grid>
        <Grid item xs={8}>
          <Slider></Slider>
        </Grid>

        <Grid item xs={4}>
          <Button variant="h6" onClick={this.handleScaleCalibration}>Calibrate</Button>
        </Grid>
      </Grid>
    </Card>);
    } else if (screen === "success"){
      return (<Card style={this.cardStyle()}>
      <Grid container style={{paddingTop: "16px"}}>
        <Grid item xs={4}>
          <Typography variant="h6">Good job bud.</Typography>
        </Grid>
      </Grid>
    </Card>);
    }
  }

  render() {
    //const styles = {};

    return (
      <Modal open={this.props.open} onClose={this.props.hide}>
        {this.cardContent(this.state.screen)}
      </Modal>
    );
  }
}

export default HardwareSetup
