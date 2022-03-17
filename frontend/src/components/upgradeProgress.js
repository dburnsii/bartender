import React from 'react';
import { Button, Card, LinearProgress, Box, Typography, Modal} from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';

class UpgradeProgress extends React.Component {
  constructor(props){
    super(props);
    this.completedTime = 3000;
    this.state = {
      open: false,
      complete: false
    }
  }

  componentDidMount(){
  }

  componentWillUnmount(){
  }

  shouldComponentUpdate(nextProps, nextState){
    // We got a progress update. Open the modal if it's not open already, and
    // check to see if we've hit 100% completion on the update. If so, display
    // the "completed" message and close the modal.
    if(this.props.progress !== nextProps.progress){
      if(!this.state.open){
        this.setState({open: true});
      }
      if(nextProps.progress >= 100){
        this.setState({complete: true})
        setTimeout(() => {
          this.setState({open: false, complete: false})
        }, this.completedTime);
      }
      return true;
    } else if(this.props.open !== nextProps.open){
      return true;
    } else if(this.state.open !== nextState.open){
      return true;
    } else if(this.state.complete !== nextState.complete) {
      return true;
    }
    return false;
  }

  progressContent(progress, complete, styles){
    if(complete){
      return(
        <Card style={styles.card}>
          <Typography style={styles.completeTitle}>
            Complete
          </Typography>
          <CheckCircleIcon
            color='success'
            style={styles.completeIcon}/>
          <Typography style={styles.completeText}>
            Please Reboot Me!
          </Typography>
        </Card>
      )
    } else {
      return(
        <Card style={styles.card}>
          <Typography style={styles.text}>
            Upgrade in Progress
          </Typography>
          <LinearProgress
            variant="determinate"
            color="success"
            value={this.props.progress}
            style={styles.progress}/>
        </Card>
      );
    }
  }

  render() {
    const styles = {
      card : {
        width: "75%",
        height: "60%",
        margin: "15%"
      },
      text : {
        textAlign: "center",
        margin: "5%",
        fontSize: "36px"
      },
      progress : {
        width: "80%",
        height: "20px",
        margin: "10% 10% 8% 10%",
        borderRadius: "10px"
      },
      cancel : {
        align: "center"
      },
      cancelBox : {
        width: "100%",
        textAlign: "center"
      },
      completeTitle : {
        textAlign: "center",
        fontSize: "48px",
        marginTop: "5%"
      },
      completeIcon : {
        align: "center",
        width: "100%",
        fontSize: "72px"
      },
      completeText : {
        textAlign: "center",
        fontSize: "32px"
      }
    };
    return (
      <Modal open={this.state.open}>
        {this.progressContent(this.props.progress, this.state.complete, styles)}
      </Modal>
    );
  }
}

export default UpgradeProgress
