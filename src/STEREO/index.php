<?php include 'include/data.php'; ?>
<?php include 'include/header.html'; ?>

<?php
/*********************************************************************
    SERVICES
*********************************************************************/
?>

<div id="services">

<form action="run.php" method="GET">

<h2>Services</h2>

<div style="border-style: solid; border-width: 1px; padding: 5px;">
<?= nl2br($services_text) ?>
</div>

</div>

<?php
/*********************************************************************
    QUERY
*********************************************************************/
?>

<div id="query">

<h2>Query</h2>

<select name="query">
<?php
$i = 0;

foreach ($queries_text as $q) {
?>

    <option value="<?= $i ?>"><?= $q ?></option>

<?php
    $i = $i + 1;
}
?>
</select>

<!---------------------------------------------------------------------------->

<h2>Ontology</h2>

<div id="ontology_select" style="padding: 5px;">

<?php
foreach ($ontologies as $ontology) {
?>

<?= $ontology["name"] ?>

<input type="radio" name="ontology" value="<?= $ontology["name"] ?>" onclick="displayOntology('<?= $ontology["text"] ?>')" />
<br/>

<?php
}
?>

</div>

<div id="ontology_display" style="border-style: solid; border-width: 1px; padding: 5px; display: none;">
</div>

<!---------------------------------------------------------------------------->

<h2>Preferences</h2>

<div id="preference_select" style="padding: 5px;">

<?php
$i = 0;

foreach ($preferences_text as $e) {
?>

<?= $i ?>
<input type="radio" name="preference" value="<?= $i ?>" onclick="displayPreference('<?= preg_replace("/[\n\r]/","",nl2br($e)) ?>')" />
<br/>

<?php
    $i = $i + 1;
}
?>

</div>

<div id="preference_display" style="border-style: solid; border-width: 1px; padding: 5px; display: none;">
</div>

<!---------------------------------------------------------------------------->

<br/>
<br/>

<input type="submit" name="run" value="All rewritings"/>
<input type="submit" name="run" value="Best rewriting"/>

</form>

</div>

<?php include 'include/footer.html'; ?>
