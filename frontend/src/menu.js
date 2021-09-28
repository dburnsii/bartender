import React from 'react';
import PropTypes from 'prop-types';
import AppBar from '@mui/material/AppBar';
import CircularProgress from '@mui/material/CircularProgress';
import CssBaseline from '@mui/material/CssBaseline';
import Divider from '@mui/material/Divider';
import Drawer from '@mui/material/Drawer';
import Hidden from '@mui/material/Hidden';
import IconButton from '@mui/material/IconButton';
import InboxIcon from '@mui/icons-material/MoveToInbox';
import LocalGasStationIcon from '@mui/icons-material/LocalGasStation';
import HomeIcon from '@mui/icons-material/Home';
import SearchIcon from '@mui/icons-material/Search';
import SettingsIcon from '@mui/icons-material/Settings';
import TuneIcon from '@mui/icons-material/Tune';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import MailIcon from '@mui/icons-material/Mail';
import MenuIcon from '@mui/icons-material/Menu';
import LightIcon from '@mui/icons-material/Light';
import NotInterestedIcon from '@mui/icons-material/NotInterested';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import { makeStyles, useTheme } from '@mui/material/styles';
import './menu.css';


class Menu extends React.Component {
  render(){
    const drawerWidth = 110;

    const drawer = (
    <div>
      <List>
        <ListItem button key='Favorites' selected={this.props.page == 'favorites'} onClick={() => this.props.changePage('favorites')}>
           <ListItemIcon> <HomeIcon className="menuIcon" /></ListItemIcon>
         </ListItem>
         <ListItem button selected={this.props.page == 'search'} key='Search'>
            <ListItemIcon> <NotInterestedIcon className="menuIcon" /></ListItemIcon>
         </ListItem>
         <ListItem button selected={this.props.page == 'manual'} key='Manual' onClick={() => this.props.changePage('manual')}>
            <ListItemIcon> <TuneIcon className="menuIcon" /></ListItemIcon>
         </ListItem>
         <ListItem button selected={this.props.page == 'gasstation'} key='GasStation'>
            <ListItemIcon> <NotInterestedIcon className="menuIcon" /></ListItemIcon>
         </ListItem>
         <ListItem button selected={this.props.page == 'future'} key='future'>
            <ListItemIcon> <NotInterestedIcon className="menuIcon" /></ListItemIcon>
         </ListItem>
         <ListItem button selected={this.props.page == 'settings'} key='Settings' onClick={() => this.props.changePage('settings')}>
            <ListItemIcon> <SettingsIcon className="menuIcon" /></ListItemIcon>
         </ListItem>
      </List>
    </div>
    );

    const container = window !== undefined ? () => window().document.body : undefined;

    return (
      <div className="menu-root">
        <CssBaseline />
        <nav className="menu-drawer" aria-label="mailbox folders">
          <Drawer
            container={container}
            variant="permanent"
            anchor="left"
            classes={{
              paper: "menu-drawer-paper",
            }}
            ModalProps={{
              keepMounted: true, // Better open performance on mobile.
            }}
          >
            {drawer}
          </Drawer>
        </nav>
      </div>
    );
  }
}

export default Menu;
