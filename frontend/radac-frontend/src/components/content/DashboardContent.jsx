import React, {useEffect, useState} from "react";
import Tabs from "@material-ui/core/Tabs";
import Tab from "@material-ui/core/Tab";
import AlgorithmTabContent, {AlgorithmTabContentContainer} from "./AlgorithmTabContent";
import {algorithmNamesFetched, surveyStatsFetched} from "../../redux/actions";
import {connect} from "react-redux";

export default function DashboardContent(props) {
    const [value, setValue] = useState(0);
    const [isAlgorithmNamesLoaded, setIsAlgorithmNamesLoaded] = useState(false);
    const [isSurveyStatsLoaded, setIsSurveyStatsLoaded] = useState(false);

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
                fetch("/survey/statistics?surveyId="+1)
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

    const algorithmNames = props.algorithmNames.map((element) =>
        <Tab key={element.algorithmId} label={element.algorithmName}/>
    );

    const handleChange = (event, newValue) => {
        setValue(newValue);
    };

    const getAlgorithmId = () =>{
        return props.algorithmNames[value].algorithmId
    };

    const algorithmStats = require("../../resources/statistics");


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
            {isAlgorithmNamesLoaded && isSurveyStatsLoaded  &&
                <AlgorithmTabContent stats={props.surveyStats} algorithmId={getAlgorithmId()}/>
            }
        </div>
    )
}

const mapStateToProps = (state) => {
    return {
        algorithmNames: state.algorithmNames,
        surveyStats: state.surveyStats
    }
};
const mapDispatchToProps = {
    algorithmNamesFetched,
    surveyStatsFetched
};

export const DashboardContentContainer = connect(mapStateToProps, mapDispatchToProps)(DashboardContent);