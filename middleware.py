from flask import Flask, request, jsonify
from supabase import create_client, Client

app = Flask(__name__)

# Supabase configuration
url = "https://agxkggapuhoheoislhzk.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFneGtnZ2FwdWhvaGVvaXNsaHprIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzk4ODU0NjUsImV4cCI6MjA1NTQ2MTQ2NX0.Fos8TBPqSkaW0pe6vyL6VF_JJQQuoUeZWtx4lBk6ftI"
supabase: Client = create_client(url, key)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    # Authenticate user with Supabase
    response = supabase.auth.sign_in(email=email, password=password)
    if response.get('error'):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    return jsonify({'message': 'Login successful'}), 200

@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = supabase.from_('vehicles').select('*').execute()
    return jsonify(vehicles.data), 200

@app.route('/book', methods=['POST'])
def book_vehicle():
    data = request.json
    user_id = data.get('user_id')
    vehicle_id = data.get('vehicle_id')
    
    # Book vehicle logic
    supabase.from_('bookings').insert({'user_id': user_id, 'vehicle_id': vehicle_id}).execute()
    return jsonify({'message': 'Vehicle booked successfully'}), 200

@app.route('/return', methods=['POST'])
def return_vehicle():
    data = request.json
    booking_id = data.get('booking_id')
    
    # Return vehicle logic
    supabase.from_('bookings').update({'returned': True}).eq('id', booking_id).execute()
    return jsonify({'message': 'Vehicle returned successfully'}), 200

@app.route('/history/<user_id>', methods=['GET'])
def rental_history(user_id):
    history = supabase.from_('bookings').select('*').eq('user_id', user_id).execute()
    return jsonify(history.data), 200

if __name__ == '__main__':
    app.run(debug=True)