import React, {useEffect} from "react";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import Typography from "@material-ui/core/Typography";
import {makeStyles} from "@material-ui/core/styles";
import {surveysInfoFetched} from "../../redux/actions";
import {connect} from "react-redux";

const useStyles = makeStyles(theme => ({
        root: {
            position: 'relative',
            overflow: 'auto',
            maxHeight: '70vh'
        },
    })
);

export default function SurveyList(props) {
    useEffect(() => {
            fetch("/survey/names")
                .then(res =>
                    res.json()
                )
                .then(json => {
                    props.surveysInfoFetched(json)
                });
        }
    );

    const classes = useStyles();
    const surveyNames = props.surveysInfo.map((element) =>
        <ListItem key={element.surveyId} button>
            <Typography component={"h2"} variant={"h6"} noWrap>
                {element.filename}
            </Typography>
        </ListItem>
    );


    return (
        <List
            className={classes.root}
        >
            {surveyNames}
            {surveyNames}
            {surveyNames}
            {surveyNames}
            {surveyNames}
        </List>
    );
}

const mapStateToProps = (state) => {
    return {
        surveysInfo: state.surveysInfo
    }
};
const mapDispatchToProps = {surveysInfoFetched};

export const SurveyListContainer = connect(mapStateToProps, mapDispatchToProps)(SurveyList);

