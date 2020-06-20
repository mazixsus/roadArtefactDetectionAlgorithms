# Frontend application 


# Backend application 

### Requirement to run server application:
- Python (version used in project: 3.7.6)
- Django (version used in project: 3.0.4)
- pandas packages

### How to run:
To run application open in the project folder command console and type "python manage.py runserver 8000".

### Add new algorithm instruction:
1.	- Implementation of algorithm need to be located in algorithms.py script in folder roadArtefactDetection/algorithms_scripts.
	- The function need to return python list with Latitude and Longitude of points.
2. 	- Go to script research_helper.py located in roadArtefactDetection/app_helper_scripts.
	- Add to the global array ALGORITHM_NAMES name of new algorithm. (important)
	- Add to the function get_alg_result call of new algorithm function with pattern:
		alg_number: count_time(algorithms.alg_function_name, first_fun_var, second_var, ... , n_var).
	
### Additional info about algorithms thresholds:
- Z-THRESH - 1.1 - 1.2
- Z-DIFF - 2 - 4
- STDEV- windows/threshold 5/0.18 - 8/0.187
- G-ZERO - 0.75 - 0.8
