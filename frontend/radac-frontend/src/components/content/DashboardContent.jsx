import React, {useEffect, useState} from "react";
import Tabs from "@material-ui/core/Tabs";
import Tab from "@material-ui/core/Tab";
import AlgorithmTabContent from "./AlgorithmTabContent";
import {
    algorithmNamesFetched,
    selectSurvey,
    surveyBumpsFetched,
    surveyResultsFetched,
    surveyStatsFetched
} from "../../redux/actions";
import {connect} from "react-redux";
import Typography from "@material-ui/core/Typography";

function DashboardContent(props) {
    const [value, setValue] = useState(0);
    const [isAlgorithmNamesLoaded, setIsAlgorithmNamesLoaded] = useState(false);
    const [isSurveyStatsLoaded, setIsSurveyStatsLoaded] = useState(false);
    const [isSurveyResultsLoaded, setIsSurveyResultsLoaded] = useState(false);
    const [isSurveyBumpsLoaded, setIsSurveyBumpsLoaded] = useState(false);

    //TODO ogarnąć wysyłanie błędnych requestów
    //fetching algorithm names
    useEffect(() => {
            if (!isAlgorithmNamesLoaded && props.selectedSurvey !== null) {
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
            if (!isSurveyStatsLoaded && props.selectedSurvey !== null) {
                fetch("/survey/statistics?surveyId=" + props.selectedSurvey)
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
        if (!isSurveyResultsLoaded && props.selectedSurvey !== null) {
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
        if (!isSurveyBumpsLoaded && props.selectedSurvey !== null) {
            fetch("/survey/bumps?surveyId=" + props.selectedSurvey)
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
            {!props.selectedSurvey
                //TODO better looking component
                ? <Typography component={"h2"} variant={"h6"} noWrap>
                    Wybierz lub wyślij plik z pomiarami
                </Typography>
                :
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
            }
        </div>
    )
}

const mapStateToProps = (state) => {
    return {
        algorithmNames: state.algorithmNames,
        surveyStats: state.surveyStats,
        surveyResults: state.surveyResults,
        surveyBumps: state.surveyBumps,
        selectedSurvey: state.selectedSurvey
    }
};
const mapDispatchToProps = {
    algorithmNamesFetched,
    surveyStatsFetched,
    surveyResultsFetched,
    surveyBumpsFetched,
    selectSurvey
};

export const DashboardContentContainer = connect(mapStateToProps, mapDispatchToProps)(DashboardContent);