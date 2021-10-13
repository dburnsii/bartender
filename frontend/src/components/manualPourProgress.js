import React from 'react';
import { Button, Card, LinearProgress, Box, Typography, Modal} from '@mui/material';
import PlayCircleFilledIcon from '@mui/icons-material/PlayCircleFilled';
import CloseIcon from '@mui/icons-material/Close';
import { titleCase } from "title-case";
import { green } from '@mui/material/colors';

class ManualPourProgress extends React.Component {
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
      ingredientName : {
        textAlign: "center",
        margin: "0% 5% 5% 2%",
        fontSize: "42px"
      },
      instructions : {
        textAlign: "center",
        margin: "0% 5% 5% 5%",
        fontSize: "16px"
      },
      progress : {
        width: "80%",
        height: "20px",
        margin: "5% 10% 8% 10%",
        borderRadius: "10px"
      },
      skip : {
        align: "center",
        margin: "2%"
      },
      cancel : {
        align: "center",
        margin: "2%"
      },
      cancelBox : {
        width: "100%",
        textAlign: "center"
      }
    };
    return (
      <Modal open={this.props.open} onClose={this.props.hide}>
        <Card style={styles.card}>
          <Typography style={styles.ingredientName}>
            {titleCase(this.props.name || "")}
          </Typography>
          <Typography style={styles.instructions}>
            Pour until LEDs below meet in the middle.
          </Typography>
          <LinearProgress
            variant="determinate"
            value={this.props.progress}
            style={styles.progress}/>
          <Box style={styles.cancelBox}>
          <Button
            style={styles.skip}
            variant="contained"
            color="secondary"
            onClick={this.props.cancelPour}>
            Skip
          </Button>
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

export default ManualPourProgress
