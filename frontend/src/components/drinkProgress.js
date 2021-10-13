import React from 'react';
import { Button, Card, LinearProgress, Box, Typography, Modal} from '@mui/material';
import PlayCircleFilledIcon from '@mui/icons-material/PlayCircleFilled';
import CloseIcon from '@mui/icons-material/Close';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import { titleCase } from "title-case";
import { green } from '@mui/material/colors';

class DrinkProgress extends React.Component {
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
    if(this.props.progress != nextProps.progress){
      return true;
    } else if(this.props.open != nextProps.open){
      if(nextProps.open){
        this.setState({open: nextProps.open})
      } else {
        this.setState({complete: true})
        setTimeout(() => {
          this.setState({open: false, complete: false})
        }, this.completedTime);
      }
      return true;
    } else if(this.state.open != nextState.open){
      return true;
    } else if(this.state.complete != nextState.complete) {
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
            Enjoy your beverage!
          </Typography>
        </Card>
      )
    } else {
      return(
        <Card style={styles.card}>
          <Typography style={styles.text}>
            Pour in progress
          </Typography>
          <LinearProgress
            variant="determinate"
            value={this.props.progress}
            style={styles.progress}/>
          <Box style={styles.cancelBox}>
            <Button
              style={styles.cancel}
              variant="contained"
              color="secondary"
              onClick={this.props.cancelPour}>
              Cancel
            </Button>
          </Box>
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
        margin: "5% 10% 8% 10%",
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
      <Modal open={this.state.open} onClose={this.props.hide}>
        {this.progressContent(this.props.progress, this.state.complete, styles)}
      </Modal>
    );
  }
}

export default DrinkProgress
