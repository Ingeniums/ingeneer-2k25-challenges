<?php

if (!isset($_SERVER['HTTP_REFERER']) || strpos($_SERVER['HTTP_REFERER'], 'index.php') === false) {
    header("Location: index.php");
    exit();
}

// Base62 encoded flag
$flag = "5M7cH20igAGgo6F7vN7QrQOPIrkYw1fopf8i6YTKr3qFzpRbmqcYMEvIjKaNuH"; 
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard </title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <h1>Welcome to the Dashboard</h1>
    <p>Your flag is: <?php echo $flag; ?></p>
    
    <p><a href="index.php">Logout</a></p>

</body>
</html>

