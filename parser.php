<?php
ini_set('display_errors', 'stderr');
include "./programArguments.php";





$xml = new XMLWriter();
$xml->openMemory();

processArgument();
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
        ['QT', 'var', 'symb', 'symb'],
        ['EQ', 'var', 'symb', 'symb'],
        ['AND', 'var', 'symb', 'symb'],
        ['OR', 'var', 'symb', 'symb'],
        ['NOT', 'var', 'symb', 'symb'],
        ['INT2CAHR', 'var', 'symb'],
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
        ['JUMPOFQE', 'label', 'symb', 'symb'],
        ['JUMPIFNEQ', 'label', 'symb', 'symb'],
        ['EXIT', 'symb'],
        ['DPRINT', 'symb'],
        ['BREAK']
    ];


function argumentPoccessing($xml, $inputArray, $operationCodeLine)
{
    if(count($inputArray) != count(operationCode[$operationCodeLine]))
    {
        fwrite(STDERR, "ERROR 23 - Other lexicalor syntax ERROR -> non-equal correct parameters number\n");
        exit(23);
    }
    
    for($i = 1; $i < count($inputArray); $i++)
    {
        if(operationCode[$operationCodeLine] == 'var')
        {
            if(preg_match('/^(GF|TF|LF)@[a-zA-Z0-9_\-\$&%\*\!\?]+$/', $inputArray[$i]))
            {

            }
            else
            {
                fwrite(STDERR, "ERROR 23 - Other lexicalor syntax ERROR -> invalid variable\n");
                exit(23);
            }
            //TODO extrakcia do XML

        }
        else if(operationCode[$operationCodeLine] == 'symb')
        {
            
            
        }
        else if(operationCode[$operationCodeLine] == 'label')
        {
            if(preg_match('/^[a-zA-Z0-9_\-\$&%\*\!\?]+$/', $inputArray[$i]))
            {

            }
            else
            {
                fwrite(STDERR, "ERROR 23 - Other lexicalor syntax ERROR -> invalid label\n");
                exit(23);
            }
            //TODO extrakcia do XML
        }

    }


}


function startOfXML($xml)
{
    $xml->startDocument('1.0', 'UTF-8');
    $xml->startElement('program');
    $xml->writeAttribute('language', 'IPPcode22');
    return $xml;

}    


function endOfXML($xml)
{
    $xml->endElement();
    $xml->endDocument();
    file_put_contents('output.xml', $xml->outputMemory());
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
 * regex prazdenho riadku s komentom: '/(^\s+#|^#|^\s+\s$)/'
 */





while(($line = fgets(STDIN)) != false)
{
    if(!$IDheader)
    {
        if(preg_match('/(^\s*.IPPcode22\s*(\s$|#)|^\s*.IPPcode22$)/i', $line))
        {
            $IDheader = true;
            $numberOfLine++;
            fwrite(STDERR, "Header loaded successfully: $numberOfLine\n");
            //TODO generovanie zakladneho XML - hlavicka a struktura

            $xml = startOfXML($xml);
            


        }
        else  if(preg_match('/(^\s+#|^#|^\s+\s$)/i', $line))
        {
            // znaci prazdny riadok
            fwrite(STDERR, "Empty line: $numberOfLine\n");
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
        $inputArray = preg_replace('/#.*/','', $line);

            //Ak sa jedna o prazdny riadok, tak skip
        if(preg_match('/(^\s+#|^#|^\s+\s$)/i', $line, $matches))
        {
            //SKIP
        }
        else{
                //rozdelenie vstupneho riadku do pola podla bielych znakov, komentare su uz v tomto momente odstranene
            $inputArray = preg_split('/[\s+]/', $inputArray, -1, PREG_SPLIT_NO_EMPTY);
         
            $validOperationReturn = validOperationCode($inputArray[0]);
            $opcode = $validOperationReturn[0];
                //Skontrolovanie operaceho kodu
            if($validOperationReturn[1] == -1)
            {
                fwrite(STDERR, "ERROR 21 - Bad or unknown operation code in source file\n");
                exit(22);
            }
            
                //XML spracovanie instrukcie
            $xml->startElement('instruction');
            $xml->writeAttribute('order', $numberOfLine);
            $xml->writeAttribute('opcode', $opcode);

                //XML spracovanie argumentu

            argumentPoccessing($xml, $inputArray, $validOperationReturn[1]);
            

            $xml->endElement();
            $numberOfLine++;
        }
     
    }





}

endOfXML($xml);




?>