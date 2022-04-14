import React from 'react';
import CssBaseline from '@mui/material/CssBaseline';
import Drawer from '@mui/material/Drawer';
import HomeIcon from '@mui/icons-material/Home';
import SettingsIcon from '@mui/icons-material/Settings';
import TuneIcon from '@mui/icons-material/Tune';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import LightIcon from '@mui/icons-material/Light';
import NotInterestedIcon from '@mui/icons-material/NotInterested';
import LocalLaundryServiceIcon from '@mui/icons-material/LocalLaundryService';
import './menu.css';


class Menu extends React.Component {
  render(){
    const drawer = (
    <div>
      <List>
        <ListItem button key='Favorites' selected={this.props.page === 'favorites'} onClick={() => this.props.changePage('favorites')}>
           <ListItemIcon> <HomeIcon className="menuIcon" /></ListItemIcon>
         </ListItem>
         <ListItem button selected={this.props.page === 'search'} key='Search'>
            <ListItemIcon> <NotInterestedIcon className="menuIcon" /></ListItemIcon>
         </ListItem>
         <ListItem button selected={this.props.page === 'manual'} key='Manual' onClick={() => this.props.changePage('manual')}>
            <ListItemIcon> <TuneIcon className="menuIcon" /></ListItemIcon>
         </ListItem>
         <ListItem button selected={this.props.page === 'clean'} key='Clean' onClick={() => this.props.changePage('clean')}>
            <ListItemIcon> <LocalLaundryServiceIcon className="menuIcon" /></ListItemIcon>
         </ListItem>
         <ListItem button selected={this.props.page === 'lights'} key='lights' onClick={() => this.props.changePage('lights')}>
            <ListItemIcon> <LightIcon className="menuIcon" /></ListItemIcon>
         </ListItem>
         <ListItem button selected={this.props.page === 'settings'} key='Settings' onClick={() => this.props.changePage('settings')}>
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
