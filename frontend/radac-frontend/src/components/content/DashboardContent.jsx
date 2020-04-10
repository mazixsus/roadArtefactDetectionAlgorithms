import React, {Fragment, useEffect, useState} from "react";
import Tabs from "@material-ui/core/Tabs";
import Tab from "@material-ui/core/Tab";
import AlgorithmTabContent from "./AlgorithmTabContent";
import {
    algorithmNamesFetched,
    selectSurvey,
    surveyBumpsFetched,
    surveyResultsFetched
} from "../../redux/actions";
import {connect} from "react-redux";
import EmptyContent from "./EmptyContent";
import StyledCircularProgress from "../StyledCircularProgress";

function DashboardContent(props) {
    const [value, setValue] = useState(0);
    const [isSurveyResultsLoaded, setIsSurveyResultsLoaded] = useState(false);
    const [isSurveyResultsLoading, setIsSurveyResultsLoading] = useState(false);
    const [isSurveyBumpsLoaded, setIsSurveyBumpsLoaded] = useState(false);
    const [isSurveyBumpsLoading, setIsSurveyBumpsLoading] = useState(false);


    //fetching survey results
    useEffect(() => {
        if (!isSurveyResultsLoaded && !isSurveyResultsLoading && props.selectedSurvey !== null) {
            setIsSurveyResultsLoading(true);
            fetch("/survey/results?surveyId=" + props.selectedSurvey)
                .then(res =>
                    res.json()
                )
                .then(json => {
                    props.surveyResultsFetched(json);
                })
                .then(() => setIsSurveyResultsLoaded(true));
        }

    });

    //fetching survey bumps
    useEffect(() => {
        if (isSurveyResultsLoaded && !isSurveyBumpsLoaded && !isSurveyBumpsLoading && props.selectedSurvey !== null) {
            setIsSurveyBumpsLoading(true);
            fetch("/survey/bumps?surveyId=" + props.selectedSurvey)
                .then(res =>
                    res.json()
                )
                .then(json => {
                    console.log(json);
                    props.surveyBumpsFetched(json);
                })
                .then(() => setIsSurveyBumpsLoaded(true));
        }
    });

    const algorithmNames = props.surveyResults.map((element) =>
        <Tab key={element.algorithmId} label={element.algorithmName}/>
    );

    //tab changing
    const handleChange = (event, newValue) => {
        setValue(newValue);
    };

    const getAlgorithmId = () => {
        return props.surveyResults[value].algorithmId
    };

    const isTabContentDataLoaded = () => {
        return isSurveyResultsLoaded &&
            isSurveyBumpsLoaded;
    };

    return (
        <Fragment>
            {props.selectedSurvey === null
                ? <EmptyContent/>
                :
                <Fragment>
                    <Tabs
                        value={value}
                        onChange={handleChange}
                        variant="scrollable"
                        scrollButtons="auto"
                        aria-label="algorithm names"
                    >
                        {isSurveyResultsLoaded && algorithmNames}
                    </Tabs>
                    {!isTabContentDataLoaded()
                        ? <StyledCircularProgress/>
                        :
                    <AlgorithmTabContent
                        results={props.surveyResults}
                        bumps={props.surveyBumps}
                        algorithmId={getAlgorithmId()}
                    />
                    }
                </Fragment>
            }
        </Fragment>
    )
}

const mapStateToProps = (state) => {
    return {
        algorithmNames: state.algorithmNames,
        surveyResults: state.surveyResults,
        surveyBumps: state.surveyBumps,
        selectedSurvey: state.selectedSurvey
    }
};
const mapDispatchToProps = {
    algorithmNamesFetched,
    surveyResultsFetched,
    surveyBumpsFetched,
    selectSurvey
};

export const DashboardContentContainer = connect(mapStateToProps, mapDispatchToProps)(DashboardContent);