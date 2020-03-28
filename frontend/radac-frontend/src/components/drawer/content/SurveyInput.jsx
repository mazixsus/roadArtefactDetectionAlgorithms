import React from "react";
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";

//TODO wysyłanie plików do API
export default function SurveyInput() {
    return (
        <Grid
            container
            direction="row"
            justify="center"
            alignItems="center"
        >
            <Grid item xs={12}>
                <TextField label="Plik z pomiarami" variant="outlined"/>
            </Grid>
            <Grid item xs={12}>
                <TextField label="Plik z lokalizacją progów" variant="outlined"/>
            </Grid>
            <Grid item xs={12}>
                <Button
                    variant="outlined"
                >
                    Dodaj
                </Button>
            </Grid>
        </Grid>
    )
}