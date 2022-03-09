<?php
/**
 * Project: IPP22
 * @author Dalibor Kralik, xkrali20
 * @brief Module which process program arguments
 * 
 * @file parse.php
 */

ini_set('display_errors', 'stderr');



$xml = new XMLWriter();
$xml->openMemory();

$IDheader = false;
$numberOfLine = 0;
const operationCode = [
        ['MOVE','var', 'symb'],
        ['CREATEFRAME'],
        ['PUSHFRAME'],
        ['POPFRAME'],
        ['DEFVAR','var'],
        ['CALL','label'],
        ['RETURN'],
        ['PUSHS','symb'],
        ['POPS','var'],
        ['ADD', 'var', 'symb', 'symb'],
        ['SUB', 'var', 'symb', 'symb'],
        ['MUL', 'var', 'symb', 'symb'],
        ['IDIV', 'var', 'symb', 'symb'],
        ['LT', 'var', 'symb', 'symb'],
        ['GT', 'var', 'symb', 'symb'],
        ['EQ', 'var', 'symb', 'symb'],
        ['AND', 'var', 'symb', 'symb'],
        ['OR', 'var', 'symb', 'symb'],
        ['NOT', 'var', 'symb'],
        ['INT2CHAR', 'var', 'symb'],
        ['STRI2INT', 'var', 'symb', 'symb'],
        ['READ', 'var', 'type'],
        ['WRITE', 'symb'],
        ['CONCAT','var', 'symb', 'symb'],
        ['STRLEN','var', 'symb'],
        ['GETCHAR','var', 'symb', 'symb'],
        ['SETCHAR','var', 'symb', 'symb'],
        ['TYPE','var', 'symb'],
        ['LABEL', 'label'],
        ['JUMP', 'label'],
        ['JUMPIFEQ', 'label', 'symb', 'symb'],
        ['JUMPIFNEQ', 'label', 'symb', 'symb'],
        ['EXIT', 'symb'],
        ['DPRINT', 'symb'],
        ['BREAK']
    ];

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



/**
 * @brief Function which replace invalid XML characters in string with valid escape sequence
 * @param $inputString - input string which can contain invalid cahracters for XML
 * @return $inputString - string which contains only valid characters for XML
 */
function replaceInvalidXML($inputString)
{
    preg_replace('/</', "&lt;", $inputString);
    preg_replace('/>/', "&gt;", $inputString);
    preg_replace('/&/', "&amp;", $inputString);
    preg_replace('/"/', "&quot;", $inputString);
    preg_replace('/\'/', "&apos;", $inputString);
    
    return $inputString;
}


/**
 * @brief Function which proccess arguments of operation instructions
 */
function argumentPoccessing($xml, $inputArray, $operationCodeLine)
{
        // Check if inputArray has same lenght as array in operationCode constant
    if(count($inputArray) != count(operationCode[$operationCodeLine]))
    {
        fwrite(STDERR, "ERROR 23 - Other lexicalor syntax ERROR -> non-equal correct parameters number\n");
        exit(23);
    }

        // Proccessing non-argument operation code fomr IPPCode22
    if(count($inputArray) == 1)
    {
        return $xml;
    }

        // Proccessing arguments
    for($i = 1; $i < count($inputArray); $i++)
    {
        if(operationCode[$operationCodeLine][$i] == 'var')
        {
            if(preg_match('/^(GF|TF|LF)@[ěščřžýáíéóúůďťňĎŇŤŠČŘŽÝÁÍÉÚŮĚÓa-zA-Z_\-\$&%\*\!\?][ěščřžýáíéóúůďťňĎŇŤŠČŘŽÝÁÍÉÚŮĚÓa-zA-Z0-9_\-\$&%\*\!\?]*$/', $inputArray[$i]))
            {
                    //replace invalid XML characters to valid escape sequece
                $inputArray[$i] = replaceInvalidXML($inputArray[$i]);

                $xml->startElement("arg$i");
                $xml->writeAttribute('type', 'var');
                $xml->text($inputArray[$i]);
                $xml->endElement();
            }
            else
            {
                fwrite(STDERR, "ERROR 23 - Other lexical or syntax ERROR -> invalid variable\n");
                exit(23);
            }
        }
        else if(operationCode[$operationCodeLine][$i] == 'symb')
        {
            if(preg_match('/^(GF|TF|LF)@[ěščřžýáíéóúůďťňĎŇŤŠČŘŽÝÁÍÉÚŮĚÓa-zA-Z_\-\$&%\*\!\?][ěščřžýáíéóúůďťňĎŇŤŠČŘŽÝÁÍÉÚŮĚÓa-zA-Z0-9_\-\$&%\*\!\?]*$/', $inputArray[$i]))
            {
                    //replace invalid XML characters to valid escape sequece
                $inputArray[$i] = replaceInvalidXML($inputArray[$i]);

                $xml->startElement("arg$i");
                $xml->writeAttribute('type', 'var');
                $xml->text($inputArray[$i]);
                $xml->endElement();
            }
            else if(preg_match('/^string@([^\s#\\\\]|\\\\\d{3})*$/', $inputArray[$i]) ||
                    preg_match('#^nil@nil$#', $inputArray[$i]) ||
                    preg_match('#^bool@(true|false)$#', $inputArray[$i]) ||
                    preg_match('#^int@[-+]?[0-9]+$#', $inputArray[$i]))
            {
                    //replace invalid XML characters to valid escape sequece
                $inputArray[$i] = replaceInvalidXML($inputArray[$i]);
                
                $split = preg_split('/@/',$inputArray[$i], 2, PREG_SPLIT_NO_EMPTY);
                $xml->startElement("arg$i");
                $xml->writeAttribute('type', $split[0]);
                if(count($split) < 2)
                {
                    $xml->text('');
                }
                else
                {
                    $xml->text($split[1]);
                }
                $xml->endElement();
            }
            else
            {
                fwrite(STDERR, "ERROR 23 - Other lexical or syntax ERROR -> invalid symb\n");
                exit(23);
            }
        }
        else if(operationCode[$operationCodeLine][$i] == 'label')
        {
            if(preg_match('/^[ěščřžýáíéóúůďťňĎŇŤŠČŘŽÝÁÍÉÚŮĚÓa-zA-Z_\-\$&%\*\!\?][ěščřžýáíéóúůďťňĎŇŤŠČŘŽÝÁÍÉÚŮĚÓa-zA-Z0-9_\-\$&%\*\!\?]*$/', $inputArray[$i]))
            {
                $xml->startElement("arg$i");
                $xml->writeAttribute('type', 'label');
                $xml->text($inputArray[$i]);
                $xml->endElement();
            }
            else
            {
                fwrite(STDERR, "ERROR 23 - Other lexical or syntax ERROR -> invalid label\n");
                exit(23);
            }
        }
        else if(operationCode[$operationCodeLine][$i] == 'type')
        {
            if(preg_match('/^(nil|int|bool|string)$/', $inputArray[$i]))
            {
                $xml->startElement("arg$i");
                $xml->writeAttribute('type', 'type');
                $xml->text($inputArray[$i]);
                $xml->endElement();
            }
            else
            {
                fwrite(STDERR, "ERROR 23 - Other lexical or syntax ERROR -> invalid type\n");
                exit(23);
            }
        }
    }
    return $xml;
}


/**
 * @brief Function which create header of new XML file
 * @param $xml
 * @return $xml - XML which contains correct header
 */
function startOfXML($xml)
{
    $xml->startDocument('1.0', 'UTF-8');
    $xml->startElement('program');
    $xml->writeAttribute('language', 'IPPcode22');
    return $xml;

}    


/**
 * @brief Function which end XML correctly
 * @param $xml
 */
function endOfXML($xml)
{
    $xml->endElement();
    $xml->endDocument();
    fwrite(STDOUT,$xml->outputMemory());
}    


/**
 * @brief Function tests if loaded operation code is valid
 * @param $code - string which has value of operation code
 * @return array(strtoupper($code): string, bool - true if find, false if not find)
 */
function validOperationCode($code)
{
    $i = 0;
    foreach(operationCode as $lineOfArray)
    {
        
        if(!(array_search(strtoupper($code), $lineOfArray) === false))
            break;
        $i++;
    }
    return array(strtoupper($code), $i<35 ? $i : -1);
}


/**
 * @brief Here is MAIN section of whole parser.php
 * 
 * Prebieha tu while cyklus, ktory nacitava vstup riadok po riadku
 */
processArgument();
while(($line = fgets(STDIN)) != false)
{
    if(!$IDheader)
    {
        $lineWithoutHastag = preg_replace('/#.*/',' ', $line);
        if(preg_match('/(^\s*.IPPcode22\s*(\s$|#)|^\s*.IPPcode22$)/i', $line))
        {
            $IDheader = true;
            $numberOfLine++;
            //fwrite(STDERR, "Header loaded successfully: $numberOfLine\n");
                
                //Generovanie zakladneho XML
            $xml = startOfXML($xml);
        }
        else  if(preg_match('/(^\s+$)/i', $lineWithoutHastag))
        {
            // znaci prazdny riadok
            //fwrite(STDERR, "Empty line: $numberOfLine\n");
        }
        else
        {
            fwrite(STDERR, "ERROR 21 - Missing or bad header\n");
            exit(21);
        }  
    
    }
    else
    {
            //odstranenie komentaru z nacitaneho riadku, komentar nebudem nidky potrebovat
        $inputArray = preg_replace('/#.*/',' ', $line);

            //Ak sa jedna o prazdny riadok, tak skip
        if(preg_match('/(^\s+$)/i', $inputArray))
        {
            //SKIP
        }
        else{
                //rozdelenie vstupneho riadku do pola podla bielych znakov, komentare su uz v tomto momente odstranene
            $inputArray = preg_split('/[\s]+/', $inputArray, -1, PREG_SPLIT_NO_EMPTY);
         
            $validOperationReturn = validOperationCode($inputArray[0]);
            $opcode = $validOperationReturn[0];
                //Skontrolovanie operaceho kodu
            if($validOperationReturn[1] == -1)
            {
                fwrite(STDERR, "ERROR 22 - Bad or unknown operation code in source file\n");
                exit(22);
            }
            
                //XML spracovanie instrukcie
            $xml->startElement('instruction');
            $xml->writeAttribute('order', $numberOfLine);
            $xml->writeAttribute('opcode', $opcode);

                //XML spracovanie argumentu
            $xml = argumentPoccessing($xml, $inputArray, $validOperationReturn[1]);
            
            $xml->endElement();
            $numberOfLine++;
        }
    }
}

endOfXML($xml);

?>
