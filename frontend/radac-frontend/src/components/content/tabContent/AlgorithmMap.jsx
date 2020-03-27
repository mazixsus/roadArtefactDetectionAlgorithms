import React, {useState, useEffect} from "react";
import {Map, GoogleApiWrapper, Marker} from 'google-maps-react'

const mapStyles = {
    margin: '2% 5% 4% 0',
};

const containerStyles = {
    width: '70%',
    height: '80%',
};

function AlgorithmMap({tpb,fpb,ndb, google}) {
    const [truePositiveBumps, setTruePositiveBumps] = useState([]);
    const [falsePositiveBumps, setFalsePositiveBumps] = useState([]);
    const [notDetectedBumps, setNotDetectedBumps] = useState([]);


    // const TruePositiveBumps = bumps.filter((element) => {
    //     element.lat
    // }, detectedBumps);
    // const FalsePositiveBumps;
    // const NotDetectedBumps;

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
            initialCenter={tpb[0]}
        >
            {bumpsMarker("green", tpb)}
            {bumpsMarker("red", fpb)}
            {bumpsMarker("blue", ndb)}
        </Map>
    )
}

export default GoogleApiWrapper({
    // apiKey: process.env.REACT_APP_API_KEY,
})(AlgorithmMap)