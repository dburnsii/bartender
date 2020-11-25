import React from 'react';
import { Button, Divider , Box, Typography, Grid } from '@material-ui/core';
import ValvePage from './components/valvePage';
import Scale from './components/scale';
import ChevronRightIcon from '@material-ui/icons/ChevronRight';
import ChevronLeftIcon from '@material-ui/icons/ChevronLeft';
import LockClosedIcon from '@material-ui/icons/Lock';
import LockOpenIcon from '@material-ui/icons/LockOpen';

class ManualModePage extends React.Component {

  constructor(props){
    super(props);
    this.startPour = this.startPour.bind(this);
    this.stopPour = this.stopPour.bind(this);
    this.nextPage = this.nextPage.bind(this);
    this.prevPage = this.prevPage.bind(this);
    this.manualOverride = this.manualOverride.bind(this);
    this.tare = this.tare.bind(this);
    this.bottlesPerPage = 10;
    this.bottlesTotal = 10;
    this.state = {
      page : 0,
      ingredients: [],
      manualOverride: false
    };
  }

  startPour(e){
    console.log("Starting pour");
    var pin = e.target.parentElement.getAttribute('valve');
    this.props.socket.emit('activate_valve', {'pin': pin});
  }

  stopPour(e){
    console.log("Stopping pour");
    var pin = e.target.parentElement.getAttribute('valve');
    this.props.socket.emit('deactivate_valve', {'pin': pin})
  }

  prevPage(){
    if(this.state.page > 0){
      this.setState({page: this.state.page - 1});
    }
  }

  nextPage(){
    if((this.state.page + 1) * this.bottlesPerPage < this.bottlesTotal){
      this.setState({page: this.state.page + 1});
    }
  }

  componentDidMount() {
    fetch("http://" + window.location.hostname + ":5000/ingredients?pourable=1")
      .then(response => response.json())
      .then((data) => {
        console.log(data);
        this.setState({
          ingredients: data
        })
      });
  }

  componentWillUnmount(){
    clearInterval(this.timer);
  }

  tare(){
	  console.log("Zeroing scale");
	  this.props.socket.emit('tare_scale', '');
  }

  manualOverride(){
    this.props.socket.emit('manual_override', {"status": !this.state.manualOverride});
    this.setState({"manualOverride": !this.state.manualOverride});
  }

  manualOverrideButton(status){
    if(status){
      return(<LockClosedIcon/>)
    } else {
      return(<LockOpenIcon/>)
    }
  }

  render() {
    const styles = {
      box : {
        margin: "10px 10px 10px 92px"
      },
      header : {

      },
      prevButton : {

      },
      prevButtonIcon : {
        fontSize: 72,
        textAlign: "left",
        display: "none"
      },
      nextButton : {

      },
      nextButtonIcon : {
        fontSize: 72,
        textAlign: "right",
        display: "none"
      },

    };
    return (
        < Box position="relative" style={styles.box}>
          <Grid container style={styles.header}>
            <Grid item xs={2}>
              <Button
                style={styles.prevButton}
                disabled={this.state.page == 0}
                disableRipple={true}
                onClick={this.prevPage}>
                <ChevronLeftIcon style={styles.prevButtonIcon}/>
              </Button>
            </Grid>
            <Grid item xs={8} onClick={this.tare}>
              < Scale
                socket={this.props.socket}
                weight={this.props.weight}
                metric={this.props.metric}
                presence={this.props.presence} />
            </Grid>
            <Grid item xs={2}>
              <Button onClick={this.manualOverride}>{this.manualOverrideButton(this.state.manualOverride)}</Button>
            </Grid>
          </Grid>
          <ValvePage page={this.state.page} bottlesPerPage={this.bottlesPerPage} socket={this.props.socket} ingredients={this.state.ingredients}/>
        </Box>
    );
  }
}

export default ManualModePage
