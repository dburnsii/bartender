import React from 'react';
import { Card, Box, Button, CircularProgress, Typography } from '@mui/material';
import DrinkCard from './components/drinkCard';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import VisibilityIcon from '@mui/icons-material/Visibility';
import VisibilityOffIcon from '@mui/icons-material/VisibilityOff';
import SentimentVeryDissatisfiedIcon from '@mui/icons-material/SentimentVeryDissatisfied';

class FavoritesPage extends React.Component {
  constructor(props){
    super(props);
    this.drinksPerPage = 6;
    this.drinksUrl = "http://" + window.location.hostname + ":5000/drinks?limit=" + this.drinksPerPage;
    this.updatingDrinks = false;
    this.valves = []
    this.drinkCards = this.drinkCards.bind(this);
    this.nextPage = this.nextPage.bind(this);
    this.prevPage = this.prevPage.bind(this);
    this.toggleFilter = this.toggleFilter.bind(this);
    this.cards = [];
    this.state = {
      page: 0,
      drinks: [],
      morePages: false,
      filter: true,
      valves: []
    }
  }

  shouldComponentUpdate(nextProps, nextState){
    return true;
  }

  componentDidMount() {
    fetch(this.drinksUrl + "&skip=0&pourable=1")
      .then(response => response.json())
      .then((data) => {
        this.setState({
          drinks: [data]
        });
        fetch(this.drinksUrl + "&skip=" + this.drinksPerPage + "&pourable=1")
          .then(response => response.json())
          .then((data) => {
            if(data.length){
              this.setState({
                drinks: [...this.state.drinks, data],
                morePages: true
              });
            } else {
              this.setState({morePages: false})
            }
          });
      });
    fetch("http://" + window.location.hostname + ":5000/valves?resolve=1")
      .then(response => response.json())
      .then((data) => {
        // Clean the list to only contain the available ingredients
        this.setState({valves: data.map((d) => { return(d.ingredient ? d.ingredient.name : null ) }).filter((d) => d)});
      });
  }

  componentWillUnmount(){
  }

  drinkCards(drinks, page){
    console.log(drinks)
    console.log(this.state.valves);
    if(drinks.length > page){
      if(this.cards.length <= page) {
        this.cards[page] = drinks[page].map((drink, index) => {
            console.log("Making drink card: " + drink.name)
           return (<DrinkCard
            key={drink['_id']['$oid'] + "card"}
            socket={this.props.socket}
            id={drink['_id']['$oid']}
            name={drink['name']}
            image={drink['image']}
            valves={this.state.valves}/>)})
        console.log("created new page")
        console.log(this.cards)
      }
      if(this.cards[page].length == 0){
        return (
          <Box style={{width: "100%",
                       height: "100%",
                       padding: "125px 0 0 0",
                       textAlign: "center"}}>
            <SentimentVeryDissatisfiedIcon/>
            <Typography>No drinks available! Try loading more ingredients?</Typography>
          </Box>
        )
      }
      return this.cards[page]
    } else {
      return (
        <Box style={{width: "100%",
                     height: "100%",
                     padding: "125px 0 0 0",
                     textAlign: "center"}}>
          <CircularProgress
            disableShrink={true}/>
        </Box>
      );
    }
  }

  loadNext(){
    fetch(this.drinksUrl + "&skip=" + (this.drinksPerPage * this.state.drinks.length) +
            "&pourable=" + (this.state.filter ? "1" : "0"))
      .then(response => response.json())
      .then((data) => {
        if(data.length > 0){
          this.setState({drinks: [...this.state.drinks, data]});
        }
      });
  }

  nextPage(){
    if(this.state.drinks.length > this.state.page){
      if(this.state.drinks[this.state.page + 1]){
        this.setState({page: this.state.page + 1})
        this.loadNext()
      } else {
        this.setState({morePages: false})
      }
    } else {
      this.setState({morePages: false})
    }
  }

  prevPage(){
    if(this.state.page > 0){
      this.setState({
        page: this.state.page - 1,
        morePages: true
      });
    }
  }

  toggleFilter(){
    this.setState({filter: !this.state.filter, page: 0}, () => {

      fetch(this.drinksUrl + "&skip=0&pourable=" + (this.state.filter ? "1" : "0"))
        .then(response => response.json())
        .then((data) => {
          this.setState({
            drinks: [data]
          }, () => {this.cards.length = 0});
          fetch(this.drinksUrl + "&skip=" + this.drinksPerPage + "&pourable=0" + (this.state.filter ? "1" : "0"))
            .then(response => response.json())
            .then((data) => {
              if(data.length){
                this.setState({
                  morePages: true,
                  drinks: [...this.state.drinks, data]
                }, () => {this.cards.length = 0});
              } else {
                this.setState({morePages: false})
              }
            });
        });
      }
    );
  }

  render() {
    const styles = {
      box : {
        margin: "10px 10px 10px 92px"
      },
      prevButton: {
        width: "40px",
        height: "150px",
        position: "absolute",
        top: "145px",
        left: "-15px"
      },
      prevButtonIcon: {
        fontSize: "80px"
      },
      nextButton: {
        width: "40px",
        height: "150px",
        position: "absolute",
        top: "145px",
        right: "-15px"
      },
      nextButtonIcon: {
        fontSize: "80px"
      },
      drinksContainer : {
        margin: "0px 35px 0px 35px",
        width: "635px"
      },
      filter : {
        position: "fixed",
        top: "10px",
        right: "10px",
        fontSize: "40px"
      }
    };
    return (
      <Box position="relative" display="inline-block" style={styles.box}>
        <Button
          disableRipple={true}
          disabled={this.state.page === 0}
          style={styles.prevButton}
          onClick={this.prevPage}>
          <ChevronLeftIcon style={styles.prevButtonIcon}/>
        </Button>
        <Box style={styles.drinksContainer}>
          {this.drinkCards(this.state.drinks, this.state.page)}
        </Box>
        <Button
          disableRipple={true}
          disabled={!this.state.morePages}
          style={styles.nextButton}
          onClick={this.nextPage}>
          <ChevronRightIcon style={styles.nextButtonIcon}/>
        </Button>
        <Box style={styles.filter} onClick={this.toggleFilter}>
          {this.state.filter ? <VisibilityOffIcon fontSize="inherit"/> : <VisibilityIcon fontSize="inherit"/>}
        </Box>
      </Box>
    );
  }
}

export default FavoritesPage
