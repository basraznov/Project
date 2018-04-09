<?php
    include("database.php");
    include("lastupdate.php");
    header('Content-Type: application/json');
    session_start();
    if(isset($_SESSION['username'])){
        if(isset($_POST['oldpassword'])){
            $username = $_SESSION['username'];
            $oldpass = hash('sha256',$_POST['oldpassword']);
            $stmt = $db->prepare("SELECT username FROM `user` WHERE username = ? and password = ?;");
            $stmt->bind_param('ss',$username ,$oldpass);
            $stmt->execute();
            $stmt->bind_result($username);
            if($stmt->fetch() == 'true'){
                $k = 0;
                $stmt->close();
                if(isset($_POST['email'])){
                    $email = $_POST['email'];
                    $stmt = $db->prepare("UPDATE `user` SET Email = ? WHERE  Username = ?");
                    $stmt->bind_param("ss", $email, $username);
                    $stmt->execute();
                    $k++;
                }
                if(isset($_POST['newpassword'])){
                    $newpass = $_POST['newpassword'];
                    $stmt = $db->prepare("UPDATE `user` SET Password = ? WHERE  Username = ?");
                    $stmt->bind_param("ss", $newpass, $username);
                    $stmt->execute();
                    $k++;
                }
                if(isset($_POST['tel'])){
                    $tel = $_POST['tel'];
                    $stmt = $db->prepare("UPDATE `user` SET Tel = ? WHERE  Username = ?");
                    $stmt->bind_param("ss", $tel, $username);
                    $stmt->execute();
                    $k++;
                }
                if($k === 0){
                    echo '{"status":"Require login or wrong parameter"}1';
                }
                else{
                    echo '{"status":"Success"}';
                }
            }
            else{
                echo '{"status":"Wrong password"}';
            }
        }
        else{
            echo '{"status":"Require login or wrong parameter"}2';
        }
    }
    else{
        echo '{"status":"Require login or wrong parameter"}3    ';
    }

?>