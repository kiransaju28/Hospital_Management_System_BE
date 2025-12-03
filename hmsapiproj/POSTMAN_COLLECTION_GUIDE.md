POSTMAN API COMMANDS (ADMINS → DOCTOR → RECEPTION → LABTEC → PHARMACIST)

-------------------------------------------------
1. ADMIN AUTHENTICATION
-------------------------------------------------
POST /api/token/
{ "username": "admin", "password": "admin123" }

POST /api/token/refresh/
{ "refresh": "<refresh_token>" }

-------------------------------------------------
2. ADMIN CREATE USER
-------------------------------------------------
POST /api/admins/register-user/
{
  "username": "doc1",
  "password": "pass123",
  "role": "Doctor",
  "full_name": "Dr John",
  "gender": "Male",
  "joining_date": "2024-02-01",
  "mobile_number": "9876543210",
  "consultation_fee": 500,
  "designation": "Physician",
  "availability": "Mon-Fri",
  "specialization": 1
}

-------------------------------------------------
3. ADMIN LIST STAFF
-------------------------------------------------
GET /api/admins/staff/

-------------------------------------------------
4. ADMIN LIST DOCTORS
-------------------------------------------------
GET /api/admins/doctors/

-------------------------------------------------
5. ADMIN LAB TEST CATEGORIES
-------------------------------------------------
GET /api/admins/manage-lab-tests/
POST /api/admins/manage-lab-tests/

-------------------------------------------------
6. ADMIN LAB PARAMETERS
-------------------------------------------------
GET /api/admins/manage-lab-parameters/
POST /api/admins/manage-lab-parameters/

-------------------------------------------------
7. RECEPTION CREATE PATIENT
-------------------------------------------------
POST /api/receptionist/patients/
{
  "patient_name": "John Doe",
  "email": "john@mail.com",
  "date_of_birth": "1995-05-20",
  "blood_group": "A+",
  "gender": "Male",
  "address": "Test address",
  "phone": "9999999999"
}

-------------------------------------------------
8. RECEPTION CREATE APPOINTMENT
-------------------------------------------------
POST /api/receptionist/appointments/
{
  "patient": 1,
  "doctor": 1
}

-------------------------------------------------
9. RECEPTION GENERATE BILL
-------------------------------------------------
POST /api/receptionist/bills/
{ "appointment": 1 }

-------------------------------------------------
10. DOCTOR VIEW TODAY APPOINTMENTS
-------------------------------------------------
GET /api/doctor/today-appointments/

-------------------------------------------------
11. DOCTOR ENTER VITALS
-------------------------------------------------
POST /api/doctor/basic-vitals/
{
  "appointment": 1,
  "height": 170,
  "weight": 65,
  "blood_pressure": "120/80",
  "blood_sugar": 90
}

-------------------------------------------------
12. DOCTOR CREATE CONSULTATION
-------------------------------------------------
POST /api/doctor/consultations/
{
  "appointment": 1,
  "vitals": 1,
  "symptoms": "Fever",
  "diagnosis": "Viral",
  "notes": "Rest"
}

-------------------------------------------------
13. DOCTOR ADD PRESCRIPTION
-------------------------------------------------
POST /api/doctor/prescription-items/
{
  "consultation": 1,
  "medicine": 1,
  "dosage": "500mg",
  "frequency": "1-0-1",
  "duration": "5 days"
}

-------------------------------------------------
14. DOCTOR ORDER LAB TESTS
-------------------------------------------------
POST /api/doctor/lab-test-orders/
{
  "consultation": 1,
  "test": 1
}

-------------------------------------------------
15. LABTEC VIEW PENDING TESTS
-------------------------------------------------
GET /api/labtec/pending-tests/

-------------------------------------------------
16. LABTEC CREATE LAB REPORT
-------------------------------------------------
POST /api/labtec/lab-reports/
{
  "order": 1,
  "category": 1,
  "remarks": "Normal"
}

-------------------------------------------------
17. LABTEC ADD TEST RESULT
-------------------------------------------------
POST /api/labtec/lab-report-results/
{
  "report": 1,
  "parameter": 1,
  "value": "5.6"
}

-------------------------------------------------
18. LABTEC CREATE BILL
-------------------------------------------------
POST /api/labtec/lab-bills/
{
  "patient": 1,
  "items": [
    { "test": 1, "price": 300, "subtotal": 300 }
  ]
}

-------------------------------------------------
19. PHARMACIST GET MEDICINES
-------------------------------------------------
GET /api/pharmacist/medicines/

-------------------------------------------------
20. PHARMACIST CREATE BILL
-------------------------------------------------
POST /api/pharmacist/bills/
{
  "patient": 1,
  "items": [
    { "medicine": 1, "quantity": 2 }
  ]
}
