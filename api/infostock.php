<?php
    include("database.php");
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
            $stmt->bind_param('ss',$stock,$stdate);
            $stmt->execute();
            $stmt_result = $stmt->get_result();
            if($stmt_result->num_rows > 0){
                $row_data = $stmt_result->fetch_assoc();
                $myfile = fopen("../main/PD.txt", "r") or die("Unable to open file!");
                $file = fread($myfile,filesize("../main/PD.txt"));
                $file = explode("], [",$file);
                foreach ($file as &$value) {
                    $value = explode(", ",$value);
                    foreach ($value as &$supva){
                        $supva = preg_replace('/[^a-z0-9\-]/i', '', $supva);
                        if($stock === $supva[0]){
                            echo "asd";
                        }
                    }
                }
                echo '{"status":"Success","last_update":"'.$row_data['Date'].'","open":"'.$row_data['Open'].'","high":"'.$row_data['High'].'","low":"'.$row_data['Low'].'","last":"'.$row_data['Last'].'"}';
                break;
            }
            if($k > 4){
                echo '{"status":"This stock is not up to date or don\'t have this stock"}';
                break;
            }
            $k++;
        }    
    }
    else{
        echo '{"status":"Require login or wrong parameter"}';
    }




// def infostock(stock,date):
//     date = datetime.strptime(date, '%Y-%m-%d').date()
//     mydb = MySQLdb.connect(host='127.0.0.1',user='root',passwd='',db='Project')
//     sql = "SELECT * from `trade` where  symbol = %s and date = %s"
//     for x in range(0,6):
//         data = [stock,str(date)]
//         cursor = mydb.cursor()
//         cursor.execute(sql,data)
//         results = cursor.fetchall()
//         row = cursor.rowcount
//         if row >= 1:
//             return results
//         date -= dt.timedelta(days=1)
//     return "stock close"
    ?>