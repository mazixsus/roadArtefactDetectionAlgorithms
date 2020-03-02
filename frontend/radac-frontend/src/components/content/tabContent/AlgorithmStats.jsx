import React from "react";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import Typography from "@material-ui/core/Typography";
import {makeStyles} from "@material-ui/core/styles";

const useStyles = makeStyles(theme => ({
        listItem: {
            width: '50%'
        }
    })
);

export default function AlgorithmStats({stats}) {
    const classes = useStyles();

    const algorithmStats = Object.entries(stats).map((element) =>
        <ListItem key={element[0]}>
            <Typography className={classes.listItem} component={"h2"} variant={"h6"} noWrap>
                {element[0]}
            </Typography>
            <Typography className={classes.listItem} component={"h2"} variant={"h6"} noWrap>
                {element[1]}
            </Typography>
        </ListItem>
    );

    return (
        <List>
            {algorithmStats}
        </List>
    )
}