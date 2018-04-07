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
                        if($stock === $value[0]){
                            $trend = $value[1];
                        }
                    }
                    if($trend === ""){
                        $trend = "Hold";
                    }
                }

                $tempday = strtotime($date);
                $tempday = date("d",$tempday );
                $tempday = intval($tempday)-1;
                $tempstr = '-'.$tempday.' day';
                $endm = strtotime($date);
                $endm = strtotime($tempstr, $endm);
                $endm = date("Y-m",$endm );
                $startm = strtotime($endm);
                $startm = strtotime('- 1 months', $startm);
                $startm = date("Y-m",$startm );
                $stmt = $db->prepare("SELECT * from `trade` where  symbol = ? and date < ? and date >= ? ORDER by Date;");
                $endm = $endm."-01";
                $startm = $startm."-01";
                $stmt->bind_param('sss',$stock,$endm,$startm);
                $stmt->execute();
                $result = mysqli_stmt_get_result($stmt);
                $mhigh = 0; 
                $mvol = 0;
                $mlow = 0;
                $mopen = 0;
                $mlast = 0;
                $fmdate = "";
                $lmdate = "";
                while ($row = mysqli_fetch_array($result, MYSQLI_NUM)){
                    if ($mlow === 0){
                        $fmdate = $row[0];
                        $mlow = $row[4];
                        $mopen = $row[2];
                    }
                    if($row[4] <= $mlow) {
                        $mlow = $row[4];
                    }
                    if($row[3] >= $mhigh){
                        $mhigh = $row[3];
                    } 
                    $mvol += $row[7];
                    $mlast = $row[5];
                    $lmdate = $row[0];
                }
                $p = 0;
                $mper = 0;
                $startmper = strtotime($startm);
                $startmper = strtotime('-1 day', $startmper);
                $startmper = date("Y-m-d",$startmper );
                while(true){
                    $stmt = $db->prepare("SELECT * from `trade` where  symbol = ? and date = ?;");
                    $stmt->bind_param('ss',$stock,$startmper);  
                    $stmt->execute();
                    $stmt_result = $stmt->get_result();
                    if($stmt_result->num_rows > 0){
                        $row_temp = $stmt_result->fetch_assoc();
                        $mper =  ($mlast - $row_temp['Last'])/$row_temp['Last'] * 100;
                        $mper = number_format($mper, 2, '.', '');
                        break;
                    }
                    if($p > 4){
                        $mper = "None";
                        break;
                    }
                    $startmper = strtotime($startmper);
                    $startmper = strtotime('-1 day', $startmper);
                    $startmper = date("Y-m-d",$startmper );
                    $p++;
                }
                $stmt = $db->prepare("SELECT stock from `favorite` where username = ?;");
                $stmt->bind_param('s',$username);  
                $stmt->execute();
                $result = mysqli_stmt_get_result($stmt);
                $isfav = 0;
                while ($row = mysqli_fetch_array($result, MYSQLI_NUM)){
                    if($stock === $row[0]){
                        $isfav = 1;
                        break;
                    }
                }
                if($date != $last_update){
                    echo '{"status":"Success","date":"'.$row_data['Date'].'","open":"'.$row_data['Open'].'","high":"'.$row_data['High'].'","low":"'.$row_data['Low'].'","last":"'.$row_data['Last'].'","percent_change":"'.$row_data['ChPer'].'","openM":"'.$mopen.'","highM":"'.$mhigh.'","lowM":"'.$mlow.'","lastM":"'.$mlast.'","percent_changeM":"'.$mper.'","fday":"'.$fmdate.'","lday":"'.$lmdate.'","trend":"None","last_update":"'.$last_update.'","isfavorite":"'.$isfav.'"}';
                }
                else{
                    echo '{"status":"Success","date":"'.$row_data['Date'].'","open":"'.$row_data['Open'].'","high":"'.$row_data['High'].'","low":"'.$row_data['Low'].'","last":"'.$row_data['Last'].'","percent_change":"'.$row_data['ChPer'].'","openM":"'.$mopen.'","highM":"'.$mhigh.'","lowM":"'.$mlow.'","lastM":"'.$mlast.'","percent_changeM":"'.$mper.'","fday":"'.$fmdate.'","lday":"'.$lmdate.'","trend":"'.$trend.'","last_update":"'.$last_update.'","isfavorite":"'.$isfav.'"}';
                    
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