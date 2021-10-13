import React from 'react';
import { Button, Card, CircularProgress, Box, Typography, Backdrop, TextField } from '@mui/material';
import Autocomplete from '@mui/material/Autocomplete';
import { titleCase } from "title-case";
import Keyboard from 'react-simple-keyboard';
import 'react-simple-keyboard/build/css/index.css';
import { createFilterOptions } from '@mui/material/Autocomplete';

import AddCircleIcon from '@mui/icons-material/AddCircle';
import RemoveCircleIcon from '@mui/icons-material/RemoveCircle';



class ValveController extends React.Component {
  constructor(props){
    super(props);
    this.startPour = this.startPour.bind(this);
    this.getLabel = this.getLabel.bind(this);
    this.getKeyboard = this.getKeyboard.bind(this);
    this.getButton = this.getButton.bind(this);
    this.changeBottle = this.changeBottle.bind(this);
    this.closeKeyboard = this.closeKeyboard.bind(this);
    this.inputChange = this.inputChange.bind(this);
    this.clear = this.clear.bind(this);

    this.filterOptions = createFilterOptions({
      matchFrom: 'start',
      limit: 5,
      ignoreCase: true
    });

    this.state = {
      bottle: null,
      ingredient: null,
      typing: false,
      searchText: "",
    }
  }

  keyboardLayout = {
  'default': [
    'q w e r t y u i o p',
    'a s d f g h j k l',
    'z x c v b n m',
    '{shift} {space} {bksp}'
  ],
  'shift': [
    ' Q W E R T Y U I O P ',
    ' A S D F G H J K L {enter}',
    '{shift} Z X C V B N M {bksp}',
    ' {space}'
  ]
}

  onChange = (input) => {
    this.setState({searchText: input});
  }

  onKeyPress = (button) => {

  }

  startPour(e){
    e.preventDefault();
    console.log("Starting pour");
    console.log(this.props);
    this.props.socket.emit('activate_valve', {'pin': this.props.pin});
    document.documentElement.addEventListener('pointerup', (e) => {
      console.log("Shutting off all valves");
      this.props.socket.emit('deactivate_valves', {})
    }, { once: true });
  }

  getLabel(ingredient){
    if(ingredient == null){
      return <CircularProgress/>
    } else if("name" in ingredient){
      return titleCase(ingredient.name);
    } else if("id" in ingredient){
      console.log("Finna load up: " + JSON.stringify(ingredient));
      fetch("http://" + window.location.hostname + ":5000/ingredients/" + ingredient.id)
        .then(response => response.json())
        .then((data) => {
          console.log("Loaded ingredient__: ");
          console.log(data);
          this.setState({ingredient: Object.assign(this.state.ingredient, data)});
        });
      return <CircularProgress/>;
    } else {
      return "";
    }
  }

  inputChange(e, value, reason) {
    if(reason == "selectOption"){
      fetch("http://" + window.location.hostname + ":5000/valves/" + this.props.pin + "?ingredient=" + value.id,
        {method: "PUT"})
        .then(response => {console.log(response); this.componentDidMount()});
      this.setState({typing: false})
    }
  }

  getKeyboard(state){
    if(state){
      return (
          <div>
            <Autocomplete
              options={this.props.ingredients || []}
              getOptionLabel={x => titleCase(x.name)}
              style={{ width: 650, zIndex: "1200", position: "fixed", top: "10px", left: "70px" }}
              filterOptions={this.filterOptions}
              open={this.state.typing}
              onChange={this.inputChange}
              inputValue={this.state.searchText}
              renderInput={(params) => <TextField style={{backgroundColor: "white", }} {...params} />}
              />
            <Keyboard
              onChange={this.onChange}
              onKeyPress={this.onKeyPress}
              layout={this.keyboardLayout}/>
          </div>
      )
    }
  }

  getButton(ingredient){
    if(ingredient && "id" in ingredient ){
      return (
        <Button disableRipple={true} onClick={this.clear}>
          <RemoveCircleIcon style={{fontSize: "30px"}}/>
        </Button>)
    } else {
      return (
        <Button disableRipple={true} onClick={this.changeBottle}>
          <AddCircleIcon style={{fontSize: "30px"}}/>
        </Button>)
    }
  }

  closeKeyboard(){
    this.setState({typing: false});
  }

  changeBottle() {
    this.setState({typing: true})
  }

  clear(e){
    e.preventDefault();
    e.stopPropagation();
    fetch("http://" + window.location.hostname + ":5000/valves/" + this.props.pin,
      {method: "DELETE"})
      .then(response => {console.log(response); this.componentDidMount()});
  }

  componentDidMount() {
    fetch("http://" + window.location.hostname + ":5000/valves/" + this.props.pin)
      .then(response => response.json())
      .then((data) => {
        if('ingredient' in data && data.ingredient){
          this.setState({ingredient: data.ingredient});
        } else {
          console.log("Setting ingredient to nothin")
          this.setState({ingredient: {}});
        }
      });
  }

  componentWillUnmount(){
    this.props.socket.emit('deactivate_valves', {})
  }

  render() {
    const styles = {
      box : {
        margin: "5px 5px 5px 5px",
        width: "120px"
      },
      button : {
        borderRadius: "30px",
        minWidth: "50px",
        width: "120px",
        height: "50px"
      },
      bottleContainer : {
        height: "120px",
      },
      bottleContents : {
        paddingTop: "20px",
        height: "110px",
        backgroundColor: this.props.color,
        filter: 'greyscale(0.2)'
      },
      keyboard : {
        display: 'none'
      },
      keyboardBackdrop : {
        zIndex: "1200",
        display: "unset"
      },
      ingredientSearchBox : {

      }
    };
    return (
      <Box position="relative" display="inline-block" style={styles.box}>
        <Box style={styles.bottleContainer} onClick={this.changeBottle} >
          <Card style={styles.bottleContents}>
            <Typography align="center">
              {this.getLabel(this.state.ingredient)}
              <br/>
              {this.getButton(this.state.ingredient)}
            </Typography>
          </Card>
        </Box>
        <Button disableRipple={true} onPointerDown={this.startPour} style={styles.button} variant="contained"/>
        <Backdrop
          open={this.state.typing}
          style={styles.keyboardBackdrop}
          onClick={this.closeKeyboard}/>
        {this.getKeyboard(this.state.typing)}
      </Box>
    );
  }
}

export default ValveController
