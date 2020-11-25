import React from 'react';
import { Button, Card, LinearProgress, Box, Typography, Modal} from '@material-ui/core';
import PlayCircleFilledIcon from '@material-ui/icons/PlayCircleFilled';
import CloseIcon from '@material-ui/icons/Close';
//import Modal from '@material-ui/core/Modal';
import { titleCase } from "title-case";
import { green } from '@material-ui/core/colors';

class DrinkProgress extends React.Component {
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
      }
    };
    return (
      <Modal open={this.props.open} onClose={this.props.hide}>
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
      </Modal>
    );
  }
}

export default DrinkProgress
