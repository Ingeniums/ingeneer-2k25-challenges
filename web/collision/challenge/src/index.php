<?php
// Handle form submission
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    
    $username = $_POST['username'];
    $password = $_POST['password'];
    
    
    $md5_username = md5($username);
    $md5_password = md5($password);

   
    if (
         $username !== $password &&
         substr($md5_username, 0, 20) === substr($md5_password, 0, 20)
    ) {
       
        header("Location: dashboard.php");
        exit();
    } else {
        
        $error_message = "Invalid credentials, please try again.";
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title> Collision Challenge</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

    
    <p>Please log in to access the dashboard and view the flag.</p>

    <?php if (isset($error_message)) { echo "<p style='color:red;'>$error_message</p>"; } ?>

    <form method="POST" action="">
        <input type="text" name="username" placeholder="Username" required><br>
        <input type="password" name="password" placeholder="Password" required><br>
        <input type="submit" value="Login">
    </form>

   

    
    <pre>
<!--

if (
    $username !== $password &&
    substr($md5_username, 0, 20) === substr($md5_password, 0, 20) 
    
) {
  
    header("Location: dashboard.php");
    exit();
} else {
    
    $error_message = "Invalid credentials, please try again.";
}
-->
</pre>


</body>
</html>

