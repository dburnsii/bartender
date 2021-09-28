import React from 'react';
import { Card, Box, Button, CircularProgress } from '@mui/material';
import DrinkCard from './components/drinkCard';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';

class SearchPage extends React.Component {
  constructor(props){
    super(props);
    this.drinksPerPage = 4;
    this.drinksUrl = "http://" + window.location.hostname + ":5000/drinks?limit=" + this.drinksPerPage;
    this.updatingDrinks = false;
    this.drinkCards = this.drinkCards.bind(this);
    this.nextPage = this.nextPage.bind(this);
    this.prevPage = this.prevPage.bind(this);
    this.cards = [];
    this.state = {
      page: 0,
      drinks: [],
      morePages: true
    }
  }

  componentDidMount() {
    fetch(this.drinksUrl + "&skip=0")
      .then(response => response.json())
      .then((data) => {
        this.setState({
          drinks: [data]
        });
        fetch(this.drinksUrl + "&skip=" + this.drinksPerPage)
          .then(response => response.json())
          .then((data) => {
            this.setState({
              drinks: [...this.state.drinks, data]
            });
          });
      });
  }

  componentWillUnmount(){
  }

  drinkCards(drinks, page){
    if(drinks.length > page){
      if(this.cards.length <= page) {
        this.cards[page] = drinks[page].map((drink, index) => {
            console.log("Making drink card: " + drink.name)
           return (<DrinkCard
            key={(page * this.drinksPerPage) + index}
            socket={this.props.socket}
            id={drink['_id']['$oid']}
            name={drink['name']}
            image={drink['image']}/>)})
        console.log("created new page")
        console.log(this.cards)
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
    fetch(this.drinksUrl + "&skip=" + (this.drinksPerPage * this.state.drinks.length))
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

  render() {
    const styles = {
      box : {
        margin: "10px 10px 10px 80px"
      },
      prevButton: {
        width: "40px",
        height: "150px",
        position: "absolute",
        top: "70px",
        left: "-15px"
      },
      prevButtonIcon: {
        fontSize: "80px"
      },
      nextButton: {
        width: "40px",
        height: "150px",
        position: "absolute",
        top: "70px",
        right: "-15px"
      },
      nextButtonIcon: {
        fontSize: "80px"
      },
      drinksContainer : {
        margin: "0px 35px 0px 35px",
        width: "325px"
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
      </Box>
    );
  }
}

export default SearchPage
