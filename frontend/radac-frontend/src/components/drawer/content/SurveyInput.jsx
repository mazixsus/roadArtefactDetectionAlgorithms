import React, {useEffect, useState} from "react";
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button";
import {makeStyles} from "@material-ui/core/styles";

const useStyles = makeStyles(() => ({
    root: {
        marginTop: '2%',
    },
    input: {
        margin: '5px 1%',
        width: '98%'
    },
    button: {
        width: '50%',
        margin: '5px 25%'
    }
}));

export default function SurveyInput(props) {
    const classes = useStyles();

    const [surveyFile, setSurveyFile] = useState(null);
    const [surveyFileError, setSurveyFileError] = useState(false);

    const [bumpsFile, setBumpsFile] = useState(null);
    const [bumpsFileError, setBumpsFileError] = useState(false);


    const addSurveyFile = event => {
        setSurveyFile(event.target.files[0])
    };
    const addBumpsFile = event => {
        setBumpsFile(event.target.files[0])
    };

    useEffect(() => {
        if (surveyFile !== null)
            setSurveyFileError(false);

        if (bumpsFile !== null)
            setBumpsFileError(false);

    }, [surveyFile, bumpsFile]);

    const validation = () => {
        let correct = true;
        if (surveyFile === null) {
            setSurveyFileError(true);
            correct = false;
        }
        if (bumpsFile === null) {
            setBumpsFileError(true);
            correct = false;
        }

        return correct;
    };

    //sending file
    const handleButtonClick = () => {
        if (validation()) {
            const data = new FormData();

            data.append('surveyFile', surveyFile);
            data.append('bumpsFile', bumpsFile);

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
                    props.selectSurvey(json.surveyId);
                    props.closeDrawer()
                })
        }
    };


    return (
        <div
            className={classes.root}
        >
            <TextField
                error={surveyFileError}
                className={classes.input}
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
            <TextField
                error={bumpsFileError}
                className={classes.input}
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
            <Button
                className={classes.button}
                variant="outlined"
                onClick={handleButtonClick}
            >
                Dodaj
            </Button>
        </div>
    )
}
