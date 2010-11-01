<?php include 'include/data.php'; ?>
<?php include 'include/header.html'; ?>

<?php

function RunSsdsat($queryfile, $viewfile, $ontologyfile)
{
    $qb = basename($queryfile);
    $vb = basename($viewfile);
    $ob = basename($ontologyfile);

    #TODO move it from /tmp
    #$outputfilenames = "/home/idaniel/stereo_results/" . "stereo-$qb-$vb-$ob";
    $outputfilenames = "/tmp/stereo_results/" . "stereo-$qb-$vb-$ob";
    $program = "/usr/local/bin/python /home/idaniel/tesis_postgrado/src/ssdsat/driver.py -t RW -q $queryfile -v $viewfile -o $ontologyfile -d $outputfilenames.out -l $outputfilenames";

    $descriptorspec = array(
            0 => array("pipe", "r"),
            1 => array("pipe", "w"),
            2 => array("pipe", "w")
            );

    $cwd = "/home/idaniel/tesis_postgrado/src/ssdsat";

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

function RunSsdsatBest($queryfile, $viewfile, $ontologyfile, $preffile)
{
    $program = "/usr/local/bin/python /home/idaniel/tesis_postgrado/src/ssdsat/driver.py -t BESTRW -q $queryfile -v $viewfile -p $preffile -o $ontologyfile";

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
          $result = RunSsdsat($queries_files[intval($q)], $services_file, $ontologies_files[intval($o)]);
      else
          $result = RunSsdsatBest($queries_files[intval($q)], $services_file, $ontologies_files[intval($o)], $preferences_files[intval($p)]);
?>

<h2>
<?php
      if ($all)
          echo "All rewritings for selected instance:";
      else
          echo "Best rewriting for selected instance:";
?>
</h2><br/><br/>

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

<br/>

<ul>
<li>Download the <a href="">human-readable CNF file and debugging output</a></li>
<li>Download the generated <a href="">CNF file</a> for this instance</li>
<li>Download the compiled <a href="">NNF file</a></li>
</ul>

<?php include 'include/footer.html'; ?>
