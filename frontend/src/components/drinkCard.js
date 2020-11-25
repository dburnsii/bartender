import React from 'react';
import { Button, Card, CircularProgress, Box, Typography, Dialog, DialogContent, DialogTitle, TableContainer, Table, TableBody, TableRow, TableCell, IconButton, Paper} from '@material-ui/core';
import PlayCircleFilledIcon from '@material-ui/icons/PlayCircleFilled';
import CloseIcon from '@material-ui/icons/Close';
import Modal from '@material-ui/core/Modal';
import { titleCase } from "title-case";
import { green } from '@material-ui/core/colors';

class DrinkCard extends React.Component {
  constructor(props){
    super(props);
    this.ingredients = [];
    this.showDrink = this.showDrink.bind(this);
    this.hideDrink = this.hideDrink.bind(this);
    this.getIngredientTable = this.getIngredientTable.bind(this);
    this.pourDrink = this.pourDrink.bind(this);
    this.state = {
      activated: false,
      ingredients: [],
      available: true
    }
  }


  componentDidMount(){
    console.log("Mounting card: " + this.props.name);
    console.log(this.props.valves)
    if(this.state.ingredients.length == 0){
      fetch("http://" + window.location.hostname + ":5000/drinks/" + this.props.id)
        .then(response => response.json())
        .then((data) => {
          this.ingredients = data.ingredients
          console.log(this.props.name + " -> " + JSON.stringify(this.ingredients))
          this.ingredients.forEach((ingredient, index) => {
            fetch("http://" + window.location.hostname + ":5000/ingredients?name=" + ingredient.ingredient)
              .then(response => response.json())
              .then((data) => {
                this.setState({ingredients: [...this.state.ingredients, data]});
                if(data.required && !(data.ingredient in this.props.valves)){
                  console.log("Missing required ingredient. marking as unavailable");
                  this.setState({available: false});
                }
              });
          });
        });
      } else {
        console.log("Prefilled ingredients! " + JSON.stringify(this.state.ingredients))
      }
  }

  componentWillUnmount(){
  }

  checkAvailability(valves, ingredients){

  }

  showDrink(){
    this.setState({activated: true});
  }

  hideDrink(){
    this.setState({activated: false});
  }

  quantityText(ingredient){
    const ing_prop =  this.ingredients.find(x => x.ingredient == ingredient.name)
    if(ingredient.measure == "mL"){
      return `• ${ing_prop.quantity} mL`
    } else if(ingredient.measure == "dash"){
      return `• ${ing_prop.quantity} dah(es)`
    } else if(ingredient.measure == "count"){
      return `• ${ing_prop.quantity}`
    }
  }

  getIngredientTable(ingredients, start, end){
    const styles = {
      ingredientColumn : {
        width: "50%",
        display: "inline-block",
        verticalAlign: "top"
      },
      ingredientCell : {
        padding: "4px",
        border: "none",
        fontSize: "24px"
      },
      ingredientCellUnavailable : {
        padding: "4px",
        border: "none",
        color: "red",
        fontSize: "24px"
      },
    };
    if(ingredients.length > 0){
      return(
        <TableContainer key={this.props.id + "tc"} style={styles.ingredientColumn}>
          <Table>
            <TableBody>
            {this.state.ingredients.slice(start, end).map((value, index) =>
              {
                if("name" in value && this.props.valves){
                  const ing_prop =  this.ingredients.find(x => x.ingredient == value.name)
                  if(ing_prop.required && this.props.valves.includes(value.name)){
                    return (
                      <TableRow style={styles.ingredientRow}>
                        <TableCell style={styles.ingredientCell}>{this.quantityText(value)}</TableCell>
                        <TableCell style={styles.ingredientCell}>{titleCase(value.name)}</TableCell>
                      </TableRow> )
                    } else {
                      return (
                        <TableRow style={styles.ingredientRow}>
                          <TableCell style={styles.ingredientCellUnavailable}>{this.quantityText(value)}</TableCell>
                          <TableCell style={styles.ingredientCellUnavailable}>{titleCase(value.name)}</TableCell>
                        </TableRow> )
                    }
                }
              }
            )}
            </TableBody>
          </Table>
        </TableContainer>
      );
    }
  }

  pourDrink(){
    console.log("Pouring drink!");
    this.setState({activated: false});
    this.props.socket.emit("drink_pour", {id: this.props.id})
  }

  render() {
    const styles = {
      card : {
        margin: "5px 5px 5px 5px",
        width: "190px",
        height: "190px",
        display: "inline-block",
        position: "relative"
      },
      image : {
        width : "100%"
      },
      title : {
        position: "absolute",
        bottom : "0px",
        color: "white",
        width: "100%",
        textAlign: "center",
        backgroundColor: "rgba(0, 0, 0, 0.59)",
        padding: "3px",
        fontSize: "large"
      },
      modalBox: {
        position: "absolute",
        inset: "0px",
        //left: "70px",
        width: "750px",
        height: "400px",
        margin: "15px",

      },
      modalImageContainer : {
        height: "100px",
        width: "100%",
        overflow: "hidden",
        position: "absolute",
        top: "0px",
        left: "0px"
      },
      modalImageShadow : {
        height: "100%",
        width: "100%",
        backgroundColor: "#000A",
        zIndex: "6",
        position: "absolute",
        top: "0px",
        left: "0px"
      },
      modalImage : {
        width: "100%",
        position: "absolute",
        top: "-150px",
        zIndex: "5"
      },
      modalClose : {
        position: "absolute",
        color: "white",
        top: "0px",
        right: "0px",
        fontSize: "36px",
        zIndex: "7"
      },
      modalIngredients : {
        position: "absolute",
        top: "100px",
        width: "100%",
        padding: "10px",
        zIndex: "7"
      },
      modalTitle : {
        color: "white",
        fontSize: "xx-large",
        width: "100%",
        textAlign: "center",
        paddingTop: "25px",
        zIndex: "7"
      },
      modalPaper : {
        width: "100%",
        height: "100%",
        maxHeight: "100%",
        margin: "15px"
      },
      ingredientColumn : {
        width: "50%",
        display: "inline-block",
        verticalAlign: "top"
      },
      ingredientCell : {
        padding: "4px",
        border: "none"
      },
      pourButton : {
        color: green[500],
        position: "fixed",
        bottom: "25px",
        right: "70px",
        fontSize: "84px"
      }
    };
    return (
      <div key={this.props.id + "root"} style={styles.card}>
        <Dialog
          open={this.state.activated}
          onClose={this.hideDrink}
          style={styles.modalBox}
          transitionDuration={0}
          PaperProps={{style: styles.modalPaper}}>
            <div style={styles.modalImageContainer}>
              <div style={styles.modalImageShadow}/>
              <img style={styles.modalImage} src={"/images/drinks/images/" + this.props.image} />
            </div>
            <Typography style={styles.modalTitle}>
              {titleCase(this.props.name)}
            </Typography>
            <Button onClick={this.hideDrink} style={styles.modalClose}>
              <CloseIcon/>
            </Button>
            <div key={this.props.id + "table"} style={styles.modalIngredients}>
              {this.getIngredientTable(this.state.ingredients, 0,5)}
              {this.getIngredientTable(this.state.ingredients, 5,10)}
              <IconButton style={styles.pourButton}  onClick={this.pourDrink}>
                <PlayCircleFilledIcon style={{fontSize: "100px"}}/>
              </IconButton>
          </div>
        </Dialog>
      <Card onClick={this.showDrink} style={styles.card}>
        <img style={styles.image} src={"/images/drinks/images/" + this.props.image} />
        <Box style={styles.title}>{titleCase(this.props.name)}</Box>
      </Card>
      </div>
    );
  }
}

export default DrinkCard
