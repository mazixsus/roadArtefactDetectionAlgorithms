import React, {useEffect, useState} from "react";
import Tabs from "@material-ui/core/Tabs";
import Tab from "@material-ui/core/Tab";
import AlgorithmTabContent from "./AlgorithmTabContent";
import {algorithmNamesFetched} from "../../redux/actions";
import {connect} from "react-redux";

export default function DashboardContent(props) {
    const [value, setValue] = useState(0);
    const [isAlgorithmNamesLoaded, setIsAlgorithmNamesLoaded] = useState(false);
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
                {algorithmNames}
            </Tabs>
            {isAlgorithmNamesLoaded &&
                <AlgorithmTabContent stats={algorithmStats} algorithmId={getAlgorithmId()}/>
            }
        </div>
    )
}

const mapStateToProps = (state) => {
    return {
        algorithmNames: state.algorithmNames
    }
};
const mapDispatchToProps = {algorithmNamesFetched};

export const DashboardContentContainer = connect(mapStateToProps, mapDispatchToProps)(DashboardContent);