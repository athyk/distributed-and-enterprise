# How To Insert Dummy Data

If first time inserting data please delete all databases from your system
Reason: there was a minor issue with one of the foreign key constraints

Run Docker and all containers using the following command in the terminal: `docker-compose up --build`

Ensure that there is no data in the existing tables already. If unsure, delete the entire database.

Once the project is running, open up `insert_data.py` and run the file

This should insert all of the data into the respectable tables
