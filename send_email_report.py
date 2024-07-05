import pandas as pd
import joblib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.models import User

user = User()

model = joblib.load('finalmodel.joblib')

def send_prediction_email(user_email):
    try:
        test_data = pd.read_csv('csv_files/app.csv')  

       
        required_columns = ['item', 'number_of_items']
        for col in required_columns:
            if col not in test_data.columns:
                raise KeyError(f"Column '{col}' is missing from the DataFrame")

        
        X_test = test_data[['item', 'number_of_items']]

       
        item_dummies = pd.get_dummies(X_test['item'], drop_first=True)
        
        feature_columns = ['item_gloves', 'item_masks', 'item_medicines', 'item_oxygen cylinders', 'item_syringes']
        for col in feature_columns:
            if col not in item_dummies.columns:
                item_dummies[col] = 0
        
        item_dummies = item_dummies[feature_columns]
        
        X_test_processed = pd.concat([item_dummies, X_test[['number_of_items']].reset_index(drop=True)], axis=1)

        predictions = model.predict(X_test_processed)

        prediction_results = pd.DataFrame({
            'item': X_test['item'],
            'predicted_number_of_items': predictions.astype(int)  
        })

        email_body = prediction_results.to_csv(index=False)

        sender_email = 'shreyagopal28@gmail.com'
        password = 'zbvk hgen esgv vdjb'  

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = user_email
        msg['Subject'] = 'Monthly Order Prediction Report'
        msg.attach(MIMEText('Here is the monthly order prediction report:\n\n' + email_body, 'plain'))

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, password)
                server.send_message(msg)
            print(f"Email sent successfully to {user_email}!")
        except Exception as e:
            print(f"Failed to send email to {user_email}. Error: {e}")

    except KeyError as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    send_prediction_email(user.Email)  

