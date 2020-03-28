import {combineReducers} from "redux";
import {surveysInfo} from "./surveysInfo"
import {algorithmNames} from "./algorithmNames";
import {surveyStats} from "./surveyStats";
import {surveyResults} from "./surveyResults";
import {surveyBumps} from "./surveyBumps";
import {selectedSurvey} from "./selectedSurvey";

export default combineReducers({
    surveysInfo,
    algorithmNames,
    surveyStats,
    surveyResults,
    surveyBumps,
    selectedSurvey
})