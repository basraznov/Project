<?php
    include("database.php");
    header('Content-Type: application/json');
    session_start();
    if(isset($_SESSION['username']){
        $username = $_SESSION['username'];
        
    }
?>