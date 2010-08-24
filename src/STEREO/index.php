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
        $("#preference_display").text(text).show();
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
national(X1,X2) :- flight(X1,X2),uscity(X1),uscity(X2)<br/>
oneway(X3,X4) :- flight(X3,X4)<br/>
onestop(X1,X3) :- flight(X1,X2),flight(X2,X3)<br/>
</div>

<h2>Query</h2>

<select name="query">
  <option value="q1">q(X1,X2) :- flight(X1,X2),flight(X2,X1),uscity(X1)</option>
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
foreach ($preferences as $e) {
?>

<?= $e["name"] ?>

<input type="radio" name="preference" value="<?= $e["name"] ?>" onclick="displayPreference('<?= $e["text"] ?>')" />
<br/>

<?php
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
