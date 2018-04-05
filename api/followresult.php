<?php 
header('Content-Type: application/json');
include("database.php");
session_start();
if(isset($_SESSION['username']) && isset($_POST['fdate']) && isset($_POST['ldate']) && isset($_POST['stock']) && isset($_POST['money'])){
    $fdate = $_POST['fdate'];
    $ldate = $_POST['ldate'];
    $stock = $_POST['stock'];
    $money = $_POST['money'];

    $stmt = $db->prepare("SELECT * FROM `company` WHERE symbol = ?;");
    $stmt->bind_param('s',$stock);
    $stmt->execute();
    $stmt->store_result(); 
    // echo preg_match("\d{4}-\d{2}-\d{2}",$fdate);

    if ($stmt->num_rows >= 1 && preg_match('/^[0-9]+$/',$money) && preg_match("/^\d{4}-\d{2}-\d{2}+$/",$fdate) && preg_match("/^\d{4}-\d{2}-\d{2}+$/",$ldate)){
        $m = '{"status":"Success"';
        $cmd = 'python ../main/FollowResult.py '.$stock.' '.$fdate.' '.$ldate.' '.$money;
        $result = shell_exec($cmd);
        if($result ===){

        }
        else{
            $result = preg_replace("/[ ]/", "", $result);
            $x = 0;
            $result = explode("\n", $result);
            unset($result[count($result)-1]);
            foreach($result as $line){
                if($result[count($result)-1] === $line){
                    $m = $m.',"summary":'.$line;
                }
                else{
                    $m = $m.',"'.$x.'":'.$line;
                    $x++;
                }
            } 
            $m = $m.'}';
            echo $m;
        }
    }
    else{
        echo '{"status":"Require login or wrong parameter"}';
    }
}
else{
    echo '{"status":"Require login or wrong parameter"}';
}
?>