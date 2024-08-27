# nu-housing
Housing Utility - Automated Student Accommodation for University Dormitory

Housing Utility is a tool designed to assist university housing staff in efficiently assigning students to dormitory rooms. The software automates the process of distributing new students among available rooms, ensuring that only rooms with sufficient beds and not undergoing maintenance are selected.

Interface Overview

The interface is divided into two main sections: the Allocation Tool and the Current Dormitory Database.

1. Allocation Tool
- Check-In

  The Check-In section is used to assign new students to rooms in the dormitory. To begin, upload the list of incoming students using the provided template. The software automatically matches students to available rooms based on the selected filters. After processing, the list of newly assigned students is exported as an Excel file and added to the PostgreSQL dormitory database. The data displayed in the Current Database section will be updated accordingly.

- Update Database

  This feature allows for a complete update of the dormitory database when necessary. Upload a file in the required format, and the program will parse the data, completely refresh the database, and update the displayed table in the Current Database section.

2. Current Database

- This section displays the up-to-date dormitory room data retrieved from the database. Filters from the Check-In section can be applied here to focus on specific rooms or students. Statistics related to the current data are also provided.
