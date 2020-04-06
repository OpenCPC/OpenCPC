<?php
    require("config.php");
    try {
        $conn = new PDO(
            $GLOBALS["DATABASE_HOST"],
            $GLOBALS["DATABASE_USER"],
            $GLOBALS["DATABASE_PASS"]
        );
        $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        ini_set('display_errors',1);
        error_reporting(E_ALL);

        $keyv = $_GET['compkey'];//replace with post
        $imgid = $_GET['imgid'];//replace with post
        
        $type = "large";
        if($_GET['type'] == "admin")
            $type = "small";
        
        $authComp = $conn->prepare("SELECT id FROM competitions WHERE competitionkey=:competitionkey");
        $authComp->bindParam(":competitionkey", $keyv);
        $authComp->execute();

        $authImg = $conn->prepare("SELECT competitionid, fileextension, filename FROM images WHERE id=:imgid");
        $authImg->bindParam(":imgid", $imgid);
        $authImg->execute();

        if ($authComp->rowCount() == 0) {
            die("Failed to find comp key");
        }

        if ($authComp->rowCount() > 1) {
            die("Comp key duplicates");
        }

        if ($authImg->rowCount() == 0) {
            die("Failed to find image id");
        }

        if ($authImg->rowCount() > 1) {
            die("Image id duplicates");
        }
        

        $authCompRow = $authComp->fetch(PDO::FETCH_ASSOC);
        $authImgRow = $authImg->fetch(PDO::FETCH_ASSOC);

        if ($authCompRow['id'] != $authImgRow['competitionid']) {
            die("Failed to authenticate");
        }


        $currentfeheader = "";
        if ($authImgRow['fileextension']=="jpg")
            $currentfeheader = "jpeg";
        else if ($authImgRow['fileextension']=="jpeg")
            $currentfeheader = "jpeg";
        else if ($authImgRow['fileextension']=="png")
            $currentfeheader = "png";
        else if ($authImgRow['fileextension']=="gif")
            $currentfeheader = "gif";
        else
            die("unsupported file type");

        if (!file_exists("/var/mcsc/imgs/".$authImgRow["filename"]."_".$type.".".$authImgRow["fileextension"]))
            die("System error: failed to find image");

        if (
            strpos($authImgRow["filename"],"/") !== FALSE
            || strpos($authImgRow["filename"],"\\") !== FALSE
            || strpos($authImgRow["fileextension"],"/") !== FALSE
            || strpos($authImgRow["fileextension"],"\\") !== FALSE
        )
            die("Invalid format of filename and fileextension");

        header('Content-Type: image/'.$currentfeheader);
        readfile("/var/mcsc/imgs/".$authImgRow["filename"]."_".$type.".".$authImgRow["fileextension"]);


    }
    catch (PDOException $e) {
        echo $e->getMessage();
    }


?>