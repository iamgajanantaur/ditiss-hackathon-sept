<?php
$servername = "192.168.10.20"; // Replace with your database server IP
$username = "leader"; // Replace with your MySQL user
$password = "admin@123"; // Replace with your MySQL password
$dbname = "userdb";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
?>
