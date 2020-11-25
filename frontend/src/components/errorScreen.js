import React from 'react';
import { Card, LinearProgress, Box, Typography, Modal} from '@material-ui/core';
import PlayCircleFilledIcon from '@material-ui/icons/PlayCircleFilled';
import CloseIcon from '@material-ui/icons/Close';
import WarningIcon from '@material-ui/icons/Warning';
//import Modal from '@material-ui/core/Modal';
import { titleCase } from "title-case";
import { green } from '@material-ui/core/colors';

class ErrorScreen extends React.Component {
  constructor(props){
    super(props);
    this.state = {
    }
  }

  componentDidMount(){
  }

  componentWillUnmount(){
  }

  render() {
    const styles = {
      card : {
        width: "80%",
        height: "70%",
        margin: "10%",
        position: "absolute",
        paddingLeft: "12px",
        paddingRight: "12px"
      },
      icon : {
        width: "100%",
        textAlign: "center",
        fontSize: "48px",
        marginTop: "12px"
      },
      close : {
        position: "absolute",
        right: "0px"
      },
      title: {
        textAlign: "center",
        fontSize: "24px"
      },
      text : {
        textAlign: "center",
        fontSize: "16px"
      }
    };
    return (
      <Modal open={this.props.open} onClose={this.props.hide}>
        <Card style={styles.card}>
          <CloseIcon style={styles.close} onClick={this.props.hide}/>
          <WarningIcon style={styles.icon} color="secondary"/>
          <Typography style={styles.title}>
            {this.props.title}
          </Typography>
          <Typography style={styles.text}>
            {this.props.text}
          </Typography>
        </Card>
      </Modal>
    );
  }
}

export default ErrorScreen
