import React from "react";
import Typography from "@material-ui/core/Typography";
import Paper from "@material-ui/core/Paper";
import makeStyles from "@material-ui/core/styles/makeStyles";

const useStyles = makeStyles(() => ({
    root: {
        width: '50%',
        margin: '25% auto'
    }
}));

export default function EmptyContent() {
    const  classes = useStyles();
    return (
        <Paper elevation={1} className={classes.root}>
            <Typography component={"h2"} variant={"h6"} noWrap>
                Nie wybrano żadnego pomiaru
            </Typography>
        </Paper>
    )

}