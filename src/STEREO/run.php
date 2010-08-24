<?php include 'data.php'; ?>

<?php

$q = $_GET["query"];
$o = $_GET["ontology"];
$p = $_GET["preference"];

if ($_GET["run"] == "All rewritings")
    $all = true;
else
    $all = false;

echo "Consultando $q sobre ont $o y pref $p. Todas? $all";
?>
