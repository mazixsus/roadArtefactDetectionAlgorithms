import React, {useEffect, useState} from "react";
import Tabs from "@material-ui/core/Tabs";
import Tab from "@material-ui/core/Tab";
import AlgorithmTabContent from "./AlgorithmTabContent";
import {algorithmNamesFetched, surveyBumpsFetched, surveyResultsFetched, surveyStatsFetched} from "../../redux/actions";
import {connect} from "react-redux";

export default function DashboardContent(props) {
    const [value, setValue] = useState(0);
    const [isAlgorithmNamesLoaded, setIsAlgorithmNamesLoaded] = useState(false);
    const [isSurveyStatsLoaded, setIsSurveyStatsLoaded] = useState(false);
    const [isSurveyResultsLoaded, setIsSurveyResultsLoaded] = useState(false);
    const [isSurveyBumpsLoaded, setIsSurveyBumpsLoaded] = useState(false);


    //fetching algorithm names
    useEffect(() => {
            if (!isAlgorithmNamesLoaded) {
                fetch("/algorithms/names")
                    .then(res =>
                        res.json()
                    )
                    .then(json => {
                        props.algorithmNamesFetched(json);
                    })
                    .then(() => setIsAlgorithmNamesLoaded(true));
            }
        }
    );

    //fetching survey statistics
    useEffect(() => {
            if (!isSurveyStatsLoaded) {
                //TODO change surveyId to not static
                fetch("/survey/statistics?surveyId=" + 1)
                    .then(res =>
                        res.json()
                    )
                    .then(json => {
                        props.surveyStatsFetched(json);
                    })
                    .then(() => setIsSurveyStatsLoaded(true));
            }
        }
    );

    //fetching survey results
    useEffect(() => {
        if (!isSurveyResultsLoaded) {
            //TODO change surveyId to not static
            fetch("/survey/results?surveyId=" + 1)
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
        if (!isSurveyBumpsLoaded) {
            //TODO change surveyId to not static
            fetch("/survey/bumps?surveyId=" + 1)
                .then(res =>
                    res.json()
                )
                .then(json => {
                    props.surveyBumpsFetched(json);
                })
                .then(() => setIsSurveyBumpsLoaded(true));
        }
    });

    const algorithmNames = props.algorithmNames.map((element) =>
        <Tab key={element.algorithmId} label={element.algorithmName}/>
    );

    const handleChange = (event, newValue) => {
        setValue(newValue);
    };

    const getAlgorithmId = () => {
        return props.algorithmNames[value].algorithmId
    };

    const isTabContentDataLoaded = () => {
        return isAlgorithmNamesLoaded &&
            isSurveyStatsLoaded &&
            isSurveyResultsLoaded &&
            isSurveyBumpsLoaded;
    };

    return (
        <div>
            <Tabs
                value={value}
                onChange={handleChange}
                variant="scrollable"
                scrollButtons="auto"
                aria-label="algorithm names"
            >
                {isAlgorithmNamesLoaded && algorithmNames}
            </Tabs>
            {isTabContentDataLoaded() &&
            <AlgorithmTabContent
                stats={props.surveyStats}
                detectedBumps={props.surveyResults}
                bumps={props.surveyBumps}
                algorithmId={getAlgorithmId()}
            />
            }
        </div>
    )
}

const mapStateToProps = (state) => {
    return {
        algorithmNames: state.algorithmNames,
        surveyStats: state.surveyStats,
        surveyResults: state.surveyResults,
        surveyBumps: state.surveyBumps
    }
};
const mapDispatchToProps = {
    algorithmNamesFetched,
    surveyStatsFetched,
    surveyResultsFetched,
    surveyBumpsFetched
};

export const DashboardContentContainer = connect(mapStateToProps, mapDispatchToProps)(DashboardContent);