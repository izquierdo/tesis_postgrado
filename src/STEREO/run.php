<?php include 'include/data.php'; ?>
<?php include 'include/header.html'; ?>

<?php

function RunSsdsat($queryfile, $viewfile, $ontologyfile)
{
    global $outputfilenames;

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

$s = $_GET["services"];
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
          $result = RunSsdsat($queries_files[intval($q)], $services_files[intval($s)], $ontologies_files[intval($o)]);
      else
          $result = RunSsdsatBest($queries_files[intval($q)], $services_files[intval($s)], $ontologies_files[intval($o)], $preferences_files[intval($p)]);
?>

<h2>
<?php
      if ($all)
          echo "All rewritings for selected instance:";
      else
          echo "Best rewriting for selected instance:";
?>
</h2>

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

      $lines = explode("\n", $result);
      $number_results = count($lines)-1;

      $model_count = (int) trim(file_get_contents($outputfilenames . ".out.count"));
?>

<div style="border-style: dashed; border-width: 1px; width: 100%">

<?php
      echo nl2br($result);
?>

</div><br/>

<?php
      echo "Showing <strong>$number_results</strong> out of <strong>$model_count</strong> total rewritings.<br/>";
      echo "Results obtained in <strong>$rounded</strong> seconds.<br/>";

      $number_results = 1;
      $model_count = 2;

      if ($number_results < $model_count)
      {
          $time_mymodels = (double) trim(file_get_contents($outputfilenames . ".out.time"));
          $time_allmodels = max(((double)$model_count)/((double)$number_results) * $time_mymodels, 0);
          echo "Estimated time needed to enumerate all results: <strong>$time_allmodels</strong> seconds.<br/>";
      }
?>

<br/>

<?php
      $dlfiles = basename($outputfilenames);
?>

<ul>
<li>Download the <a href="<?php echo "/STEREO/download/$dlfiles.out"; ?>">human-readable CNF theory and program output</a></li>
<li>Download the generated <a href="<?php echo "/STEREO/download/$dlfiles.cnf"; ?>">CNF file</a> for this instance</li>
<li>Download the compiled <a href="<?php echo "/STEREO/download/$dlfiles.cnf.nnf"; ?>">NNF file</a></li>
</ul>

<?php include 'include/footer.html'; ?>
