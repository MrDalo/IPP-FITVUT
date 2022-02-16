<?php
ini_set('display_errors', 'stderr');
include "./programArguments.php";

processArgument();

$IDheader = false;

/**
 * regex prazdenho riadku s komentom: '/(^\s+#|^#|^\s+\s$)/'
 */


$numberOfLine = 0;


while(($line = fgets(STDIN)) != false)
{
    if(!$IDheader)
    {
        if(preg_match('/(^\s*.IPPcode22\s*(\s$|#)|^\s*.IPPcode22$)/i', $line))
        {
            $IDheader = true;
            echo "Mam header\n";
            $numberOfLine++;
        }
        else  if(preg_match('/(^\s+#|^#|^\s+\s$)/i', $line, $matches))
        {
            // znaci prazdny riadok
            fwrite(STDERR, "Empty line: $numberOfLine\n");
        }
        else
        {
            fwrite(STDERR, "ERROR 21 - Missing or bad header\n");
            echo "TU\n";
            exit(21);

        }  
    
    }





}




?>