<?php
// Data that pass through POST
$data = array(
);
foreach ($data as $key => $value) {
   $_GET[$key] = $value;
}
?>
<!DOCTYPE html>
<html>

<head>
    <title>Server</title>
</head>

<body>
    <h1 style=" color: darkslategrey; text-align:center;">Welcome to My SERVER</h1>
    <div style="margin:100px">
        <h2 style="color: navy"> How it works</h2>
        <p> Type <b> http://localhost:2728/"file-name" </b> to run </P>
    </div>
</body>

</html>