import React,{useState, useEffect} from "react";
import AlgorithmStats from "./tabContent/AlgorithmStats";
import AlgorithmMap from "./tabContent/AlgorithmMap";
import Grid from "@material-ui/core/Grid";
import {makeStyles} from "@material-ui/core/styles";
import {surveysInfoFetched, surveyStatsFetched} from "../../redux/actions";
import {connect} from "react-redux";


export default function AlgorithmTabContent({stats, algorithmId}) {
    const algorithmStats = stats.find((element) => element.algorithmId === algorithmId).stats;



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
            <Grid item xs={2}>
                <AlgorithmStats stats={algorithmStats}/>
            </Grid>
            <Grid item xs={10}>
                <AlgorithmMap/>
            </Grid>

        </Grid>
    )
}
