<?php
//     include './programArguments.php';
//     $a = 1;
//     $option = getopt("abc");
//     $mywriter = new XMLWriter();


//     function hy()
//     {
    
//         global $b;
//         $a = 10;
//         //echo "$a\n";
//         $b = 1222;

//     }

// echo "1";
//     //processArgument();

// //hy();



$input = "ahoj@";
$split = preg_split('/@/',$input, 2, PREG_SPLIT_NO_EMPTY);
print_r($split);

?>