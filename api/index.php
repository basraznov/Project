<?php
    session_start();
    if (isset($_SESSION['username'])){
        echo $_SESSION['username'];
        echo '<form action="logout.php" method="post">      
        <button type="submit">Logout</button></form>';
    }
    else {
        echo '<form action="login.php" method="post">  
        <input type="text" placeholder="Enter Username" name="username" required>     
        <input type="password" placeholder="Enter Password" name="password" required>   
        <button type="submit">Login</button></form>';
    }
?>