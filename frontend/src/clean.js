import React from 'react';
import { Button, Box, Typography, Grid, Slider, CircularProgress } from '@mui/material';
import RefreshIcon from '@mui/icons-material/Refresh';

class CleanPage extends React.Component {

  constructor(props){
    super(props);
    this.startClean = this.startClean.bind(this)
    this.state = {};
  }

  componentDidMount() { }

  componentWillUnmount(){ }

  startClean() {
    this.props.socket.emit("clean_valve", {"pin": 8})
  }

  render() {
    const styles = {
      box : {
        margin: "15px 15px 15px 110px"
      },
    };
    return (
        <Box position="relative" display="inline-block" style={styles.box}>
          <Typography variant="h4">Cleaning</Typography>
          <Grid container columns={20}>
            <Grid item xs={4}>
              <Button variant="outlined" onClick={this.startClean}>1</Button>
            </Grid>
            <Grid item xs={4}>
              <Button variant="outlined" onClick={this.startClean}>2</Button>
            </Grid>
            <Grid item xs={4}>
              <Button variant="outlined" onClick={this.startClean}>3</Button>
            </Grid>
            <Grid item xs={4}>
              <Button variant="outlined" onClick={this.startClean}>4</Button>
            </Grid>
            <Grid item xs={4}>
              <Button variant="outlined" onClick={this.startClean}>5</Button>
            </Grid>
            <Grid item xs={4}>
              <Button variant="outlined" onClick={this.startClean}>6</Button>
            </Grid>
            <Grid item xs={4}>
              <Button variant="outlined" onClick={this.startClean}>7</Button>
            </Grid>
            <Grid item xs={4}>
              <Button variant="outlined" onClick={this.startClean}>8</Button>
            </Grid>
            <Grid item xs={4}>
              <Button variant="outlined" onClick={this.startClean}>9</Button>
            </Grid>
            <Grid item xs={4}>
              <Button variant="outlined" onClick={this.startClean}>10</Button>
            </Grid>
          </Grid>
        </Box>
    );
  }
}

export default CleanPage
