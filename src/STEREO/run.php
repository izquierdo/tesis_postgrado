<?php include 'data.php'; ?>

<?php

function RunSsdsat($queryfile)
{
    $program = "/usr/local/bin/python /home/idaniel/ssdsat/demo -t RW -q $queryfile -v <TODO views>";

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
        #fwrite($pipes[0], $locationdatalist);
        fclose($pipes[0]);

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

echo "Consultando $q sobre ont $o y pref $p. Todas? $all";

echo "Running da " . RunSsdsat();

?>
