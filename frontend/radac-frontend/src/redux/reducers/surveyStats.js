export const surveyStats = (state = [], action) => {
    switch (action.type) {
        case 'FETCH_SURVEY_STATISTICS_SUCCESS':
            return [
                ...action.surveyStats
            ];
        default:
            return state
    }
};