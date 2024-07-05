# scc-2
# scc-2
<h1>SmartCareConnect - README</h1>

Project Description

SmartCareConnect is an advanced resource management system designed specifically for hospitals and vendors. This platform provides a comprehensive solution for managing hospital requirements, vendor order management, and delivery tracking. Built with HTML and CSS, the system ensures a seamless and user-friendly interface while maintaining robust functionality.

<h2>Key Features</h2>

1. Hospital Dashboard: Hospitals can efficiently manage their profiles, track past and current orders, and place new orders through an intuitive and easy-to-navigate interface.
   
2. Vendor Dashboard: Vendors can view and manage orders categorized by urgency and distance, ensuring timely delivery and efficient resource management.
   
3. Delivery Management: A dedicated delivery dashboard for tracking and managing the delivery status of orders, ensuring that hospitals receive their supplies promptly.

4. Predictive Analysis Model: A state-of-the-art predictive analysis model forecasts hospitals' next orders based on historical data and sends them email notifications, ensuring that they are always stocked with necessary supplies.

5. Responsive Design: The platform is fully responsive, ensuring a consistent user experience across different devices and screen sizes.

6. Enhanced UI/UX: Utilizing Tailwind CSS, the platform provides a modern and visually appealing user interface with features like hover effects and custom scrollbars for better navigation.

7. Fetch Map API: Integration with a map API to find and display the distance between two locations, aiding in efficient delivery planning and resource allocation.
Setup and Installation

<h2>To set up and run the SmartCareConnect project locally, follow these steps:</h2>

Clone the repository:

```git clone https://github.com/your-username/smartcareconnect.git```

Navigate to the project directory:

```cd smartcareconnect```

Create a virtual environment:

```python -m venv env```
Activate the virtual environment:

On Windows:

```.\env\Scripts\activate```

On macOS/Linux:

```source env/bin/activate```

Install the necessary dependencies:

```pip install -r requirements.txt```

Set up the database:

```flask db init```
```flask db migrate```
```flask db upgrade```

Run the application:

```flask run```

<h2>Usage:</h2>

<h3>Hospital Dashboard</h3>

Profile Management: View and update hospital profile information.
Order Tracking: View past and current orders with detailed information.
Place New Orders: Easily place new orders by filling out the required information.

<h3>Vendor Dashboard</h3>

Order Management: View and manage pending orders categorized by urgency and distance.
Checkout for Delivery: Mark orders as ready for delivery.

<h3>Delivery Dashboard</h3>

Delivery Tracking: Track the status of deliveries in real-time.
Mark as Delivered: Update the status of orders once they are delivered.

<h3>Predictive Analysis Model</h3>

Forecasting: Predict the hospitals' next orders based on historical data.
Email Notifications: Automatically send email notifications to hospitals with predicted order details.

<h3>Fetch Map API</h3>

Distance Calculation: Find and display the distance between two locations using the integrated map API.
Efficient Planning: Utilize distance data to plan deliveries and allocate resources efficiently.

<h2>Acknowledgements</h2>

Thanks to all contributors and users for their support and feedback.
