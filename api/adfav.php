<?php
    include("database.php");
    header('Content-Type: application/json');
    session_start();
    if(isset($_SESSION['username']) && isset($_POST['stock']) && isset($_POST['status'])){
        $stock = $_POST['stock'];
        $status = $_POST['status'];//1 = add 0 = del
        $username = $_SESSION['username'];
        $stmt = $db->prepare("SELECT * FROM `favorite` WHERE stock = ? and username = ?;");
        $stmt->bind_param('ss',$stock ,$username);
        $stmt->execute();
        $stmt->bind_result($stock,$username);
        $stmt->store_result();
        if ($stmt->num_rows < 1 && $status === "0"){
            echo '{"status":"You don\'t have this stock in list"}';
        }
        else if ($stmt->num_rows >= 1 && $status === "1"){
            echo '{"status":"You have this stock"}';
        }
        else if ($stmt->num_rows >= 1 && $status === "0"){
            $stmt = $db->prepare("DELETE FROM `favorite` WHERE stock = ? and username = ?;");
            $stmt->bind_param('ss',$stock,$username);
            $stmt->execute();
            echo '{"status":"Deleted"}';
        }
        else if ($stmt->num_rows < 1 && $status === "1"){
            $stmt = $db->prepare("INSERT INTO `favorite` (Username,stock) VALUES (?,?);");
            $stmt->bind_param('ss',$username,$stock);
            $stmt->execute();
            echo '{"status":"Added"}';
        }
        else{
            echo '{"status":"Require login or wrong parameter"}';
        }
    }
    else {
        echo '{"status":"Require login or wrong parameter"}';
    }
?>