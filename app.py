# Importing essential libraries
from flask import Flask, render_template, request
import pickle
import numpy as np

# Load the Ridge Regression Classifier model
filename = 'ipl_score_predict_model.pkl'# change the model type to see lil changes in prediction
reg = pickle.load(open(filename, 'rb'))

app = Flask(__name__)
app.static_folder = 'static'

# default route using / method to home
@app.route('/')
def home():
	return render_template('index.html')

# route to predict - /predict
@app.route('/predict', methods=['POST'])
def predict():
    temp_array = list() # creating epty list
    
    if request.method == 'POST':
        # getting user inputs
        batting_team = request.form['batting-team']
        
        # one - hot encoding - batting_team
        if batting_team == 'Chennai Super Kings':
            temp_array = temp_array + [1,0,0,0,0,0,0,0]
        elif batting_team == 'Delhi Daredevils':
            temp_array = temp_array + [0,1,0,0,0,0,0,0]
        elif batting_team == 'Kings XI Punjab':
            temp_array = temp_array + [0,0,1,0,0,0,0,0]
        elif batting_team == 'Kolkata Knight Riders':
            temp_array = temp_array + [0,0,0,1,0,0,0,0]
        elif batting_team == 'Mumbai Indians':
            temp_array = temp_array + [0,0,0,0,1,0,0,0]
        elif batting_team == 'Rajasthan Royals':
            temp_array = temp_array + [0,0,0,0,0,1,0,0]
        elif batting_team == 'Royal Challengers Bangalore':
            temp_array = temp_array + [0,0,0,0,0,0,1,0]
        elif batting_team == 'Sunrisers Hyderabad':
            temp_array = temp_array + [0,0,0,0,0,0,0,1]
            
        # one - hot encoding - bowling_team    
        bowling_team = request.form['bowling-team']
        if bowling_team == 'Chennai Super Kings':
            temp_array = temp_array + [1,0,0,0,0,0,0,0]
        elif bowling_team == 'Delhi Daredevils':
            temp_array = temp_array + [0,1,0,0,0,0,0,0]
        elif bowling_team == 'Kings XI Punjab':
            temp_array = temp_array + [0,0,1,0,0,0,0,0]
        elif bowling_team == 'Kolkata Knight Riders':
            temp_array = temp_array + [0,0,0,1,0,0,0,0]
        elif bowling_team == 'Mumbai Indians':
            temp_array = temp_array + [0,0,0,0,1,0,0,0]
        elif bowling_team == 'Rajasthan Royals':
            temp_array = temp_array + [0,0,0,0,0,1,0,0]
        elif bowling_team == 'Royal Challengers Bangalore':
            temp_array = temp_array + [0,0,0,0,0,0,1,0]
        elif bowling_team == 'Sunrisers Hyderabad':
            temp_array = temp_array + [0,0,0,0,0,0,0,1]
            
        # get overs and other required fields inputs    
        overs = float(request.form['overs'])
        runs = int(request.form['runs'])
        wickets = int(request.form['wickets'])
        runs_in_prev_5 = int(request.form['runs_in_prev_5'])
        wickets_in_prev_5 = int(request.form['wickets_in_prev_5'])
        
        # adding the rest to one got encoded list
        temp_array = temp_array + [overs, runs, wickets, runs_in_prev_5, wickets_in_prev_5]
        
        # converting list to array
        data = np.array([temp_array])
        
        # predicting
        my_prediction = int(reg.predict(data)[0])
        
        # returning output text      
        return render_template('result.html', lower_limit = my_prediction-5, upper_limit = my_prediction+5)


# default run
if __name__ == '__main__':
	app.run(debug=True)