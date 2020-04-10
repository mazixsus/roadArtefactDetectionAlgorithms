import React, {Fragment} from "react";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import Typography from "@material-ui/core/Typography";
import {makeStyles} from "@material-ui/core/styles";

const useStyles = makeStyles(() => ({
        listItem: {
            width: '50%'
        }
    })
);

const tableLabels = ['Precyzja', 'TPR', 'FPR','FNR','Czas'];

export default function AlgorithmStats({stats}) {
    const classes = useStyles();

    //generating statistics list
    const algorithmStats = Object.entries(stats).map((element,index) =>
        <ListItem key={element[0]}>
            <Typography className={classes.listItem} component={"h2"} variant={"h6"} noWrap>
                {tableLabels[index]}
            </Typography>
            <Typography className={classes.listItem} component={"h2"} variant={"h6"} noWrap>
                {element[1]}
            </Typography>
        </ListItem>
    );

    return (
        <Fragment>
            <Typography component={"h2"} variant={"h6"} >Statystyki:</Typography>
            <List>
                {algorithmStats}
            </List>
        </Fragment>
    )
}