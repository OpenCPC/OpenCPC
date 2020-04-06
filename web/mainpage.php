<div id='main_menu'>
	<h1>
		MCSC - Menu
	</h1>
	<h3>
		Select practice or competition session.
	</h3>
	<div class='rename_me_later_please'>
		<button onclick='mainMenuPractice();' class='header_button'>
			Practice
		</button><!--
		--><button onclick='mainMenuCompete();' class='header_button'>
			Compete
		</button>
		<div id='main_menu_practice'>
			<div onclick='openCreateComp("prac");' id='createPracButton' class="btn btn-primary">
				Add a Practice Competition
			</div>
			<div class='practice_header_name'>
				Practice
			</div>
			<div id='main_menu_practice_list'>
			</div>
		</div>
		<div id='main_menu_compete'>
			<div onclick="openCreateComp('comp');" id='createCompButton' class="btn btn-primary">
				Create Your Own Competition!
			</div>
			<br><br>
			<div id="compete_header_name">
				Compete
			</div>
			<div id='main_menu_compete_list'>
			</div>
		</div>
	</div>
	<br>
	<div class='submission_processing_servers_area'>
		<div>
			<div>
				Submission Processing Servers
			</div>
			<div id='main_menu_sps'>
			</div>
		</div>
	</div>
	<div id='createCompPage'>
	</div>
</div>