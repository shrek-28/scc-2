# Import necessary libraries
import pandas as pd  # For handling data in DataFrame format
import joblib  # For loading pre-trained models
import numpy as np  # For numerical operations
import smtplib  # For sending emails
from email.mime.text import MIMEText  # For creating the text part of the email
from email.mime.multipart import MIMEMultipart  # For creating the complete email message
import schedule  # For scheduling tasks
import time  # For sleeping between scheduled tasks
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
    
    # Prepare the features for prediction
    features = [col for col in test_data_encoded.columns if col not in ['id', 'amount', 'hospital_username', 'timestamp']]  # Select feature columns
    
    X_test = test_data_encoded[features]  # Extract features from the test data
    
    # Predict item type and amount
    y_pred_item = clf.predict(X_test)  # Predict item types
    y_pred_amount = reg.predict(X_test)  # Predict amounts
    
    # Round predicted amounts to the nearest whole number
    y_pred_amount = np.round(y_pred_amount).astype(int)  # Convert predictions to integers
    
    # Combine item predictions into a single column
    item_columns = [col for col in test_data_encoded.columns if col.startswith('item_')]  # List of item columns
    pred_item_df = pd.DataFrame(y_pred_item, columns=item_columns)  # Convert predictions to DataFrame
    predicted_item = pred_item_df.idxmax(axis=1).str.replace('item_', '')  # Get the predicted item names
    
    # Create a DataFrame for predictions
    predictions = pd.DataFrame({
        'predicted_item': predicted_item,  # Predicted item types
        'predicted_amount': y_pred_amount  # Predicted amounts
    })
    
    # Generate the email content
    email_body = predictions.to_csv(index=False)  # Convert predictions DataFrame to CSV format for email body
    
    # Define email parameters
    sender_email = 'shreyagopal28@gmail.com' 
    password = 'zbvk hgen esgv vdjb'
  # Replace with your email address
    receiver_email =  'naman.dsce@gmail.com' # Replace with the hospital's email address
     # Replace with your email account password
    
    # Create the email message
    msg = MIMEMultipart()  # Create a multipart email message
    msg['From'] = sender_email  # Set the sender's email address
    msg['To'] = receiver_email  # Set the recipient's email address
    msg['Subject'] = 'Daily Order Prediction Report'  # Set the subject of the email
    
    # Attach the email body
    msg.attach(MIMEText('Here is the daily order prediction report:\n\n' + email_body, 'plain'))
    
    # Send the email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:  # Connect to the SMTP server (replace with your SMTP server details)
        server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
        server.login(sender_email, password)  # Log in to the SMTP server
        server.send_message(msg)  # Send the email message

print("done")

# Schedule the task to run every day at 8:00 AM
schedule.every().day.at("20:33:00").do(send_email_report)  # Schedule the email report function to run at 8:00 AM

print("done ")
# Run the scheduler
while True:
    schedule.run_pending()  # Run any scheduled tasks  # Wait for one second before checking for the next scheduled task
    # time.sleep(1)

print("done")