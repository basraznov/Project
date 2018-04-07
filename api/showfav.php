<?php 
    include("database.php");
    header('Content-Type: application/json');
    session_start();
    if(isset($_SESSION['username'])){
        $username = $_SESSION['username'];
        $stmt = $db->prepare("SELECT * FROM `favorite` WHERE username = ?;");
        $stmt->bind_param('s',$username);
        $stmt->execute();
        $k = "[";
        $result = mysqli_stmt_get_result($stmt);
        while ($row = mysqli_fetch_array($result, MYSQLI_NUM)){
            // $k = $k.'"'.$row[1].'",';
            echo $row[1];
        }
        die();
        $k = rtrim($k,",");
        echo '{"status":"Success","stock":'.$k.']}';
    }
    else{
        echo '{"status":"Require login or wrong parameter"}';
    }

?>