import React from "react";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import Typography from "@material-ui/core/Typography";
import {makeStyles} from "@material-ui/core/styles";

const useStyles = makeStyles(theme => ({
        root: {
            position: 'relative',
            overflow: 'auto',
            maxHeight: '70vh',
        },
    })
);

export default function SurveyList(props) {
    const classes = useStyles();
    const surveyNames = props.data.map((element) =>
        <ListItem key={element.id} button>
            <Typography component={"h2"} variant={"h6"} noWrap>
                {element.name}
            </Typography>
        </ListItem>
    );


    return (
        <List className={classes.root}>
            {surveyNames}
            {surveyNames}
            {surveyNames}
            {surveyNames}
            {surveyNames}
        </List>
    );
}
