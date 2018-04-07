<?php 
    include("database.php");
    include("lastupdate.php");
    header('Content-Type: application/json');
    session_start();

    function searchForId($id, $array) {
        foreach ($array as $key => $val) {
            if ($val[0] === $id) {
                return $val[1];
            }
        }
        return false;
    }

    if(isset($_SESSION['username'])){
        $last_update = $date;
        $username = $_SESSION['username'];
        $stmt = $db->prepare("SELECT * FROM `trade` WHERE Symbol in (SELECT stock FROM `favorite` WHERE username = ?) and Date = ?;");
        $stmt->bind_param('ss',$username,$date);
        $stmt->execute();
        $k = "";
        $x = 0;
        $result = mysqli_stmt_get_result($stmt);
        $myfile = fopen("../main/PD.txt", "r") or die("Unable to open file!");
        $file = fread($myfile,filesize("../main/PD.txt"));
        $trend = "Hold";
        if($file === "None"){
            $trend = "Hold";
        }
        else{
            $file = explode("], [",$file);
            foreach ($file as &$value) {
                $value = explode(", ",$value);
                foreach ($value as &$supva){
                    $supva = preg_replace('/[^a-z0-9\-]/i', '', $supva);
                }
            }
        }
        while ($row = mysqli_fetch_array($result, MYSQLI_NUM)){
            if($file === "None"){
                $trend = "Hold";
            }
            else{
                $trend = searchForId($row[1],$file);
                if (!$trend){
                    $trend = "Hold";
                }
            }
            $k = '"'.$x.'":["'.$row[1].'","'.$row[2].'","'.$row[5].'","'.$row[6].'","'.$trend.'"],'.$k;
            $x++;
        }
        $k = rtrim($k,",");
        echo '{"status":"Success",'.$k.'}';
    }
    else{
        echo '{"status":"Require login or wrong parameter"}';
    }

?>