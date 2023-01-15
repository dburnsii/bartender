import React from 'react';
import { Card, Typography, TextField, Modal, CircularProgress} from '@mui/material';
import Keyboard from 'react-simple-keyboard';
import 'react-simple-keyboard/build/css/index.css';
import '../App.css'

class LockScreen extends React.Component {
  constructor(props){
    super(props);
    this.purpose = this.props.purpose || "unlock" // Options: unlock, disable, enable
    this.onChange = this.onChange.bind(this);
    this.onKeyPress = this.onKeyPress.bind(this);
    this.getTextField = this.getTextField.bind(this);
    this.handleClose = this.handleClose.bind(this)
    this.inputField = React.createRef();
    this.keyboard = React.createRef();
    this.pinLength = 4;
    this.state = {
      input: "",
      disabled: false,
      open: true
    };
  }


  keyboardLayout = {
  'default': [
    '1 2 3',
    '4 5 6',
    '7 8 9',
    '{enter} 0 {bksp}'
  ]}

  keyboardDisplay = {
    '{enter}': '⏎',
    '{bksp}': '⌫'
  }

  onChange(input) {
    if(!this.state.disabled){
      this.setState({input: input});
    }
  }

  onKeyPress(button) {
    if(!this.state.disabled){
      this.inputField.current.children[0].children[0].focus();
    }

    if(button === "{enter}"){
      if(this.purpose === "unlock"){
        if(this.state.input === this.props.pin ){
          this.setState({disabled: false, input: ""});
          this.keyboard.clearInput();
          this.props.unlock();
        } else {
          this.setState({disabled: true, input: ""});
          this.keyboard.clearInput();
          setTimeout(
            () => {this.setState({disabled: false})},
            3000);
        }
      } else if(this.purpose === "disable"){
        if(this.state.input === this.props.pin ){
          this.setState({disabled: false, input: ""});
          this.keyboard.clearInput();
          this.props.clearPin();
        } else {
          this.setState({disabled: true, input: ""});
          this.keyboard.clearInput();
          setTimeout(
            () => {this.setState({disabled: false})},
            3000);
        }
      } else if(this.purpose === "enable"){
        if(this.state.input.length === this.pinLength){
          this.props.setPin(this.state.input)
        } else {
          // TODO: Make this more clear to the user
          console.log("Invalid pin!");
          this.setState({input: ""});
          this.keyboard.clearInput();
        }
      }
    }
  }

  handleClose() {
    if(this.props.purpose === "enable" || this.props.purpose === "disable") {
      this.props.cancel();
    }
  }

  getTextField(disabled) {
    const styles = {
      progress : {
        align: "center"
      },
      pinField : {
        width: "40%",
        height: "20px",
        margin: "5% 30% 8% 30%",
        align: "center",
        fontSize: "40px",
        textAlign: "center"
      }
    }

    if(disabled){
      return (<CircularProgress/>)
    } else {
      return (
        <TextField
          style={styles.pinField}
          id="pinField"
          ref={this.inputField}
          variant="outlined"
          type="password"
          className="lockScreenInput"
          value={this.state.input}
          disabled={this.state.disabled}
          error={this.state.disabled} />)
    }
  }

  getPromptText(purpose){
    if(purpose === "unlock"){
      return "Enter Pin: ";
    } else if(purpose === "enable"){
      return "Enter New Pin: "
    } else if(purpose === "disable"){
      return "Enter Current Pin: "
    } else {
      console.log("Unknown purpose: " + purpose);
      return "Enter Pin: ";
    }
  }

  componentDidMount(){}

  componentWillUnmount(){}

  shouldComponentUpdate(nextProps, nextState){
    //if(this.props.open !== nextProps.open){
    //  return true;
    //} else if(this.state.input !== nextState.input) {
    //  return true;
    //}
    return true;
  }

  render() {
    const styles = {
      card : {
        width: "40%",
        height: "160px",
        marginTop: "3%",
        marginLeft: "30%",
        marginRight: "30%"
      },
      keyboard : {
        height: "300px"
      }
    };
    return (
      <Modal open={this.props.open} onClose={this.handleClose}>
        <div>
          <Card style={styles.card}>
            <br/>
            <Typography
              align="center"
              variant="h4">
              {this.getPromptText(this.purpose)}
            </Typography>
            {this.getTextField(this.state.disabled)}
          </Card>
          <Keyboard
            onChange={this.onChange}
            onKeyPress={this.onKeyPress}
            layout={this.keyboardLayout}
            preventMouseDownDefault={true}
            preventMouseUpDefault={true}
            stopMouseDownPropagation={true}
            stopMouseUpPropagation={true}
            useMouseEvents={true}
            keyboardRef={(r) => (this.keyboard = r)}
            theme={"lockScreenKeyboard"}
            buttonTheme={"lockScreenButton"}
            display={this.keyboardDisplay} />
        </div>
      </Modal>
    );
  }
}

export default LockScreen
