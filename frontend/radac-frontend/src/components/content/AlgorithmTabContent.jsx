import React, {useState, useEffect} from "react";
import AlgorithmStats from "./tabContent/AlgorithmStats";
import AlgorithmMap from "./tabContent/AlgorithmMap";
import Grid from "@material-ui/core/Grid";

export default function AlgorithmTabContent({results, bumps, algorithmId}) {
    const [algorithmStats, setAlgorithmStats] = useState([]);
    const [algorithmDetectedBumps, setAlgorithmDetectedBumps] = useState([]);

    //selecting data for current algorithm
    useEffect(() => {
        setAlgorithmStats( results.find((element) => element.algorithmId === algorithmId).stats);
        setAlgorithmDetectedBumps(results.find((element) => element.algorithmId === algorithmId).detectedBumps)
    }, [algorithmId,results]);


    return (
        <Grid
            container
            direction="row"
            justify="center"
            alignItems="stretch"
        >
            <Grid item xs={3}>
                <AlgorithmStats stats={algorithmStats}/>
            </Grid>
            <Grid item xs={9}>
                <AlgorithmMap
                    bumps={bumps}
                    detectedBumps={algorithmDetectedBumps}
                />
            </Grid>

        </Grid>
    )
}
