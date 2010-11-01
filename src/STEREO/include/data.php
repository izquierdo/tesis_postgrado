<?php

################################################################################
# Filenames
################################################################################

$file_prefix = "/home/idaniel/ssdsat/demo_ex/";

$services_file = $file_prefix . "services.txt";

$queries_files = array(
    $file_prefix . "query1.txt",
    $file_prefix . "query2.txt",
    $file_prefix . "query3.txt",
);

$ontologies_files = array(
    $file_prefix . "ontology1.txt",
    $file_prefix . "ontology2.txt",
    $file_prefix . "ontology3.txt",
);

$preferences_files = array(
    $file_prefix . "preferences1.txt",
    $file_prefix . "preferences2.txt",
    $file_prefix . "preferences3.txt",
);

################################################################################
# File contents
################################################################################

$services_text = file_get_contents($services_file);

$queries_text = array();
$ontologies_text = array();
$preferences_text = array();

foreach ($queries_files as $f)
{
    array_push($queries_text, file_get_contents($f));
}

foreach ($ontologies_files as $f)
{
    array_push($ontologies_text, file_get_contents($f));
}

foreach ($preferences_files as $f)
{
    array_push($preferences_text, file_get_contents($f));
}

################################################################################
# Data
################################################################################

$ontologies = array(
    array("name" => "0", "text" => "ontologia1"),
    array("name" => "1", "text" => "ontologia2"),
    array("name" => "2", "text" => "ontologia3"),
    array("name" => "3", "text" => "ontologia4"),
    );

$preferences = array(
    array("name" => "1", "text" => "preferencia1"),
    array("name" => "2", "text" => "preferencia2"),
    array("name" => "3", "text" => "preferencia3"),
    );

?>
