<?php
    include("database.php");
    include("lastupdate.php");
    header('Content-Type: application/json');
    session_start();
    date_default_timezone_set('Asia/Bangkok');
    if(isset($_SESSION['username']) && isset($_POST['stock']) && isset($_POST['date'])){
        $stock = $_POST['stock'];
        $stdate = $_POST['date'];
        $date = strtotime($_POST['date']);
        $date = date("Y-m-d",$date );
        $nowdate = date('Y-m-d', time());
        $username = $_SESSION['username'];
        if ($date > $nowdate){
            echo '{"status":"Worong date"}';
            die();
        }
        $k = 0;
        while (true){
            $stmt = $db->prepare("SELECT * from `trade` where  symbol = ? and date = ?;");
            $stmt->bind_param('ss',$stock,$date);
            $stmt->execute();
            $stmt_result = $stmt->get_result();
            $trend = "";
            if($stmt_result->num_rows > 0){
                $row_data = $stmt_result->fetch_assoc();
                $myfile = fopen("../main/PD.txt", "r") or die("Unable to open file!");
                $file = fread($myfile,filesize("../main/PD.txt"));
                $file = explode("], [",$file);
                if($file === "None"){
                    $trend = "Hold";
                }
                else{
                    foreach ($file as &$value) {
                        $value = explode(", ",$value);
                        foreach ($value as &$supva){
                            $supva = preg_replace('/[^a-z0-9\-]/i', '', $supva);
                        }
                        if($stock === $value[0]){
                            $trend = $value[1];
                        }
                    }
                    if($trend === ""){
                        $trend = "Hold";
                    }
                }
                if($date != $last_update){
                    echo '{"status":"Success","date":"'.$row_data['Date'].'","open":"'.$row_data['Open'].'","high":"'.$row_data['High'].'","low":"'.$row_data['Low'].'","last":"'.$row_data['Last'].'","trend":"None","last_update":"'.$last_update.'"}';
                }
                else{
                    echo '{"status":"Success","date":"'.$row_data['Date'].'","open":"'.$row_data['Open'].'","high":"'.$row_data['High'].'","low":"'.$row_data['Low'].'","last":"'.$row_data['Last'].'","trend":"'.$trend.'","last_update":"'.$last_update.'"}';
                }
                break;
            }
            if($k > 4){
                echo '{"status":"This stock is not up to date or don\'t have this stock"}';
                break;
            }
            $date = strtotime($date);
            $date = strtotime('-1 day', $date);
            $date = date("Y-m-d",$date );
            $k++;
        }    
    }
    else{
        echo '{"status":"Require login or wrong parameter"}';
    }
?>