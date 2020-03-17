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