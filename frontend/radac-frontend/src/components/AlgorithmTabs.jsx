import React from "react";
import Tabs from "@material-ui/core/Tabs";
import Tab from "@material-ui/core/Tab";

export default function AlgorithmTabs({names}) {
    const [value, setValue] = React.useState(0);

    const algorithmNames = names.map((element) =>
        <Tab key={element.id} label={element.name}/>
    );

    const handleChange = (event, newValue) => {
        setValue(newValue);
    };

    return (
        <Tabs
            value={value}
            onChange={handleChange}
            variant="scrollable"
            scrollButtons="auto"
            aria-label="algorithm names"
        >
            {console.log(names)}
            {algorithmNames}
        </Tabs>
    )
}