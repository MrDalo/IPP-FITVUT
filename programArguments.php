<?php
/**
 * Project: IPP22
 * @author Dalibor Kralik, xkrali20
 * @brief Module which process program arguments
 * 
 * @file programArguments.php
 */


/**
 * @brief Function which process program arguments
 * @use call processArgument() in external modules
 * 
 */
function processArgument()
{
    global $argc, $argv;

    if($argc == 2)
    {
        $argument = $argv[1];
        if($argument == "--help")
        {
            echo("This is Help section of parser.php\n");
            echo("=====================================\n\n");
            echo("This program supports just one argument\n\n");
            echo("      --help      -shows help section of parser.php\n\n\n");
            echo("=====================================\n\n");
            echo("The program can by run as:\n");
            echo "      \$php parser.php [--help]\n\n";
            echo("=====================================\n\n");
            exit(0);
        }
        else
        {
            fwrite(STDERR, "ERROR 10 - unknow argument\n");
            exit(10);
        }
    }
    else if($argc > 2)
    {
        fwrite(STDERR, "ERROR 10 - unexpected combination of arguments\n");
        exit(10);
    }

}


?>