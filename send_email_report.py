import pandas as pd  
import joblib  
import numpy as np  
import smtplib  
from email.mime.text import MIMEText  
from email.mime.multipart import MIMEMultipart 
import schedule 
import time  
from app.models import User

user = User()

# Load the pre-trained models
clf = joblib.load('random_forest_classifier.joblib')  # Load the classifier model for item type prediction
reg = joblib.load('random_forest_regressor.joblib')  # Load the regressor model for amount prediction

# Define the function to read the test dataset and send the email
def send_email_report():
    # Read the test dataset
    test_data = pd.read_csv('scc-2-main/csv_files/realistic_dataset.csv')  # Replace 'test_dataset.csv' with the actual test dataset path
    
    # Preprocess the test data in the same way as training data
    test_data['timestamp'] = pd.to_datetime(test_data['timestamp'])  # Convert timestamp to datetime
    test_data_encoded = pd.get_dummies(test_data, columns=['item', 'status', 'urgency'], drop_first=True)  # One-hot encode categorical variables
    test_data_encoded['lag_1_amount'] = test_data_encoded['amount'].shift(1)  # Create lag feature
    test_data_encoded['rolling_mean_amount'] = test_data_encoded['amount'].rolling(window=3).mean()  # Create rolling mean feature
    test_data_encoded = test_data_encoded.dropna().reset_index(drop=True)  # Drop NaN values due to shifting and rolling
    
    
    features = [col for col in test_data_encoded.columns if col not in ['id', 'amount', 'hospital_username', 'timestamp']]  # Select feature columns
    
    X_test = test_data_encoded[features]  
    
    
    y_pred_item = clf.predict(X_test)  
    y_pred_amount = reg.predict(X_test)  
    
    
    y_pred_amount = np.round(y_pred_amount).astype(int) 
    
    
    item_columns = [col for col in test_data_encoded.columns if col.startswith('item_')]  
    pred_item_df = pd.DataFrame(y_pred_item, columns=item_columns)  
    predicted_item = pred_item_df.idxmax(axis=1).str.replace('item_', '')  
    
    
    predictions = pd.DataFrame({
        'predicted_item': predicted_item, 
        'predicted_amount': y_pred_amount 
    })
    
    
    email_body = predictions.to_csv(index=False)  
    
    
    sender_email = 'shreyagopal28@gmail.com' 
    password = 'zbvk hgen esgv vdjb'
  
    receiver_email =  User.email 
    
    # Create the email message
    msg = MIMEMultipart()  
    msg['From'] = sender_email  
    msg['To'] = receiver_email  
    msg['Subject'] = 'Daily Order Prediction Report'  
    
    
    msg.attach(MIMEText('Here is the daily order prediction report:\n\n' + email_body, 'plain'))
    
   
    with smtplib.SMTP('smtp.gmail.com', 587) as server:  
        server.starttls()  
        server.login(sender_email, password)  
        server.send_message(msg)  

print("done")

# Schedule the task to run every day at 8:00 AM
schedule.every().day.at("20:33:00").do(send_email_report)  # Schedule the email report function to run at 8:00 AM

print("done ")
# Run the scheduler
while True:
    schedule.run_pending()  # Run any scheduled tasks  # Wait for one second before checking for the next scheduled task
    # time.sleep(1)

print("done")