<?php
    include("database.php");
    header('Content-Type: application/json');
    if(isset($_POST['username']) && isset($_POST['password']) && isset($_POST['tel']) && isset($_POST['email'])){
        $username = $_POST['username'];
        $password = hash('sha256',$_POST['password']);
        $tel = $_POST['tel'];
        $email = $_POST['email'];
        $stmt = $db->prepare("SELECT username,email FROM `user` WHERE username = ? OR email = ?");
        $stmt->bind_param('ss',$username ,$email);
        $stmt->execute();
        $stmt->bind_result($username,$email);
        $stmt->store_result();
        if ($stmt->num_rows >= 1){
            echo '{"status":"username or email is used"}';
        }
        else{
            $stmt = $db->prepare("INSERT INTO user (Username,Password,tel,email) VALUES (?,?,?,?)");
            $stmt->bind_param('ssss',$username,$password,$tel,$email);
            $stmt->execute();
            echo '{"status":"Success"}';
        }
    }
    else{
        echo '{"status":"wrong parameter"}';
    }
?>