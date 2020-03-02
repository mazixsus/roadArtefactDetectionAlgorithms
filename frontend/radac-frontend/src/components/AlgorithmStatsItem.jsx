import ListItem from "@material-ui/core/ListItem";
import Typography from "@material-ui/core/Typography";
import List from "@material-ui/core/List";
import React from "react";
import {makeStyles} from "@material-ui/core/styles";

const useStyles = makeStyles(theme => ({
        listItem: {
            width: '50%'
        }
    })
);

export default function AlgorithmStats({stats}) {
    const classes = useStyles();

    const algorithmStats = stats.map((element) =>
        <ListItem key={element.id}>
            <Typography component={"h2"} variant={"h6"} noWrap>
                {element.name}
            </Typography>
            <Typography component={"h2"} variant={"h6"} noWrap>
                {element.name}
            </Typography>
        </ListItem>
    );

    return (
        <List>
            {algorithmStats}
        </List>
    )
}