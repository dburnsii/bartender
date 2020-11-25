import React from 'react';
import { Box } from '@material-ui/core';
import ValveController from './valveController';

class ValvePage extends React.Component {
  constructor(props){
    super(props);
    this.colors = [0xff0000, 0x00ff00, 0x0000ff, 0xffffff, 0xffff00, 0xff00ff, 0x00ffff, 0xffaaff, 0xaaff00, 0x0033ff];
  }

  shouldComponentUpdate(nextProps, nextState) {
    if(this.props.page !== nextProps.page){
      return true
    }
    else if(this.props.ingredients !== nextProps.ingredients){
      return true
    }
    return false
  }

  getValves(page){
    const min = (page * this.props.bottlesPerPage);
    const max = min + this.props.bottlesPerPage;
    console.log("Displaying valve " + min + "-" + max);
    var output = []
    for(var i = min; i < max; i++){
      console.log(this.colors[i].toString(16).padStart(6, "0"));
      output.push(< ValveController key={i} pin={i} color={"#" + this.colors[i].toString(16).padStart(6, "0")} socket={this.props.socket} ingredients={this.props.ingredients}/>)
    }
    return output
  }

  componentDidMount() {
    this.props.socket.emit("highlight_bottles", {"pins": [0,1,2,3,4,5,6,7,8,9], "colors": this.colors})
  }

  componentWillUnmount(){}

  render() {
    const styles = {};
    return (
      < Box >
        {this.getValves(this.props.page)}
      </Box>
    );
  }
}

export default ValvePage
