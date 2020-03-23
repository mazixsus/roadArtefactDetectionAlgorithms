import {combineReducers} from "redux";
import {surveysInfo} from "./surveysInfo"
import {algorithmNames} from "./algorithmNames";
import {surveyStats} from "./surveyStats";
import {surveyResults} from "./surveyResults";

export default combineReducers({
    surveysInfo,
    algorithmNames,
    surveyStats,
    surveyResults
})