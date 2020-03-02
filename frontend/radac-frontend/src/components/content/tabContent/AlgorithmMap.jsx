import React from "react";

export default function AlgorithmMap({bumps}) {

    const mapImage = require("../../../resources/map.png");

    return (
        <div>
            <img
            style={{
                maxWidth: '100%',
                maxHeight: '100%'
            }}
                src={mapImage} alt="mapa google" />
        </div>
    )
}