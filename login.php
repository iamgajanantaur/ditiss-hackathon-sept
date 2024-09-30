<?php
require 'config.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST['username'];
    $password = $_POST['password'];

    // Prepare a statement to fetch the user
    $sql = "SELECT password FROM users WHERE username=?";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("s", $username);
    $stmt->execute();
    $stmt->store_result();
    $stmt->bind_result($hashed_password);

    if ($stmt->num_rows > 0) {
        $stmt->fetch();
        // Verify the password
        if (password_verify($password, $hashed_password)) {
            header("Location: welcome.php");
        } else {
            echo "Incorrect password!";
        }
    } else {
        echo "Username not found!";
    }

    $stmt->close();
}
?>

<h2>Login</h2>
<form method="post">
    Username: <input type="text" name="username" required><br>
    Password: <input type="password" name="password" required><br>
    <input type="submit" value="Login">
</form>
