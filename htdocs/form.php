<!DOCTYPE html>
<html>

<head>
    <title>PHP Form</title>
</head>

<body>
    <h1>PHP Form Example</h1>
    <form method="POST" action="display.php">
        <label for="name">Name:</label>
        <input type="text" id="name" name="Name" required>
        <br><br>
        <label for="lastname">Last Name:</label>
        <input type="text" id="lastname" name="Last" required>
        <label>Age</label>

        <input type="submit" value="Submit">
    </form>
</body>

</html>