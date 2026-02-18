student_enrollment

-   student
    -   api.py ----> API endpoints
    -   model.py ----> database schema
    -   validations.py ----> data validation and serialization
    -   service.py ----> Write your business logic here
-   course

##### flask migrate

```
flask db init - intialize the environment
flask db migrate -m "Initial course table" - Generates the SQL script
flask db upgrade -  actually create a tables in database 
```
availabilities = db.relationship('StaffAvailability', backref='staff', lazy=True)