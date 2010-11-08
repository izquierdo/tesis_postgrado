<?php

################################################################################
# Filenames
################################################################################

$file_prefix = "/home/idaniel/tesis_postgrado/demo_ex/";

$services_files = array(
    $file_prefix . "services0.txt",
    $file_prefix . "services1.txt",
    $file_prefix . "services2.txt",
    $file_prefix . "services3.txt",
    $file_prefix . "services4.txt",
);

$queries_files = array(
    $file_prefix . "query0.txt",
    $file_prefix . "query1.txt",
    $file_prefix . "query2.txt",
    $file_prefix . "query3.txt",
);

$ontologies_files = array(
    $file_prefix . "ontology0.txt",
    $file_prefix . "ontology1.txt",
    $file_prefix . "ontology2.txt",
);

$preferences_files = array(
    $file_prefix . "preferences0.txt",
    $file_prefix . "preferences1.txt",
    $file_prefix . "preferences2.txt",
);

################################################################################
# File contents
################################################################################

$services_text = array();
$queries_text = array();
$ontologies_text = array();
$preferences_text = array();

foreach ($services_files as $f)
{
    array_push($services_text, file_get_contents($f));
}

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
#

#TODO creo que esto no se usa. verificar y borrar en ese caso
$services = array(
    array("name" => "0", "text" => "servicios0"),
    array("name" => "1", "text" => "servicios1"),
    array("name" => "2", "text" => "servicios2"),
    array("name" => "3", "text" => "servicios3"),
    );

$ontologies = array(
    array("name" => "0", "text" => "ontologia0"),
    array("name" => "1", "text" => "ontologia1"),
    array("name" => "2", "text" => "ontologia2"),
    array("name" => "3", "text" => "ontologia3"),
    );

$preferences = array(
    array("name" => "1", "text" => "preferencia0"),
    array("name" => "2", "text" => "preferencia1"),
    array("name" => "3", "text" => "preferencia2"),
    );
