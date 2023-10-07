### SNAPBOOK
## Collaborative Photo Album Platform

This collaborative photo album platform is the culmination of my final coursework for Harvard's CS50 course. It's designed to provide a user-friendly web application for friends to create, share, and cherish memories together through photos. The project uses a combination of Python, Flask, Bootstrap, and SQLite to deliver a comprehensive photo-sharing experience.

#### Features:

1. **Login and Registration System:**
   - Users can securely register and log into the platform to ensure the privacy and authenticity of their interactions.

2. **Album Creation:**
   - Users have the ability to create new albums, specifying album names and group associations. This feature promotes organized sharing within specific circles of friends.

3. **Album Pages:**
   - Each album has a dedicated page displaying the collection of photos related to that group. The Bootstrap framework ensures a responsive and visually appealing layout.

4. **Photo Upload:**
   - Friends within the group can contribute photos to shared albums, creating a collective visual representation of their experiences.

5. **Album Invitation:**
   - Users can request to join a group, fostering a sense of community and interaction.

6. **Discover Relevant Albums:** 
   - Enter keywords, album names, or descriptions in the search box to locate specific albums that pique their interest.

7. **User-Friendly Interface:**
   - The Bootstrap framework guarantees a user-friendly interface that adapts to different devices, ensuring a seamless experience across various screen sizes.

#### Technology Stack:

- **Python:** The core programming language used for backend development.
  
- **Flask:** A lightweight and flexible web framework for Python, responsible for building the web application, managing routing, and handling server-side functionality.

- **Bootstrap:** A popular front-end framework that aids in creating responsive and visually appealing user interfaces.

- **SQLite:** A compact and reliable database management system used to store user data, album details, photo information, and user interactions.

### Usage:

To run the project:

1. Clone the repository to your local machine.

2. Install the required dependencies using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up your Flask application secret key and database configuration.

4. Run the Flask application:

   ```bash
   flask run
   ```

5. Access the application in your web browser by navigating to `http://localhost:5000`.

### Project Structure:

- `app.py`: The main Flask application that handles routing and server-side logic.
- `templates/`: Contains HTML templates for rendering web pages.
- `static/`: Stores static assets like CSS, JavaScript, and images.
- `snapbook.db`: The SQLite database file where user data and album details are stored.
- `helpers.py`: Contains helper functions for authentication and other functionalities.
- `requirements.txt`: Lists the project's dependencies for easy installation.

### Contribution:

This project is open for contributions and improvements. If you have any suggestions or would like to add new features, feel free to create a pull request.

### License:

This project is licensed under the [MIT License](LICENSE). You are welcome to use and modify the code for your own purposes.