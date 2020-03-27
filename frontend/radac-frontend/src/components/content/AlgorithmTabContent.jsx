import React, {useState, useEffect} from "react";
import AlgorithmStats from "./tabContent/AlgorithmStats";
import AlgorithmMap from "./tabContent/AlgorithmMap";
import Grid from "@material-ui/core/Grid";
import {makeStyles} from "@material-ui/core/styles";
import {surveysInfoFetched, surveyStatsFetched} from "../../redux/actions";
import {connect} from "react-redux";


export default function AlgorithmTabContent({stats, detectedBumps, bumps, algorithmId}) {
    const algorithmStats = stats.find((element) => element.algorithmId === algorithmId).stats;
    // const algorithmDetectedBumps = detectedBumps.find((element) => element.algorithmId === algorithmId)["detectedBumps"];
    const [algorithmDetectedBumps, setAlgorithmDetectedBumps] = useState([]);
    const [truePositiveBumps, setTruePositiveBumps] = useState([]);
    const [falsePositiveBumps, setFalsePositiveBumps] = useState([]);
    const [notDetectedBumps, setNotDetectedBumps] = useState([]);
    const [isBumpSorted, setIsBumpsSorted] = useState(false);

    useEffect(() => {
        setAlgorithmDetectedBumps(detectedBumps.find((element) => element.algorithmId === algorithmId)["detectedBumps"])
        setIsBumpsSorted(false)
    }, [algorithmId]);

    useEffect(() => {
        if (!isBumpSorted) {
            //searching for true positive bumps
            setTruePositiveBumps(
                bumps.filter((bump) => {
                    return algorithmDetectedBumps.some((detectedBump) => {
                        return detectedBump.lat === bump.lat && detectedBump.lng === bump.lng;
                    })
                })
            );
        }
    });
    useEffect(() => {
        //searching for false positive bumps
        setFalsePositiveBumps(
            algorithmDetectedBumps.filter((detectedBump) => {
                return truePositiveBumps.every((tpb) => {
                    return tpb.lat !== detectedBump.lat || tpb.lng !== detectedBump.lng;
                })
            })
        );

        //searching for not detected bumps
        setNotDetectedBumps(
            bumps.filter((bump) => {
                return truePositiveBumps.every((tpb) => {
                    return tpb.lat !== bump.lat || tpb.lng !== bump.lng;
                })
            })
        );

        setIsBumpsSorted(true);
    }, [truePositiveBumps]);


    return (
        <Grid
            container
            spacing={3}
            direction="row"
            justify="center"
            alignItems="stretch"
        >
            {/*{console.log(algorithmId)}*/}
            {/*{console.log(algorithmStats)}*/}
            {/*{console.log(algorithmDetectedBumps)}*/}
            <Grid item xs={2}>
                <AlgorithmStats stats={algorithmStats}/>
            </Grid>
            <Grid item xs={10}>
                {isBumpSorted &&
                <AlgorithmMap
                    bumps={bumps}
                    detectedBumps={algorithmDetectedBumps}
                    tpb={truePositiveBumps}
                    fpb={falsePositiveBumps}
                    ndb={notDetectedBumps}
                />
                }
            </Grid>

        </Grid>
    )
}
