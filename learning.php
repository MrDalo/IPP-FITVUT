<?php
    include './programArguments.php';
    $a = 1;
    $option = getopt("abc");
    $mywriter = new XMLWriter();


    function hy()
    {
    
        global $b;
        $a = 10;
        echo "$a\n";
        $b = 1222;

    }


    processArgument();

//hy();







?>