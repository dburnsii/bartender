import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import Button from '@material-ui/core/Button';
import reportWebVitals from './reportWebVitals';
import BartenderDrawer from './drawer.js';
import DrinkCards from './drinks.js';

ReactDOM.render(
	<div>
	<BartenderDrawer/>
	<main style={{ marginLeft: 77 }}>
	<DrinkCards/>
	</main>
	</div>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
