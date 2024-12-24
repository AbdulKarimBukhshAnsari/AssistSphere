from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import cv2
import numpy as np
import os
import pickle
from tensorflow.keras.models import load_model
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL
import bcrypt

# Initialize Flask app
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '23sep2004'
app.config['MYSQL_DB'] = 'oncosmart'
mysql = MySQL(app)
# Load your pre-trained model and label encoder
model = load_model('models/CNN_Cancer_tumormodel_Version.h5')  # Replace with your model path
le = pickle.load(open("models/Label_encoder.pkl", 'rb'))  # Load the label encoder

# Path to store uploaded images
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def process_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Image not found at path: {image_path}")
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_resized = cv2.resize(image_rgb, (150, 150))
    image_normalized = image_resized / 255.0
    image_input = np.expand_dims(image_normalized, axis=0)
    predictions = model.predict(image_input)
    predicted_index = np.argmax(predictions)
    confidence_score = predictions[0][predicted_index]
    predicted_label = le.inverse_transform([predicted_index])[0]
    return predicted_label, confidence_score



@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        predicted_label, confidence_score = process_image(file_path)
        return render_template('result.html',
                               image_path=file_path,
                               filename=filename,
                               predicted_label=predicted_label,
                               confidence_score=confidence_score)

@app.route('/camera')
def camera():
    return render_template('camera.html')



@app.route("/")
def home():
    #return render_template('registrationPatient.html')
    return render_template('index.html')


@app.route("/cancer_types")
def cancer_types():
    return render_template("CancerTypes/types.html")

@app.route("/doctor_ai")
def doctor_ai():
    return render_template("doctorai.html")

@app.route("/about_us")
def about_us():
    return render_template("aboutus.html")

@app.route("/donate_us")
def donate_us():
    return render_template("donateus.html")

@app.route("/appointment.html", methods=['GET', 'POST'])
def appointment():
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        patient_id = 3
        full_name = request.form.get('fullName')
        phone_number = request.form.get('phoneNumber')
        email_address = request.form.get('emailAddress')
        appointment_type = request.form.get('appointmentType')
        preferred_date = request.form.get('preferredDate')
        preferred_time = request.form.get('preferredTime')
        current_symptoms = request.form.get('currentSymptoms')
        previous_treatments = request.form.get('previousTreatments')

        sql_query = """
        INSERT INTO appointments ( patient_id,full_name, phone_number, email_address, appointment_type, 
                                   preferred_date, preferred_time, current_symptoms, previous_treatments)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql_query, (patient_id, full_name, phone_number, email_address, appointment_type,
                                   preferred_date, preferred_time, current_symptoms, previous_treatments))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('home')) 
       

    return render_template('appointment.html')

# @app.route("/registrationPatient", methods=['GET', 'POST'])
# def registration_patient():
    
#     cursor = mysql.connection.cursor()
#     full_name = request.form.get('fullName')
#     dob = request.form.get('dob')
#     gender = request.form.get('gender')
#     email = request.form.get('email')
#     phone = request.form.get('phone')
#     address = request.form.get('address')
#     symptoms = request.form.get('symptoms')
#     medical_history = request.form.get('medicalHistory')
#     password = request.form.get('password')

#     # Hash the password
#     password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

#     sql_query = """
#     INSERT INTO patients (full_name, date_of_birth, gender, email_address, phone_number, address, 
#                           symptoms, medical_history, password_hash)
#     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
#     """
#     cursor.execute(sql_query, (full_name, dob, gender, email, phone, address, symptoms, medical_history, password_hash))
#     mysql.connection.commit()
#     cursor.close()
#     return redirect(url_for('home'))
@app.route("/registrationPatient", methods=['GET', 'POST'])
def registration_patient():
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        full_name = request.form.get('fullName')
        dob = request.form.get('dob')
        gender = request.form.get('gender')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        symptoms = request.form.get('symptoms')
        medical_history = request.form.get('medicalHistory')
        password = request.form.get('password')

        # Hash the password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        sql_query = """
        INSERT INTO patients (full_name, date_of_birth, gender, email_address, phone_number, address, 
                              symptoms, medical_history, password_hash)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql_query, (full_name, dob, gender, email, phone, address, symptoms, medical_history, password_hash))
        mysql.connection.commit()
        cursor.close()

        # Redirect to the home page or another page after successful registration
        return redirect(url_for('home'))

    # Render the registration form if the request is GET (when the user first visits the page)
    return render_template('registrationPatient.html')
# @app.route("/patientlogin.html", methods=['POST'])
# def patient_login():
#     cursor = mysql.connection.cursor()
#     email_address = request.form.get('username')
#     password = request.form.get('password')
#     print(email_address)
#     sql_query = "SELECT * FROM patients WHERE email_address = %s"
#     cursor.execute(sql_query, [email_address])
#     user = cursor.fetchone()

#     if user:
#         stored_password_hash = user[-1]  # Assuming the last column is the password hash
#         if bcrypt.checkpw(password.encode('utf-8'), stored_password_hash.encode('utf-8')):
#             patient_id = user[0]  # Assuming the first column is the patient ID
#             return redirect(url_for('appointment'))  # Redirect after successful login
#         else:
#             return render_template('jobseekerwrongsignin.html', error="Invalid password")
#     else:
#         return render_template('jobseekerwrongsignin.html', error="User not found")
@app.route("/patient_login", methods=['GET', 'POST'])
def patient_login():
    if request.method == 'POST':
        # Get the email from the form
        email_address = request.form.get('username')

        # Check the database for the user
        cursor = mysql.connection.cursor()
        sql_query = "SELECT * FROM patients WHERE email_address = %s"
        cursor.execute(sql_query, [email_address])
        user = cursor.fetchone()

        if user:
            # If a user with the email exists, redirect to the appointment page
            return redirect(url_for('appointment'))
        else:
            # If no user is found, return an error message
            return render_template('patientlogin.html', error="User not found")
    else:
        # If the method is GET, render the login page
        return render_template('patientlogin.html')

if __name__ == '__main__':
    app.run(debug=True)