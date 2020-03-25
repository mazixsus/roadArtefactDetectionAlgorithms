import React from "react";
import {Map, GoogleApiWrapper, Marker} from 'google-maps-react'

const mapStyles = {
    margin: '2% 5% 4% 0',
};

const containerStyles = {
    width: '70%',
    height: '80%',
};

function AlgorithmMap({bumps,google}) {

    const bumpsMarker = bumps.map((element,index) =>
        <Marker
            key={index}
            name={'bump'}
            position={element}
            icon={{
                url: "http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
            }}/>
    );

    return (
        <Map
            google={google}
            zoom={15}
            style={mapStyles}
            containerStyle={containerStyles}
            initialCenter={bumps[0]}
        >
            {bumpsMarker}
        </Map>
    )
}

export default GoogleApiWrapper({
    // apiKey: process.env.REACT_APP_API_KEY,
})(AlgorithmMap)