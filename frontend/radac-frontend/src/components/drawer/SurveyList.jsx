import React, {useState, useEffect} from "react";
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
    const [isDataLoaded, setIsDataLoaded] = useState(false);
    useEffect(() => {
            if (!isDataLoaded) {
                fetch("/survey/names")
                    .then(res =>
                        res.json()
                    )
                    .then(json => {
                        props.surveysInfoFetched(json);
                    })
                    .then(() => setIsDataLoaded(true));
            }

        }
    );

    const classes = useStyles();
    const surveyNames =
        props.surveysInfo.map((element) =>
            <ListItem key={element.surveyId} button>
                <Typography component={"h2"} variant={"h6"} noWrap>
                    {element.fileName}
                </Typography>
            </ListItem>
        );


    return (
        <List
            className={classes.root}
        >
            {isDataLoaded && surveyNames
            }
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

