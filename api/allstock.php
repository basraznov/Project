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
        $username = $_SESSION['username'];
        $stmt = $db->prepare("SELECT * from `trade` where date = ?;");
        $stmt->bind_param('s',$last_update);
        $stmt->execute();
        $result = mysqli_stmt_get_result($stmt);
        $myfile = fopen("../main/PD.txt", "r") or die("Unable to open file!");
        $file = fread($myfile,filesize("../main/PD.txt"));
        $k = '{"status":"Success",';
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
        $x = 0;
        while ($row = mysqli_fetch_array($result, MYSQLI_NUM)){
            if($file === "None"){
                $trend = "Hold";
            }
            else{
                $trend = searchForId($row[1],$file);
            }

            $stmt = $db->prepare("SELECT * from `company` where symbol = ?;");
            $stmt->bind_param('s',$row[1]);
            $stmt->execute();
            $temp1 = mysqli_stmt_get_result($stmt);
            $temp2 = mysqli_fetch_array($temp1, MYSQLI_NUM);
            $stmt->close();
            if (strpos($row[1], '-') !== false) {
                if($temp2[2] === 'mai'){
                    $m = '"3",';
                }
                else{
                    $m = '"1",';
                }
            }
            else{
                if($temp2[2] === 'mai'){
                    $m = '"2",';
                }
                else{
                    $m = '"0",';
                }
            }
            $k = $k.'"'.$x.'":['.$m.'"'.$row[1].'","'.$row[2].'","'.$row[5].'","'.$row[6].'","'.$row[7];//.'","'.$row[6].'","'.$row[7].'","'.$row[8];
            if($trend != false){
                $k = $k.'","'.$trend.'"],';
                }
            else{
                $k = $k.'","Hold"],';
            }
            $x++;
        }
        $k = rtrim($k,",");
        $k = $k.',"last_update":"'.$last_update.'"}';
        echo $k;
    }
    else{
        echo '{"status":"Require login or wrong parameter"}';

    }

?>