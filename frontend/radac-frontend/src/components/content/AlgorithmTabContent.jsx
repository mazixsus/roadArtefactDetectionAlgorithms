import React from "react";
import AlgorithmStats from "./tabContent/AlgorithmStats";
import AlgorithmMap from "./tabContent/AlgorithmMap";
import Grid from "@material-ui/core/Grid";
import {makeStyles} from "@material-ui/core/styles";


export default function AlgorithmTabContent({stats, algorithmId}) {
    const algorithmStats = stats.find((element) => element.id === algorithmId).stats;

    return (
        <Grid
            container
            spacing={3}
            direction="row"
            justify="center"
            alignItems="stretch"
        >
            {console.log(algorithmId)}
            {console.log(algorithmStats)}
            <Grid item xs={2}>
                <AlgorithmStats stats={algorithmStats}/>
            </Grid>
            <Grid item xs={10}>
                <AlgorithmMap/>
            </Grid>

        </Grid>
    )
}