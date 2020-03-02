import React from "react";
import AlgorithmStats from "./AlgorithmStats";

export default function AlgorithmContent({stats, algorithmId}) {

    const algorithmStats = stats.find((element) => element.id === algorithmId).stats;

    return (
        <div>
            {console.log(algorithmId)}
            {console.log(algorithmStats)}
            <AlgorithmStats stats={algorithmStats}/>
        </div>
    )
}