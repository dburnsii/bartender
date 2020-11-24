import React from 'react';
import styles from './App.css';
import { makeStyles } from '@material-ui/core/styles';
import Drawer from '@material-ui/core/Drawer';
import List from '@material-ui/core/List';
import Typography from '@material-ui/core/Typography';
import Divider from '@material-ui/core/Divider';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import SearchIcon from '@material-ui/icons/Search';
import HomeIcon from '@material-ui/icons/Home';
import CreateIcon from '@material-ui/icons/Create';
import AndroidIcon from '@material-ui/icons/Android';
//import CreateIcon from '@material-ui/icons/Create';
import SettingsIcon from '@material-ui/icons/Settings';
import Icon from '@material-ui/core/Icon';

const drawerWidth = 75;

function DrawerButton(props) {
	return (
		<ListItem button divider="true">
			<Icon style={{ fontSize: 42 }}>{props.name}</Icon>
		</ListItem>
	);
}

const useStyles = makeStyles((theme) => ({
	root: {
		display: 'flex',
	},
	appBar: {
		width: `calc(100% - ${drawerWidth}px)`,
		marginLeft: drawerWidth,
	},
	drawer: {
		width: drawerWidth,
		flexShrink: 0,
	},
	drawerPaper: {
		width: drawerWidth,
	},
	// necessary for content to be below app bar
	toolbar: theme.mixins.toolbar,
	content: {
		flexGrow: 1,
		backgroundColor: theme.palette.background.default,
		padding: theme.spacing(3),
	},
	drawerIcon: {
		fontSize: 40
	},
	drawerButton: {
		disableGutters: true,
		divider: true
	},
}));

export default function BartenderDrawer() {
	const classes = useStyles();

  return (
      <Drawer
        className={classes.drawer}
        variant="permanent"
        classes={{
          paper: classes.drawerPaper,
        }}
        anchor="left"
		    style={{ flexShrink: 0, overflow: "hidden" }}
      >
        <List>
					{["home", "search", "create", "android", "settings"].map((value) => (
						<DrawerButton name={value}/>
					))}
        </List>
      </Drawer>
  );
}
