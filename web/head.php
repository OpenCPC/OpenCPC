<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
	<link rel="stylesheet" href="css/linedtextarea.css">
	<link rel="stylesheet" href="css/base.css">
	<link rel="stylesheet" href="css/addl.css">
	<link rel="stylesheet" href="css/admin_page.css">
	<link rel="stylesheet" href="css/competitionpage.css">
	<link rel="stylesheet" href="css/main_page.css">
	<link rel="stylesheet" href="css/loginpage.css">
	<link rel="stylesheet" href="css/header.css">
	<script src="js/utility.js"></script>
	<script src="js/client.js"></script>
	<script src="js/login.js"></script>
	<script src="js/mainmenu.js"></script>
	<script src="js/linedtextarea.js"></script>
 	<script src="js/competition.js"></script>
	<script src="js/section.js"></script>
	<script src="js/sidebar.js"></script>
	<script src="js/admin.js"></script>
	<script src="js/compstatus.js"></script>
	<script src="js/resetPassword.js"></script>
	
	<style>
		<?php for ($i=0; $i<16; $i++) {
			echo "


			.loadingSpinnerContainer>.rect".$i." {
				width: 5px;
				height: 40px;
				background-color: white;
				position: absolute;
				left: 50px;
				top: 50px;
				animation: loadingSpinnerAnimation".$i."1.0s infinite;
				-webkit-animation: loadingSpinnerAnimation".$i."1.0s infinite;
				animation-delay: ".($i*2/16)."s;
				-webkit-animation-delay: ".($i*2/16)."s;
				transform: rotate(".($i*360.0/16)."deg) scaleY(0.5) translate(0px, 70px);
				-webkit-transform: rotate(".($i*360.0/16)."deg) scaleY(0.5) translate(0px, 70px);
			}

			/* loading circle animation */
			@keyframes loadingSpinnerAnimation".$i." {

				0%,
				30%,
				70%,
				100% {
					transform: rotate(".($i*360.0/16)."deg) scaleY(0.5) translate(0px, 70px);
					-webkit-transform: rotate(".($i*360.0/16)."deg) scaleY(0.5) translate(0px, 70px);
				}

				50% {
					transform: rotate(".($i*360.0/16)."deg) scaleY(2.0) translate(0px, 70px);
					-webkit-transform: rotate(".($i*360.0/16)."deg) scaleY(2.0) translate(0px, 70px);
				}
			}

			";

		}

		?>
	</style>