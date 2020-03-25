export const surveysInfoFetched = (surveysInfo) => ({
    type: 'FETCH_SURVEYS_INFO_SUCCESS',
    surveysInfo
});

export const algorithmNamesFetched = (algorithmNames) => ({
    type: 'FETCH_ALGORITHM_NAMES_SUCCESS',
    algorithmNames
});

export const surveyStatsFetched = (surveyStats) => ({
    type: 'FETCH_SURVEY_STATISTICS_FETCHED',
    surveyStats
});

export const surveyResultsFetched = (surveyResults) => ({
    type: 'FETCH_SURVEY_RESULTS_FETCHED',
    surveyResults
});

export const surveyBumpsFetched = (surveyBumps) => ({
    type: 'FETCH_SURVEY_BUMPS_FETCHED',
    surveyBumps
});