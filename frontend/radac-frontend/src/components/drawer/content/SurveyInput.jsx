import React, {useState} from "react";
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";
import {selectSurvey} from "../../../redux/actions";
import {connect} from "react-redux";

function SurveyInput(props) {
    const [surveyFile, setSurveyFile] = useState();
    const [bumpsFile, setBumpsFile] = useState();


    const addSurveyFile = event => {
        setSurveyFile(event.target.files[0])
    };
    const addBumpsFile = event => {
        setBumpsFile(event.target.files[0])
    };
    const handleButtonClick = () => {
        const data = new FormData();
        data.append('surveyFile', surveyFile);
        data.append('bumpsFile',bumpsFile);
        const requestOptions = {
            method: 'POST',
            headers: {'Content-type': 'text/csv'},
            body: data
        };
        fetch('/survey/add', requestOptions)
            .then(res =>
                res.json()
            )
            .then(json => {
                props.selectSurvey(json.surveyId)
            })

    };


    return (
        <Grid
            container
            direction="row"
            justify="center"
            alignItems="center"
            spacing={2}
            style={{
                marginTop: '10px'
            }}
        >

            <Grid item xs={12}>
                <TextField
                    label="Plik z pomiarami"
                    variant="outlined"
                    InputLabelProps={{
                        shrink: true
                    }}
                    InputProps={{
                        readOnly: true,
                    }}
                    inputProps={{
                        accept: ".csv",
                    }}
                    type={"file"}
                    onChange={addSurveyFile}
                />
            </Grid>
            <Grid item xs={12}>
                <TextField
                    label="Plik z lokalizacją progów"
                    variant="outlined"
                    InputLabelProps={{
                        shrink: true
                    }}
                    InputProps={{
                        readOnly: true,
                    }}
                    inputProps={{
                        accept: ".csv"
                    }}
                    type={"file"}
                    onChange={addBumpsFile}
                />
            </Grid>
            <Grid item xs={12}>
                <Button
                    variant="outlined"
                    onClick={handleButtonClick}
                >
                    Dodaj
                </Button>
            </Grid>
        </Grid>
    )
}

const mapStateToProps = (state) => {
    return {
        selectedSurvey: state.selectedSurvey
    }
};
const mapDispatchToProps = {
    selectSurvey
};

export const SurveyInputContainer = connect(mapStateToProps, mapDispatchToProps)(SurveyInput);

