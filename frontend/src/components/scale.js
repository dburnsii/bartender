import React from 'react';
import { Button, CircularProgress, Box, Typography } from '@mui/material';

class Scale extends React.Component {
  constructor(props){
    super(props);
    this.measureToText = this.measureToText.bind(this);
    this.state = {
        measureText: "0.0 fl oz"
    }
  }

  measureToText(weight){
        var unit = "";
	if(this.props.metric){
		unit = " grams";
	} else {
		unit = " fl oz";
	}

	if(weight == 0 || !this.props.presence) {
		return "0.0" + unit;
	} else if(this.props.metric){
		return weight + unit;
	}
 	else{
		return (0.033814023 * weight).toFixed(1) + unit;
	}
  }

  componentWillUnmount(){
  }

  render() {
    const styles = {
      box : {
        margin: "15px 5px 5px 5px"

      }
    };
    return (
        <Box position="relative" style={styles.box}>
          <Typography
            variant="h3"
            align="center"
            color={((this.props.presence) ? "textPrimary" : "error" )} >
	          {this.measureToText(this.props.weight)}
	        </Typography>
        </Box>
    );
  }
}

export default Scale
