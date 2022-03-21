import React from 'react';
import { Typography, Card, Modal } from '@mui/material';
import BokehAnimation from './bokeh';

class Screensaver extends React.Component {
  componentDidMount(){
  }

  componentWillUnmount(){
  }

  render() {
    const styles = {
      card : {
        width: "100%",
        height: "100%",
        margin: "0%",
        backgroundColor: "#222",
        position: "fixed"
      },
      text : {
        textAlign: "center",
        fontSize: "85px",
        color: "white",
        paddingTop: "160px",
        fontFamily: "Lobster",
        zIndex: "100",
        position: "relative"
      }
    };
    return (
      <Modal open={this.props.idle}>
        <Card style={styles.card}>
          <Typography style={styles.text}>The Bartender</Typography>
          <BokehAnimation/>
        </Card>
      </Modal>
    );
  }
}

export default Screensaver
