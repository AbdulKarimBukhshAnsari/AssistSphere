@app.route("/registrationPatient", methods=['GET', 'POST'])
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