<?php
/**
 * Project: IPP22
 * @author Dalibor Kralik, xkrali20
 * @brief Module which process program arguments
 * 
 * @file test.php
 */
ini_set('display_errors', 'stderr');



function processArgument()
{
    global $argc, $argv, $recursive, $directory, $parseScript, $intScript, $parseOnly, $intOnly, $noClean, $jExamPath;

    $longOpts=array(
        "help",
        "directory::",
        "recursive",
        "parse-script::",
        "int-script::",
        "parse-only",
        "int-only",
        "jexampath::",
        "noclean"
    );

    $options = getopt("",$longOpts);

    if(array_key_exists('help', $options))
    {
        if ($argc >2)
        {
            fwrite(STDERR, "ERROR 10 - unexpected combination of arguments\n");
            exit(10);
        }

        echo("This is Help section of test.php\n\n");
        echo("==========================================================================\n\n");
        echo("This program supports just one argument\n\n");
        echo("      --help      -shows help section of parser.php\n\n");
        echo("      --parse-script=      -Argument takes link to the parse script and his name\n");
        echo("                            If not used, test.php will use \"parse.php\" in current folder\n\n");
        echo("      --int-script=      -Argument takes link to the intepret script and his name\n");
        echo("                            If not used, test.php will use \"interpret.py\" in current folder\n\n");
        echo("      --jexampath=      -Link to the comparator of XML files. If not used, test.php will use \"/pub/courses/ipp/jexamxml/\" \n\n");
        echo("      --parse-only      -Tests only parser in --parse-script or parse.php\n\n");
        echo("      --int-only        -Tests only intepret in --int-script or interpret.py\n\n");
        echo("      --recursive       -Recursive folder searching\n\n");
        echo("      --no-clean        -No cleaning after test.php execution\n\n");
        echo("==========================================================================\n\n");
        echo("The program can by run as:\n");
        echo "      \$php parser.php [--help] [--directory=] [--parse-script=] [--int-script=] [--jexampath=] [--parse-only] [--int-only] [--recursive] [--noclean]\n\n";
        echo("==========================================================================\n\n");
        exit(0);
    }

    $parseOnly = array_key_exists('parse-only', $options);
    $intOnly = array_key_exists('int-only', $options);
    $recursive = array_key_exists('recursive', $options);
    $noClean = array_key_exists('noclean', $options);


    if ((array_key_exists('directory', $options)))
    {
        $directory = $options["directory"];
    }
    else
    {
        $directory = getcwd();
    }

    if ($directory[strlen($directory) - 1] !="/" and  !preg_match('/.+\.src$/', $directory))
    {
        $directory =$directory.'/';
    }
    
    if ($intOnly != 1)
    {
        if ((array_key_exists('parse-script', $options)))
        {
            $parseScript = $options["parse-script"];
        }
        else
        {
            $parseScript = "parse.php";
        }
    
        if(!file_exists($parseScript))
        {
            fwrite(STDERR, "ERROR 41\n");
            exit(41);
        }
        
    }

    
    if ($parseOnly != 1)
    {
        if ((array_key_exists('int-script', $options)))
        {
            $intScript = $options["int-script"];
        }
        else
        {
            $intScript = "interpret.py";
        }

        if(!file_exists($intScript))
        {
            fwrite(STDERR, "ERROR 41\n");
            exit(41);
        }
    
    }

    
    if ((array_key_exists('jexampath', $options)))
    {
        $jExamPath = $options["jexampath"];
        if ($jExamPath[strlen($jExamPath) - 1] !="/")
        {
            $jExamPath += '/';
        }

    }
    else
    {
        $jExamPath = "/pub/courses/ipp/jexamxml/";
    }

    if(!file_exists($jExamPath))
    {
        fwrite(STDERR, "ERROR 41\n");
        exit(41);
    }

    //echo "parseOnly: $parseOnly, intOnly: $intOnly,recursive: $recursive, noCleam: $noClean";

    if ($parseOnly == 1 && (array_key_exists('int-script', $options) or $intOnly == 1))
    {
        fwrite(STDERR, "ERROR 10 - Invalid combination of arguments\n");
        exit(10);
    } 
    
    if ($intOnly ==1  && (array_key_exists('parse-script', $options) or $parseOnly == 1 or array_key_exists('jexampath', $options)))
    {
        fwrite(STDERR, "ERROR 10 - Invalid combination of arguments\n");
        exit(10);
    } 

}


function runTimeOfProgram()
{
    global $argc, $argv, $recursive, $directory, $parseScript, $intScript, $parseOnly, $intOnly, $noClean, $jExamPath, $html, $correctTestsString, $failedTestsString, $testingPart, $srcCounter, $correctTests;
    $srcCounter = 0;
    $correctTests = 0;
    $correctTestsString = "";
    $failedTestsString = "";

    if($parseOnly == 1)
    {
        $testingPart = "Parse";
    }
    else if($intOnly == 1)
    {
        $testingPart = "interpret";
    }
    else
    {
        $testingPart = "All";
    }

        //jedna sa o rekurzivne prehladavanie
    if($recursive == 1)
    {
        if(!file_exists($directory))
        {
            fwrite(STDERR, "ERROR 41\n");
            exit(41);
        }


        $arrayOfFiles = scandir($directory, 0);
        $it = new RecursiveDirectoryIterator($directory);
        $arrayOfFiles = new RecursiveIteratorIterator($it);
        
    }
    else
    {
		
        if(!file_exists($directory))
        {
        
			fwrite(STDERR, "ERROR 41\n");
            exit(41);
        }

		
		if(preg_match('/.+\.src$/', $directory))
		{
			$arrayOfFiles = [$directory];	
		}
		else
		{
        	$arrayOfFiles = scandir($directory, 0);
        }

    }
   
    

    foreach ($arrayOfFiles as $file)
    {
	 	  if($recursive != 1)
		  {
    	  		$file = $directory.$file;
		  }
	 	  // testovanie pre parser
        if (preg_match("/.+\.src$/", $file))
        {
           // echo "$file\n"; 
            $srcCounter += 1;
            
                //vytvorenie output filu pre vystup po spusteni parse.php
            $outputFile = preg_replace("/\.src$/", "_out.out", $file);
            $refferenceOutput = preg_replace("/src$/", "out", $file);
            $refferenceErrorOutput = preg_replace("/src$/", "rc", $file);
            $inFile = preg_replace("/src$/", "in", $file);
            if(!file_exists($refferenceOutput))
            {
                shell_exec("touch $refferenceOutput");
            }
            
            if(!file_exists($refferenceErrorOutput))
            {
                shell_exec("echo 0 > $refferenceErrorOutput");
            }
            if(!file_exists($inFile))
            {
                shell_exec("touch $inFile");
            }

            $programRefferenceErrorCode = shell_exec("cat $refferenceErrorOutput");

            if($intOnly != 1)
            {

                    //spustenie parse.php, s exit kodom
                exec("php8.1 $parseScript <$file >$outputFile 2>/dev/null",$outputArray, $exitCode);

                if ($exitCode == $programRefferenceErrorCode && $parseOnly != 1 && $exitCode > 0)
                {
                    $correctTests +=1;
                    $fileHTML = str_replace($directory, "", $file);
                    $correctTestsString = $correctTestsString."<div>".$fileHTML."</div>";
                    continue;
                }
                else if ($parseOnly != 1)
                {
                    //PASS - symboluje volny prechod ifom
                }
                else if($exitCode == $programRefferenceErrorCode && $parseOnly == 1)
                {
                    
                    if($exitCode == 0)
                    {
						  		$outputOfJavaController = shell_exec("java -jar ".$jExamPath."jexamxml.jar $outputFile $refferenceOutput delta.xml ".$jExamPath."options");
						  			//echo "$outputOfJavaController\n";
                        if(preg_match("/Two files are identical/", $outputOfJavaController))
                        {
                                //Zapis do HTML do CORRECT ze sedi exit code aj je zhodna JAVA
                            $correctTests +=1;
                            $fileHTML = str_replace($directory, "", $file);
                            $correctTestsString = $correctTestsString."<div>".$fileHTML."</div>";
                            // echo "Correct Java tester Output\n";
                        }
                        else
                        {
                                //Zapis do HTML do INCORRECT ze nie je identicka JAVA
                                $fileHTML = str_replace($directory, "", $file);
                            $failedTestsString = $failedTestsString."<div>".$fileHTML."</div>";
                            // echo "Java tester unmatched\n";
                        }
                    }
                    else
                    {
                        //Zapis do HTML ze mam zhodny exitcode > 0, do CORRECT
					 			$correctTests +=1;
                        $fileHTML = str_replace($directory, "", $file);
                        $correctTestsString = $correctTestsString."<div>".$fileHTML."</div>";
                    }

                
                }
                else
                {
                        //Zapis chyby do HTML do INCORRECT
                   // echo "FAILED\n";
						  $fileHTML = str_replace($directory, "", $file);
                    $failedTestsString = $failedTestsString."<div>".$fileHTML."</div>";
                    // echo "Exit Code unmatched: $file";
                    continue;
                }          
                
            } 
       		
				$intOutputFile = "";
                //Zacina testovanie pre interpret
            if($parseOnly != 1)
            {
                if($intOnly != 1)
                {
                 		$file = preg_replace("/\.src$/", "_out.out", $file);
   					   $intOutputFile =preg_replace("/_out\.out$/", "_out2.out", $file);
             		  //echo "$file\n";
				 	 }
					 else
					 {
							$intOutputFile = preg_replace("/\.src$/", "_out.out", $file);
					 }
                exec("python3.8 $intScript --source=$file --input=$inFile >$intOutputFile 2>/dev/null",$outputArray, $exitCode);
                
                if($exitCode == $programRefferenceErrorCode)
                {
                    exec("diff $intOutputFile $refferenceOutput", $outputArray, $exitCode);
                    if($exitCode == 0)
                    {
                        //Zapis do CORRECT
								$correctTests +=1;
                        $fileHTML = str_replace($directory, "", $file);
      					   $fileHTML =preg_replace("/_out\.out$/", ".src", $fileHTML);
                       $correctTestsString = $correctTestsString."<div>".$fileHTML."</div>";
                    }
                    else
                    {
					  			//Zapis do INCORRECT
                        $fileHTML = str_replace($directory, "", $file);
       					   $fileHTML =preg_replace("/_out\.out$/", ".src", $fileHTML);
                        $failedTestsString = $failedTestsString."<div>".$fileHTML."</div>";
                    }
            
                }
                else
                {
		  					//Zapis do INCORRECT nezhodny exit code
                    $fileHTML = str_replace($directory, "", $file);
      				  $fileHTML =preg_replace("/_out\.out$/", ".src", $fileHTML);
                   $failedTestsString = $failedTestsString."<div>".$fileHTML."</div>";
                }
            }

            if($noClean != 1)
            {
                $command = "rm -f $outputFile $intOutputFile";
                shell_exec($command);
            }
            
        }
    }



    $html = "<!DOCTYPE html>
    <html lang=\"en\">
    <head>
        <meta charset=\"UTF-8\">
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
        <link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">
        <link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>
        <link href=\"https://fonts.googleapis.com/css2?family=Fredoka:wght@300;400;500&display=swap\" rel=\"stylesheet\">
        <title>IPP project 2022</title>

        <style>
            *{
                box-sizing: border-box;
                margin: 0;
                padding: 0;
                font-size: 16px;
                color: black;
                font-family:\'Fredoka\',Arial, sans-serif;
            }

            #header{
                margin:3% 20%;
                width: 60%;
                height: 20vh;
                background-color: #eed8a9af;
                text-align: center;
                position: relative;
                border-radius: 30px;
                padding-top: 0.5vh;
                box-shadow: 5px 5px 10px #AAAAAA;
            }

            #header h1{
                font-size: 2.5em;
                margin-bottom: 2%;
                margin-top: 2%;
            }

            #header p{
                font-size: 1.4em;
            }

            #header div{
                display: flex;
                justify-content: center;
                align-items: center;
                flex-direction: row;
                column-gap: 5%;
                
            }
            
            #author{
                width: 100%;
                font-size: 1.2em;
            }

            #testBox{
                position: relative;
                display: flex;
                justify-content: space-between;
                flex-wrap: wrap;
                align-items: center;
                margin: 5% 10% 12% 10%;
                width: 80%;
                column-gap: 10%;
                height: 80vh;
            
            }


            #testBox h1{
                font-size: 2em;
                width: 100%;
                text-align: center;
                margin-bottom: 5vh;
                font-weight: 500;
            }

            #testBox h2{
                font-size: 1.5em;
                width: 100%;
                text-align: center;
                margin-bottom: 5%;
                font-weight: 500;
            }

            .Meter{
                width: 100%;
                display: flex;
                justify-content: center;
                margin-bottom: 5vh;
            }

            .Meter meter{
                width: 20%;
            }

            

            .correct{
                width: 45%;
                position: relative;
                background-color: rgb(191, 255, 194);
                border-radius: 30px;
                height: 100%;
                overflow: auto;
                padding-top: 3vh;
                padding-bottom: 1vh;
            }
            
            .incorrect{
                width: 45%;
                position: relative;
                background-color: rgb(255, 180, 180);
                border-radius: 30px;
                height: 100%;
                overflow: auto;
                padding-top: 3vh;
                padding-bottom: 1vh;
            }

            .correct div, .incorrect div{
                width: 80%;
                margin-left: 10%;
                margin-right:10%;
                height: 4vh;
                border-bottom: #555555 1px solid;
                line-height: 4vh;
            }

            ::-webkit-scrollbar {
            width: 8px;
            }

            ::-webkit-scrollbar-track {
                background: #eee;
                border-radius: 10px;  
            }
            
            ::-webkit-scrollbar-thumb {
                background: #aaa; 
                border-radius: 10px; 
            }

            ::-webkit-scrollbar-thumb:hover {
            background: #777; 
            }


        </style>
    </head>
    <body>
        <div id=\"header\">
            <h1>IPP project 2022</h1>
            <div>
                <p>Correct answers: $correctTests/$srcCounter</p>
                <meter id=\"correctAnswers\" value=\"$correctTests\" min=\"0\" max=\"$srcCounter\"> 
            </div>
            <div id=\"author\">
                Author: Dalibor Králik - xkrali20
            </div>
        </div>
        <div id=\"testBox\">
            <h1>$testingPart tests $correctTests/$srcCounter</h1>
            <div class=\"Meter\">
                <meter value=\"$correctTests\" min=\"0\" max=\"$srcCounter\"></meter>
            </div>
            <div class=\"correct\">
                <h2>Correct</h2>
                $correctTestsString
                
            </div>
            <div class=\"incorrect\">
                <h2>Incorrect</h2>
                $failedTestsString
            </div>
        </div>
        
    </body>
    </html>";

    echo $html;


}





processArgument();
runTimeOfProgram();

?>
