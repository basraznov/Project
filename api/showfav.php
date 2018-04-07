<?php 
    include("database.php");
    include("lastupdate.php");
    header('Content-Type: application/json');
    session_start();
    if(isset($_SESSION['username'])){
        $last_update = $date;
        $username = $_SESSION['username'];
        $stmt = $db->prepare("SELECT * FROM `trade` WHERE Symbol in (SELECT stock FROM `favorite` WHERE username = ?) and Date = ?;");
        $stmt->bind_param('ss',$username,$date);
        $stmt->execute();
        $k = "";
        $x = 0;
        $result = mysqli_stmt_get_result($stmt);
        while ($row = mysqli_fetch_array($result, MYSQLI_NUM)){
            $k = '"'.$x.'":["'.$row[1].'","'.$row[2].'","'.$row[5].'","'.$row[6].'"],'.$k;
            $x++;
        }
        $k = rtrim($k,",");
        echo '{"status":"Success",'.$k.'}';
    }
    else{
        echo '{"status":"Require login or wrong parameter"}';
    }

?>