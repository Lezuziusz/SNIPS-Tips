<?php
include('/var/www/html/core/class/scenario.class.php');


$snipsip = '192.168.x.y';
$sshlogin = 'my.ssh.login.to.the.pi';
$sshpass = 'mypass';

if (isset($argv)) {
	foreach ($argv as $arg) {
		$argList = explode('=', $arg);
		if (isset($argList[0]) && isset($argList[1])) {
			$_GET[$argList[0]] = $argList[1];
		}
	}
}
$action = 'default';
if(isset($_GET['action'])) $action = $_GET['action'];
if ($action != 'default') call_user_func($action);


//===========actions:
function speak()
{
	$title = $_GET['title'];
    $message = $_GET['message'];
  	$message = evalDynamicString($message);
	speakNow($message);
}

//=====functions:
function speakNow($message)
{
  	$cmd = cmd::byString('#[Snips-Intents][Snips-TTS-default][say]#');
    $cmd->execCmd($options=array('title'=>'', 'message'=>$message), $cache=0);
}

function evalDynamicString($_string)
{
	if (strpos($_string, '{') !== false AND strpos($_string, '}') !== false)
	{
		try {
			preg_match_all('/{(.*?)}/', $_string, $matches);
			foreach ($matches[0] as $expr_string)
			{
				$expr = substr($expr_string, 1, -1);
				$exprAr = explode('|', $expr);
				$value = $exprAr[0];
				array_shift($exprAr);

				$valueString = '';
				foreach ($exprAr as $thisExpr)
				{
					$evaluateString = 'return ';
					$parts = explode(':', $thisExpr);
					if ( $parts[0][0] != '<' AND $parts[0][0] != '>') $parts[0] = '=='.$parts[0];

					$test = eval("return ".$value.$parts[0].";");
					if ($test)
					{
					     $valueString = $parts[1];
					}

					if ($valueString != '') break;
				}

				$_string = str_replace($expr_string, $valueString, $_string);
			}

			return $_string;
		} catch (Exception $e) {
			return $_string;
		}
	}
	else return $_string;
}

?>