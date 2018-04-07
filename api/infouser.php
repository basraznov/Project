<?php
    include("database.php");
    session_start();
    if(isset($_SESSION['username']) && isset($_POST['status'])){
        $username = $_SESSION['username'];
        $status = $_POST['status'];
        
        $stmt = $db->prepare("SELECT * from `user` where  username = ?;");
        $stmt->bind_param('s',$username);
        $stmt->execute();
        $result = mysqli_stmt_get_result($stmt);
        $row = mysqli_fetch_array($result, MYSQLI_NUM);
        if ($status === '0'){
            echo '{"status":"Success","membername":"'.$row[0].'","tel":"'.$row[2].'","email":"'.$row[3].'"}';
        }
        else if ($status === '1'){
            echo '{"status":"Success","membername":"'.$row[0].'","email":"'.$row[3].'"}';
        }
        else{
            echo '{"status":"Require login or wrong parameter"}';
        }
    }
    else{
        echo '{"status":"Require login or wrong parameter"}';
    }
?>