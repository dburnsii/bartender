import React from 'react';
import PropTypes from 'prop-types';
import AppBar from '@material-ui/core/AppBar';
import CircularProgress from '@material-ui/core/CircularProgress';
import CssBaseline from '@material-ui/core/CssBaseline';
import Divider from '@material-ui/core/Divider';
import Drawer from '@material-ui/core/Drawer';
import Hidden from '@material-ui/core/Hidden';
import IconButton from '@material-ui/core/IconButton';
import InboxIcon from '@material-ui/icons/MoveToInbox';
import LocalGasStationIcon from '@material-ui/icons/LocalGasStation';
import HomeIcon from '@material-ui/icons/Home';
import SearchIcon from '@material-ui/icons/Search';
import SettingsIcon from '@material-ui/icons/Settings';
import TuneIcon from '@material-ui/icons/Tune';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import MailIcon from '@material-ui/icons/Mail';
import MenuIcon from '@material-ui/icons/Menu';
import NotInterestedIcon from '@material-ui/icons/NotInterested';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Box from '@material-ui/core/Box';
import { makeStyles, useTheme } from '@material-ui/core/styles';
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
