# Job Application Manager

This repository contains a Python server designed to help you manage and track your job applications efficiently.

## Features

- **Application Tracking**: Keep a record of all job applications, including company name, job title, application date, status, and notes.
- **Search and Filter**: Easily search and filter applications based on various criteria.
- **Notifications**: Get reminders for follow-ups and deadlines.
- **User Authentication**: Securely manage your application data with user authentication.

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/ivasik-k7/JobApplicationAPI.git
   ```

2. Install the dependencies with poetry:

   ```sh
   poetry install
   ```

3. Install Poetry if needed (Optional)
   ```sh
   pip install poetry
   ```

## Usage

1. Run the server:

   ```sh
    uvicorn --version app.main:app --host 0.0.0.0 --port 8000
   ```

2. Open your web browser and navigate to `http://localhost:8000` to access the application.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
