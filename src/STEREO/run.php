<?php include 'data.php'; ?>

<html>
<head>
    <title>
        STEREO results
    </title>

    <link rel="stylesheet" href="http://www.izquierdo.com.ve/stereo_media/css/style.css" type="text/css">
</head>

<?php

function RunSsdsat($queryfile, $viewfile)
{
    $program = "/usr/local/bin/python /home/idaniel/ssdsat/driver.py -t RW -q $queryfile -v $viewfile";

    $descriptorspec = array(
            0 => array("pipe", "r"),
            1 => array("pipe", "w"),
            2 => array("pipe", "w")
            );

    $cwd = NULL;

    $env = array();

    $process = proc_open($program, $descriptorspec, $pipes, $cwd, $env);

    if (is_resource($process))
    {
        fclose($pipes[0]);

        $error = stream_get_contents($pipes[2]);
        $result = stream_get_contents($pipes[1]);
        fclose($pipes[1]);
        fclose($pipes[2]);

        $return_value = proc_close($process);
    }

    return $result;
}

function RunSsdsatBest($queryfile, $viewfile, $preffile)
{
    $program = "/usr/local/bin/python /home/idaniel/ssdsat/driver.py -t BESTRW -q $queryfile -v $viewfile -p $preffile";

    $descriptorspec = array(
            0 => array("pipe", "r"),
            1 => array("pipe", "w"),
            2 => array("pipe", "w")
            );

    $cwd = NULL;

    $env = array();

    $process = proc_open($program, $descriptorspec, $pipes, $cwd, $env);

    if (is_resource($process))
    {
        fclose($pipes[0]);

        $error = stream_get_contents($pipes[2]);
        $result = stream_get_contents($pipes[1]);
        fclose($pipes[1]);
        fclose($pipes[2]);

        $return_value = proc_close($process);
    }

    return $result;
}
?>

<?php

$q = $_GET["query"];
$o = $_GET["ontology"];
$p = $_GET["preference"];

if ($_GET["run"] == "All rewritings")
    $all = true;
else
    $all = false;
?>

<?php
/********************************************************************************* 
    BEGIN TIMING
 *********************************************************************************/

      $mtime = microtime();
      $mtime = explode(' ', $mtime);
      $mtime = $mtime[1] + $mtime[0];
      $starttime = $mtime;
?>

<?php
/********************************************************************************* 
    SSDSAT
 *********************************************************************************/

      if ($all)
          $result = RunSsdsat($queries_files[intval($q)], $services_file);
      else
          $result = RunSsdsatBest($queries_files[intval($q)], $services_file, $preferences_files[intval($p)]);
?>

<?php
/********************************************************************************* 
    END TIMING
 *********************************************************************************/
      $mtime = microtime();
      $mtime = explode(" ", $mtime);
      $mtime = $mtime[1] + $mtime[0];
      $endtime = $mtime;
      $totaltime = ($endtime - $starttime);
      $rounded = round($totaltime, 3);

      echo nl2br($result);
      echo "Results obtained in $rounded seconds.";
?>
