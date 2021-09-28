import React from 'react';
import { Button, CircularProgress, Box, Typography } from '@mui/material';
import { makeStyles, useTheme } from '@mui/material/styles';
const drawerWidth = 60;



class ScalePage extends React.Component {
  constructor(props){
    super(props);
    this.metric = false;
    this.state = {
      weight: 40,
      present: false};
  }

  normalize(value){
    return value / 2;
  }

  componentDidMount() {
		this.props.socket.on('weight', (data) => {
			this.setState({
				weight: data
			})
		});
  }

  componentWillUnmount(){
    clearInterval(this.timer);
  }

  render() {
    const styles = {
      box : {
        margin: "10px 10px 10px 100px"
      }
    };
    return (
        <Box position="relative" display="inline-flex" style={styles.box}>
          <CircularProgress size={200} variant="determinate" value={this.normalize(this.state.weight)} />
          <Box
            top={0}
            left={0}
            bottom={0}
            right={0}
            position="absolute"
            display="flex"
            alignItems="center"
            justifyContent="center"
          >
            <Typography variant="caption" component="div" color="textSecondary">{`${Math.round(
              this.normalize(this.state.weight),
            )} g`}</Typography>
          </Box>

        </Box>
    );
  }
}

export default ScalePage
