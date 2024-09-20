Description:
The library management app allows users to read e-books. The librarian is the admin. They are 
responsible for adding sections and books and for approving, rejecting or terminating user 
requests. The users can see a list of all the books available, request them and if approved, can get 
access to the PDF version of these books, online. Both user and librarian can use the search 
function to see what is available in the library.
Technology Used:
  1. Flask: For API
  2. JWT Security: For authorization and authentication
  3. CORS: Used to authorize resources shared with external third parties
  4. VueJS: JavaScript library for building UIs
  5. SQLite: Database for storing application data
  6. Redis: Caching
  7. Celery: Background jobs
  8. Bootstrap: Framework for styling UIs
DB Schema Design:
  1. User:
    a. id (Primary Key, Integer)
    b. username (String, max length 150, unique, not null)
    c. password (String, max length 256, not null)
    d. role (String, max length 100, not null)
    e. email (String, max length 256, not null)
    f. last_login (DateTime)
  2. Sections:
    a. id (Primary Key, Integer)
    b. name (String, max length 256, unique, not null)
    c. date_created (DateTime)
    d. description (String, max length 256)
  3. Book:
    a. id (Primary Key, Integer)
    b. name (String, max length 100)
    c. author (String, max length 256)
    d. section_id (Integer, Foreign key Sections id)
    e. description (String, max length 256)
    f. section (String, max length 256)
    g. pdf (String, max length 512)
  4. Requests:
    a. id (Primary key, Integer)
    b. requested_user (Integer, Foreign key User id)
    c. requested_book (Integer, Foreign key Book id)
    d. user (String, max length 256)
    e. book (String, max length 256)
    f. approved (Boolean)
  5. Issued:
    a. id (Primary Key, Integer)
    b. requested_id (Integer, Foreign key Request id)
    c. issued_user (Integer, Foreign key User id)
    d. issued_book (Integer, Foreign key Book id)
    e. date_returned (DateTime)
    f. book (String, max length 256)
    g. author (String, max length 256)
    h. description (String, max length 256)
    i. pdf (String, max length 512)
  6. Feedback:
    a. id (Primary Key, Integer)
    b. user_id (Integer, Foreign key User id)
    c. book_id (Integer, Foreign key Book id)
    d. issue_id (Integer, Foreign key Issued id)
    e. feedback (String, max length 256)
  7. Read:
    a. id (Integer, Primary key)
    b. book_id (Integer, Foreign key Book id)
    c. user_id (Integer, Foreign key User id)
    d. timestamp (DateTime)
API Designs
  1. CRUD for Sections
  2. CRUD for Books
  3. Validation of input fields
  4. Backend validation
Architecture
There are 3 Python files;
  1. app.py
  2. celery_config.py
  3. tasks.py

Screenshots:

![Screenshot (8)](https://github.com/user-attachments/assets/0ffed665-968e-41bc-9e87-991caf719ec2)

![Screenshot (10)](https://github.com/user-attachments/assets/a7bf9ec2-59d9-4bdc-ba1e-9eae779aebd7)

![Screenshot (12)](https://github.com/user-attachments/assets/9ba5e408-9245-4b07-9a1c-bdd5bf535a44)

![Screenshot (13)](https://github.com/user-attachments/assets/af7b4242-1116-4cba-85e5-92e203c165f1)

![Screenshot (14)](https://github.com/user-attachments/assets/7651a039-8182-4a46-8a55-b853d31c014b)

![Screenshot (17)](https://github.com/user-attachments/assets/836d83d5-9635-42ef-8a9e-6b079ad798d5)

![Screenshot (18)](https://github.com/user-attachments/assets/ed10198f-f89b-4dc2-a70c-53279c58b2bd)

Video Link: https://drive.google.com/file/d/1P3gvgEi1CBat7yFJ5LbVEsAe3cj3nOAt/view?usp=drive_link
