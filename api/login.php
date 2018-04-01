<?php
    include('database.php');
    header('Content-Type: application/json');
    if(isset($_POST['username']) && isset($_POST['password'])){
        $username = $_POST['username'];
        $password = hash('sha256',$_POST['password']);
        $stmt = $db->prepare("SELECT username FROM `user` WHERE username = ? and password = ?;");
        $stmt->bind_param('ss',$username ,$password);
        $stmt->execute();
        $stmt->bind_result($username);
        if($stmt->fetch() == 'true'){
            session_start();
            echo '{"status":"Success"}';
            $_SESSION["username"] = $username;
        }else{
            echo '{"status":"wrong username or password"}';
        }
    }
    else{
        echo '{"status":"worng parameter"}';
    }
?>