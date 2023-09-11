<!DOCTYPE html>
<html>

<head>
    <title>Submitted Data</title>
</head>

<body>
    <h1>Submitted Data</h1>
    <?php
    if (isset($_GET["Name"]) && isset($_GET["Last"])) {
        $name = $_GET["Name"];
        $last = $_GET["Last"];

        echo $last - $name;
        echo "<p>Hello, $name $last!</p>";
    } else {
        echo "<p>No data submitted.</p>";
    }
    ?>
</body>

</html>