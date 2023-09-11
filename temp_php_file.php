<?php
// Data that pass through POST
$data = array(
   'Name' => '1',
   'Last' => '2',
);
foreach ($data as $key => $value) {
   $_POST[$key] = $value;
}
?>
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
        echo "<p>Hello, $name $last!</p>";
    } else {
        echo "<p>No data submitted.</p>";
    }
    ?>
</body>

</html>