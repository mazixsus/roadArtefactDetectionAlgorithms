import React, {Fragment} from 'react'
import IconButton from "@material-ui/core/IconButton";
import ChevronLeftIcon from "@material-ui/icons/ChevronLeft";
import {SurveyListContainer} from "./content/SurveyList";
import SurveyInput from "./content/SurveyInput";
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles(theme => ({
    toolbarIcon: {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'flex-end',
        padding: '0 8px',
        ...theme.mixins.toolbar,
    },
}));

export default function DrawerContent(props) {
    const classes = useStyles();
    const handleDrawerClose = () => {
        props.onClick();
    };


    return (
        <Fragment>
            <div className={classes.toolbarIcon}>
                <IconButton onClick={handleDrawerClose}>
                    <ChevronLeftIcon/>
                </IconButton>
            </div>
            <SurveyListContainer/>
            <SurveyInput/>
        </Fragment>
    )
}