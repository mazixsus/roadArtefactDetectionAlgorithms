import React, {useState, useEffect} from "react";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import Typography from "@material-ui/core/Typography";
import {makeStyles, withStyles} from "@material-ui/core/styles";
import {selectSurvey, surveysInfoFetched} from "../../../redux/actions";
import {connect} from "react-redux";


const useStyles = makeStyles(theme => ({
        root: {
            position: 'relative',
            overflow: 'auto',
            maxHeight: '70vh',
        }
    })
);

const StyledListItem = withStyles({
    root: {
        '&$selected': {
            backgroundColor: 'rgb(126,125,129)'
        }
    },
    selected: {}
})(ListItem);

function SurveyList(props) {
    const classes = useStyles();
    const [isSurveysInfoLoaded, setIsSurveysInfoLoaded] = useState(false);
    useEffect(() => {
            if (!isSurveysInfoLoaded) {
                fetch("/survey/names")
                    .then(res =>
                        res.json()
                    )
                    .then(json => {
                        props.surveysInfoFetched(json);
                    })
                    .then(() => setIsSurveysInfoLoaded(true));
            }

        }
    );
    const handleListItemClick = (event, index) => {
        props.selectSurvey(index);
    };

    const surveyNames =
        props.surveysInfo.map((element) =>
            <StyledListItem
                key={element.surveyId}
                button
                selected={props.selectedSurvey === element.surveyId}
                onClick={event => handleListItemClick(event, element.surveyId)}
            >
                <Typography component={"h2"} variant={"h6"} noWrap>
                    {element.fileName}
                </Typography>
            </StyledListItem>
        );


    return (
        <List
            className={classes.root}
        >
            {isSurveysInfoLoaded && surveyNames
            }
        </List>
    );
}

const mapStateToProps = (state) => {
    return {
        surveysInfo: state.surveysInfo,
        selectedSurvey: state.selectedSurvey
    }
};
const mapDispatchToProps = {
    surveysInfoFetched,
    selectSurvey
};

export const SurveyListContainer = connect(mapStateToProps, mapDispatchToProps)(SurveyList);

