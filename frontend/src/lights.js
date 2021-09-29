import React from 'react';
import { Box, Typography } from '@mui/material';

class LightsPage extends React.Component {
  constructor(props){
    super(props);
  }

  render() {
    const styles = {
      box: {
        margin: "100px"
      }
    }
    return (
      <Box position="relative" display="inline-block" style={styles.box}>
        <Typography>
          Coming soon!
        </Typography>
      </Box>
    );
  }
}

export default LightsPage
