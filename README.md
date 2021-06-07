# LessonPlanner-api

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/ff4fcea4832145388bdad098955fd994)](https://app.codacy.com/manual/WycliffeMuchumi/LessonPlanner-api?utm_source=github.com&utm_medium=referral&utm_content=WycliffeMuchumi/LessonPlanner-api&utm_campaign=Badge_Grade_Settings)

  A minimal flask restful API to be consumed by the LessonPlanner-Client-App application.
  Consists of a list of dictionaries used as a memory data storage instead of an actual database(to be done only in development environment and not in production environment where an actual database is recommended).
  Error handlers to handle various error scenarios as a results of HTTP Requests made by clients.
  Use of flask-httpauth flask extension for securing the API.
