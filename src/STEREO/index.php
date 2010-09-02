<?php include 'data.php'; ?>

<html>
<head>
    <title>
        STEREO
    </title>

    <link rel="stylesheet" href="http://www.izquierdo.com.ve/stereo_media/css/style.css" type="text/css">

    <script language="javascript" type="text/javascript" src="http://www.izquierdo.com.ve/stereo_media/js/jquery-1.4.2.js"></script>
    <script language="javascript" type="text/javascript">
    function displayOntology(text) {
        $("#ontology_display").text(text).show();
    }

    function displayPreference(text) {
        $("#preference_display").html(text).show();
    }
    </script>
</head>

<!---------------------------------------------------------------------------->

<body>

<p>
    <img src="http://www.izquierdo.com.ve/stereo_media/images/cebolla.png" class="logo" />
    <h4 class="centrado">Universidad Sim&oacute;n Bol&iacute;var</h2>
    <h1 class="title">STEREO</h1>
</p>

<form action="run.php" method="GET">

<h2>Services</h2>

<div style="border-style: solid; border-width: 1px; padding: 5px;">
<?= nl2br($services_text) ?>
</div>

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

<?php
/*
?>


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
<?php
*/
?>


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

</body>
</html>
