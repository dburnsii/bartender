import React from 'react';
import ReactDOM from 'react-dom';
import { Button, CircularProgress, Box, Typography } from '@material-ui/core';
import './index.css';
//import App from './App';
import reportWebVitals from './reportWebVitals';
import Menu from './menu';
import ScalePage from './scale';
import Bartender from './bartender';


ReactDOM.render(
  <React.StrictMode>
	  <Bartender/>
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
