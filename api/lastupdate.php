<?php 
    date_default_timezone_set('Asia/Bangkok');
    $k = 0;
    $date = date('Y-m-d', time());
    while(true){
        $stmt = $db->prepare("SELECT date from `trade` where date = ?;");
        $stmt->bind_param('s',$date);
        $stmt->execute();
        $stmt_result = $stmt->get_result();
        if($stmt_result->num_rows > 0){
            $row_data = $stmt_result->fetch_assoc();
            break;
        }
        if ($k === 10){
            break;
        }
        $date = strtotime($date);
        $date = strtotime('-1 day', $date);
        $date = date("Y-m-d",$date );
        $k++;
    }
    $last_update = $date;
?>