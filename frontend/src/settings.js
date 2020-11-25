import React from 'react';
import { Button, Divider , Box, Typography, Grid } from '@material-ui/core';

class SettingsPage extends React.Component {

  constructor(props){
    super(props);
    this.state = {

    };
  }

  componentDidMount() {

  }

  componentWillUnmount(){

  }


  render() {
    const styles = {
      box : {
        margin: "10px 10px 10px 80px"
      }

    };
    return (
        < Box position="relative" style={styles.box}>
        <Button variant="contained" onClick={() => window.location.reload(false)}>Refresh</Button>
        </Box>
    );
  }
}

export default SettingsPage
