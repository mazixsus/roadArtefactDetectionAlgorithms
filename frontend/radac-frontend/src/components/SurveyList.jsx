import React from "react";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";

export default function SurveyList(props) {

    const surveyNames = props.data.map((element) =>
            <ListItem key={element.id} button>{element.name}</ListItem>
        );


    return(
        <List>
            {surveyNames}
        </List>
    );
}
