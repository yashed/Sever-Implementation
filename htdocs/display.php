<!DOCTYPE html>
<html>

<head>
    <title>Submitted Data</title>
</head>

<body>
    <h1>Submitted Data</h1>
    <?php
    if (isset($_POST["Name"]) && isset($_POST["Last"])) {
        $name = $_POST["Name"];
        $last = $_POST["Last"];

        echo $last + $name;
        echo "<p>Number 1 = $name</br> Number 2 = $last</p>";
    } else {
        echo "<p>No data submitted.</p>";
    }
    ?>
</body>

</html>