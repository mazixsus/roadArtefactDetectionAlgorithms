import {combineReducers} from "redux";
import {surveysInfo} from "./surveysInfo"
import {algorithmNames} from "./algorithmNames";
import {surveyStats} from "./surveyStats";

export default combineReducers({
    surveysInfo,
    algorithmNames,
    surveyStats
})