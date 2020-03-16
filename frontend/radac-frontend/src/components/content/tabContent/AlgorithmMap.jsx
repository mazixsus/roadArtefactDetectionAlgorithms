import React from "react";
import {Map, GoogleApiWrapper, Marker} from 'google-maps-react'

const mapStyles = {
    margin: '2% 5% 4% 0',
};

const containerStyles = {
    width: '70%',
    height: '80%',
    // boxSizing:'border-box',
    // right: '2%'
};

function AlgorithmMap(props) {
    return (
        <Map
            google={props.google}
            zoom={15}
            style={mapStyles}
            containerStyle={containerStyles}
            initialCenter={{lat: 51.2728665489703, lng: 22.5443017110229}}
        >
            <Marker
                name={'Your position'}
                position={{lat: 51.2728665489703, lng: 22.5443017110229}}
                icon={{
                    url: "http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
                }}/>
        </Map>
    )
}

export default GoogleApiWrapper({
    // apiKey: process.env.REACT_APP_API_KEY,
})(AlgorithmMap)