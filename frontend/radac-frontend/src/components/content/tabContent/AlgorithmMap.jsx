import React, {useState, useEffect} from "react";
import {Map, GoogleApiWrapper, Marker} from 'google-maps-react'

const mapStyles = {
    margin: '1% 0 0 0',
};

const containerStyles = {
    width: '70%',
    height: '80%',
};

function AlgorithmMap({bumps, detectedBumps, google}) {
    const [truePositiveBumps, setTruePositiveBumps] = useState([]);
    const [falsePositiveBumps, setFalsePositiveBumps] = useState([]);
    const [notDetectedBumps, setNotDetectedBumps] = useState([]);
    const [isBumpSorted, setIsBumpsSorted] = useState(false);


    //detecting tab switching
    useEffect(() => {
        setIsBumpsSorted(false);
    }, [detectedBumps]);

    useEffect(() => {
        if (!isBumpSorted) {

            //searching for true positive bumps
            const tp = bumps.filter((bump) => {
                return detectedBumps.some((detectedBump) => {
                    return detectedBump.lat === bump.lat && detectedBump.lng === bump.lng;
                })
            });

            setTruePositiveBumps(tp);

            //searching for false positive bumps
            setFalsePositiveBumps(
                detectedBumps.filter((detectedBump) => {
                    return tp.every((tpb) => {
                        return tpb.lat !== detectedBump.lat || tpb.lng !== detectedBump.lng;
                    })
                })
            );

            //searching for not detected bumps
            setNotDetectedBumps(
                bumps.filter((bump) => {
                    return tp.every((tpb) => {
                        return tpb.lat !== bump.lat || tpb.lng !== bump.lng;
                    })
                })
            );

            setIsBumpsSorted(true);
        }
    }, [isBumpSorted, bumps, detectedBumps]);


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
            {isBumpSorted && bumpsMarker("green", truePositiveBumps)}
            {isBumpSorted && bumpsMarker("red", falsePositiveBumps) }
            {isBumpSorted && bumpsMarker("blue", notDetectedBumps)  }
        </Map>
    )
}

export default GoogleApiWrapper({
    // apiKey: process.env.REACT_APP_API_KEY,
})(AlgorithmMap)