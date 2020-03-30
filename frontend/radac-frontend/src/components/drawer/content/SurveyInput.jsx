import React, {useEffect} from "react";
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";

//TODO wysyłanie plików do API
export default function SurveyInput() {
//     useEffect(() => {
//         const requestOptions = {
//             method: 'POST',
//             headers: { 'Content-Type': 'application/json' },
//             body: JSON.stringify({ title: 'React Hooks POST Request Example' })
//         };
//         fetch('https://jsonplaceholder.typicode.com/posts', requestOptions)
//             .then(response => response.json())
//             .then(data => setPostId(data.id));
//
// // empty dependency array means this effect will only run once (like componentDidMount in classes)
//     }, []);


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
                        accept: ".csv"
                    }}
                    type={"file"}
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
                />
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