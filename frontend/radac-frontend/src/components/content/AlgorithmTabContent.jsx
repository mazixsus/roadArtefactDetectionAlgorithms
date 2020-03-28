import React, {useState, useEffect} from "react";
import AlgorithmStats from "./tabContent/AlgorithmStats";
import AlgorithmMap from "./tabContent/AlgorithmMap";
import Grid from "@material-ui/core/Grid";

export default function AlgorithmTabContent({stats, detectedBumps, bumps, algorithmId}) {
    const [algorithmStats, setAlgorithmStats] = useState([]);
    const [algorithmDetectedBumps, setAlgorithmDetectedBumps] = useState([]);

    useEffect(() => {
        setAlgorithmStats( stats.find((element) => element.algorithmId === algorithmId).stats);
        setAlgorithmDetectedBumps(detectedBumps.find((element) => element.algorithmId === algorithmId)["detectedBumps"])
    }, [algorithmId]);


    return (
        <Grid
            container
            spacing={3}
            direction="row"
            justify="center"
            alignItems="stretch"
        >
            <Grid item xs={2}>
                <AlgorithmStats stats={algorithmStats}/>
            </Grid>
            <Grid item xs={10}>
                <AlgorithmMap
                    bumps={bumps}
                    detectedBumps={algorithmDetectedBumps}
                />
            </Grid>

        </Grid>
    )
}
