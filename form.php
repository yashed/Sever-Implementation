<!DOCTYPE html>
<html>

<head>
    <title>PHP Form</title>
</head>

<body>
    <h1>PHP Form Example</h1>
    <form method="POST">
        <label for="name">Name:</label>
        <input type="text" id="name" name="name" required>
        <br><br>
        <input type="submit" value="Submit">
    </form>

    <?php
     echo "hello";
    if (isset($_SERVER["REQUEST_METHOD"])  ) {
        
        echo "hello";
        $name = $_POST["name"];
        echo "<p>Hello, $name!</p>";
    }
    ?>
</body>

</html>