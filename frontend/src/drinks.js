import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Grid from '@material-ui/core/Grid';

function DrinkCard(props) {
	return (
			<Grid item paper>
				<Card style={{width:150, margin: 10, padding: 10}}>
					<CardContent>
						<h1>{props.name}</h1>
					</CardContent>
				</Card>
			</Grid>
	);
}

export default function DrinkCards() {
	const classes = makeStyles({
		root: {
			width: 50,
		},
		title: {
			fontSize: 14,
		},
		pos: {
			marginBottom: 12,
		},
	});

	return (
		<Grid container>
			{["Vodka", "Tequila", "Test1", "Test2", "Test3", "Test4"].map((value) => (
				<DrinkCard name={value}/>
			))}
		</Grid>
 );
}
