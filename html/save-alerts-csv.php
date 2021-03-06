<?php
session_start();

include_once 'includes/functions.php';

$data = array("target" => "alerts");
$result = CallAPI('POST', 'http://127.0.0.1:5000/api/v1.0/falcongate/status', json_encode($data));
if (!$result){
    echo ("<h3>FalconGate API process seems to be down!</h3>");
    echo ("<h3>Check your device's configuration and reboot if necessary.</h3>");
}else{
    // Based on code from Stephen Morley
    // http://code.stephenmorley.org/php/creating-downloadable-csv-files/
    header('Content-Type: text/csv; charset=utf-8');
    header('Content-Disposition: attachment; filename=recent_alerts_'.date('Y-m-d').'.csv');

    // create a file pointer connected to the output stream
    $output = fopen('php://output', 'w');
    
    // output the column headings
    fputcsv($output, array('First seen', 'Last seen', 'Host', 'Threat', 'Indicators'));
    
    $obj = json_decode($result, true);
    
    // fetch the data
    if ($obj[0] != 'none'){
        foreach ($obj as $alert){
            $nextrow = array();
            $nextrow[0] = date('Y/m/d H:i:s', $alert['alerts']['first_seen']);
            $nextrow[1] = date('Y/m/d H:i:s', $alert['alerts']['last_seen']);
            $nextrow[2] = $alert['host'];
            $nextrow[3] = $alert['alerts']['threat'];
            $nextrow[4] = implode(",", $alert['alerts']['indicators']);
            fputcsv($output, $nextrow);
        }
    }
}
?>