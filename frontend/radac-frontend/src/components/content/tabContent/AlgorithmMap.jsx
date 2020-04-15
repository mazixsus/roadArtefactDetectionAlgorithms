import React from "react";
import {Map, GoogleApiWrapper, Marker} from 'google-maps-react'

const mapStyles = {
    margin: '1% 0 0 0',
};

const containerStyles = {
    width: '70%',
    height: '80%',
};

function AlgorithmMap({bumps, truePositives, falsePositives, falseNegatives, google}) {

    const bumpsMarker = (color, data) => data.map((element, index) => {
            return (
                <Marker
                    key={index}
                    name={'bump'}
                    position={element}
                    icon={{
                        url: "http://maps.google.com/mapfiles/ms/icons/" + color + "-dot.png",
                    }}/>
            )
        }
    );

    return (
        <Map
            google={google}
            zoom={15}
            style={mapStyles}
            containerStyle={containerStyles}
            initialCenter={bumps[0]}
        >
            {bumpsMarker("green", truePositives)}
            {bumpsMarker("red", falsePositives) }
            {bumpsMarker("blue", falseNegatives)  }
        </Map>
    )
}

export default GoogleApiWrapper({
    // apiKey: process.env.REACT_APP_API_KEY,
})(AlgorithmMap)