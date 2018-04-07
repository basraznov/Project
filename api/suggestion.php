<?php
    include("database.php");
    header('Content-Type: application/json');
    session_start();
    if(isset($_SESSION['username'])){
        $username = $_SESSION['username'];
        
        $myfile = fopen("../main/ML.txt", "r") or die("Unable to open file!");
        $file = fread($myfile,filesize("../main/PD.txt"));
        if($file === "None"){
            echo '{"status":"No stock suggestion today"}';
        }
        else{
            $file = explode(",",$file);
            foreach ($file as &$value) {
                $value = preg_replace('/[^a-z0-9\-]/i', '', $value);
            }
            $m = '[';
            $s = '[';
            foreach($file as &$value){
                $stmt = $db->prepare("SELECT * from `company` where  symbol = ?;");
                $stmt->bind_param('s',$value);
                $stmt->execute();
                $result = mysqli_stmt_get_result($stmt);
                $row = mysqli_fetch_array($result, MYSQLI_NUM);
                if($row[2] === "SET"){
                    $s = $s.'"'.$value.'",';
                }
                if($row[2] === "mai"){
                    $m = $m.'"'.$value.'",';
                }
            }
            $s = rtrim($s,",");
            $s = $s.']';
            $m = rtrim($m,",");
            $m = $m.']';
            echo '{"status":"Success","set":'.$s.',"mai":'.$m.'}';
        }
    }
    else{
        echo '{"status":"Require login or wrong parameter"}';
    }
?>