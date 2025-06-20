import sqlite3

conn = sqlite3.connect('../db/users.db')
c = conn.cursor()

# Drop existing table
# Create table if it doesn't exist
c.execute('DROP TABLE IF EXISTS users')



# Create table
c.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    issue TEXT,
    language TEXT
)
''')

# 50 Sample users
users = [
    ('Mani', 22, 'loneliness', 'english'),
    ('Ravi', 24, 'stress', 'telugu'),
    ('Meera', 19, 'overthinking', 'tamil'),
    ('Aarav', 21, 'exam pressure', 'hindi'),
    ('Priya', 23, 'sleep issues', 'english'),
    ('Ananya', 20, 'anxiety', 'telugu'),
    ('Kiran', 25, 'self-doubt', 'english'),
    ('Divya', 22, 'relationship issues', 'hindi'),
    ('Sanjay', 27, 'depression', 'tamil'),
    ('Aarti', 19, 'anger issues', 'english'),
    ('Vikram', 26, 'exam pressure', 'marathi'),
    ('Neha', 23, 'stress', 'kannada'),
    ('Arjun', 21, 'overthinking', 'telugu'),
    ('Sneha', 20, 'sleep issues', 'english'),
    ('Rahul', 28, 'loneliness', 'english'),
    ('Ritika', 19, 'anxiety', 'hindi'),
    ('Manoj', 25, 'depression', 'tamil'),
    ('Sara', 22, 'self-doubt', 'english'),
    ('Aman', 24, 'relationship issues', 'punjabi'),
    ('Tanya', 21, 'overthinking', 'english'),
    ('Nikhil', 26, 'stress', 'telugu'),
    ('Lavanya', 20, 'exam pressure', 'tamil'),
    ('Varun', 22, 'anger issues', 'english'),
    ('Keerthi', 23, 'sleep issues', 'hindi'),
    ('Ajay', 28, 'loneliness', 'english'),
    ('Isha', 19, 'self-doubt', 'telugu'),
    ('Sathvik', 24, 'depression', 'english'),
    ('Harika', 21, 'anxiety', 'tamil'),
    ('Rohit', 25, 'relationship issues', 'english'),
    ('Jaya', 23, 'overthinking', 'marathi'),
    ('Kavya', 20, 'exam pressure', 'english'),
    ('Sandeep', 27, 'stress', 'kannada'),
    ('Bhavya', 21, 'anger issues', 'telugu'),
    ('Teja', 26, 'sleep issues', 'hindi'),
    ('Rani', 22, 'loneliness', 'english'),
    ('Vamsi', 24, 'self-doubt', 'english'),
    ('Nisha', 20, 'relationship issues', 'punjabi'),
    ('Yash', 25, 'anxiety', 'english'),
    ('Lakshmi', 23, 'exam pressure', 'hindi'),
    ('Mohan', 21, 'overthinking', 'english'),
    ('Simran', 22, 'depression', 'tamil'),
    ('Kunal', 26, 'sleep issues', 'english'),
    ('Shreya', 19, 'loneliness', 'telugu'),
    ('Dhruv', 24, 'self-doubt', 'english'),
    ('Pallavi', 23, 'stress', 'hindi'),
    ('Sameer', 20, 'relationship issues', 'english'),
    ('Tanvi', 22, 'exam pressure', 'marathi'),
    ('Naveen', 27, 'depression', 'english'),
    ('Irfan', 25, 'overthinking', 'urdu'),
    ('Rekha', 19, 'anxiety', 'english'),
    ('Pranav', 28, 'anger issues', 'kannada'),
]

c.executemany('INSERT INTO users (name, age, issue, language) VALUES (?, ?, ?, ?)', users)

conn.commit()
conn.close()
print("✅ 50 users inserted successfully. Database setup complete.")
