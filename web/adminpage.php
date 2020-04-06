<div id="admin_page">
    <div id='admin_overlay'>
        <h1 id="admin_overlayTitle">
            Loading...
        </h1>
        <h3 id="admin_overlayLong">
            Retrieving info...
        </h3>
    </div>
    <div id='admin_sidebar'>
        <div>
            <div>
                <div id='admin_competition_name'>
                    Loading...
                </div>
                <div id='admin_time'>
                    Loading...
                </div>
                <br>
                <br>
                <div class="sidebardivider"></div>
                <button class="sidebarbutton" onclick="adminControlPanel();">
                    Control Panel
                </button>
                <button class="sidebarbutton" onclick="adminEditComp();">
                    Edit Competition
                </button>
                <button class="sidebarbutton" onclick="adminLevels();">
                    Levels
                </button>
                <button class="sidebarbutton" onclick="adminGroups();">
                    Groups
                </button>
                <button class="sidebarbutton" onclick="adminProblems();">
                    Problems
                </button>
                <button class="sidebarbutton" onclick="adminCompetitors();">
                    Competitors
                </button>
                <button class="sidebarbutton" onclick="adminSubmissions();">
                    Submissions
                </button>
                <button class="sidebarbutton" onclick="adminScoreboard();">
                    Scoreboard
                </button>
                <div class="sidebardivider"></div>
                <div class="sidebartextsmall">
                    <br>
                    MCSC 2018-2019
                </div>
            </div>
        </div>
    </div>

    <div id='admin_field'>
        <div id="admin_backlay">
            MCSC
        </div>
        <div id='admin_levels'>
            <div>
                Levels</div>
            <div id='admin_levels_list'>
                Loading...
            </div>
        </div>
        <div id='admin_groups'>
            <div>
                Groups
            </div>
            <div id='admin_groups_list'>
                Loading...
            </div>
        </div>
        <div id='admin_control_panel'>
            <div>
                Control Panel
            </div>
            <div id='admin_control_panel_data'>
                <span class='admin_control_panel_scoreboard_header'>
                    Current Situation
                </span>
                <br>
                <span id="adminCurrentSituation">
                    Loading...
                </span>
                <br>
                <span class='admin_control_panel_scoreboard_header'>
                    Competition Status (Changing here resets automatic)
                </span>
                <br>
                <button class="btn btn-primary" onclick="adminSetCompStatus(0);">
                    Before Competition
                </button>
                <button class="btn btn-primary" onclick="adminSetCompStatus(1);">
                    During Competition
                </button>
                <button class="btn btn-primary" onclick="adminSetCompStatus(2);">
                    After Competition
                </button>
                <br>
                <span class='admin_control_panel_scoreboard_header'>
                    Automatic Competition Status w/ Timer
                </span>
                <br>
                <span>
                    Starting time (minutes after clicking Start Auto):
                    <input
                        id="adminControlPanelStartingTimeDelay"
                        type="number"
                        value="5"
                    >
                    <br>
                    Duration (minutes after starting time):
                    <input
                        id="adminControlPanelDuration"
                        type="number"
                        value="30"
                    >
                    <br>
                </span>
                <br>
                <button class="btn btn-primary" onclick="adminSetAutomaticCompetitionStatus();">
                    Start Auto
                </button>
                <br>
                <span class="admin_control_panel_scoreboard_header">
                    Scoreboard Visibility
                </span>
                <br>
                <span>
                    Sets whether the scoreboard is visible (during competition). Default is yes.
                </span>
                <br>
                <button class="btn btn-primary" onclick="adminEnableScoreboard();">
                    Enable Scoreboard
                </button> 
                <button class="btn btn-primary" onclick="adminDisableScoreboard();">
                    Disable Scoreboard
                </button>
                <br>
            </div>
        </div>
        <div id='admin_problems'>
            <div>
                Problems
            </div>
            <button class="btn btn-primary" onclick="adminAddProblem();">
                Add Problem
            </button>
            <div id='admin_problems_list'>
                Loading...
            </div>
        </div>
        <div id='admin_problem_general'>
            <div>
                <div>
                    Problem
                </div>
                <input id="admin_edit_problemname" value="">
            </div>
            <div class='admin_problem_general_area'>
                <div>
                    Problem Description
                </div>
                <textarea rows=10 id='admin_problem_general_inner'>
                	Loading...
                </textarea>
                <div>
                    Images
                </div>
                <ul id="admin_problem_images">
                    <li id="adminAddImageFields">
                        <input id="newProblemImage" type="file">
                        <button class="btn btn-primary" onclick="adminAddImage();">
                            Add Image
                        </button>
                    </li>
                </ul>
                <div>
                    Grading Server Specifications
                </div>
                <ul class="submission_processing_server_settings_editor">
                    <li>
                        Runtime Limit (1-30 Seconds):
                        <input
                            id="admin_problem_general_runtime"
                            type="number"
                            min="1"
                            max="30"
                            value="1"
                        >
                    </li>
                    <li>
                        Memory Limit (50-400 Megabytes):
                        <input
                            id="admin_problem_general_memory"
                            type="number"
                            min="50"
                            max="400"
                            value="100"
                        >
                        <br>
                    </li>
                </ul>
                <div>
                    Level
                </div>
                <select id="admin_problem_level"></select>
                <div onclick="adminSaveQuestion()">
                    Save
                </div>
            </div>
        </div>
        <div id='admin_problem_cases'>
            <div>
                Cases
            </div>
            <div>
                <button class="btn btn-primary" onclick="adminAddCase();">
                    Add Case
                </button>
                <button class="btn btn-primary" onclick="adminRegradeProblemSubmissions();">
                    Regrade Submissions
                </button>
            </div>
            <div id='admin_problem_cases_list'>
                Loading...
            </div>
        </div>
        <div id='admin_case'>
            <div>
                Problem
            </div>
            <div id='admin_case_inner'>
                <div class="admin_case_inner_header">
                    Input:
                </div>
                <textarea rows=5 id="editInput" placeholder='Input...'></textarea>
                <br><br>
                <div class="admin_case_inner_header">Output:</div>
                <textarea rows=5 id="editOutput" placeholder='Expected output...'></textarea>
                <br><br>
                <div class="admin_case_inner_header">Value:</div>
                <input style='' type="number" id="editValue">
                <br><br>
                <div class="admin_case_return" onclick='adminSaveCase();'>
                    Save & Return to Problem
                </div>
            </div>
        </div>
        <div id='admin_competitors'>
            <div>
                Competitors
            </div>
            <div id='admin_competitors_list'>
                Loading...
            </div>
        </div>
        <div id='admin_competitor_info'>
            <div id="competitor_username">
                Loading...
            </div>
            <div class='admin_competitor_info_overview'>
                <div>
                    Overview
                </div>
                <div class='admin_competitor_info_overview_typical'>
                    <div>
                        Score:
                    </div>
                    <div id="competitors_score">Loading...</div>
                </div>
                <div class='admin_competitor_info_overview_typical'>
                    <div>
                        Number of Submissions:
                    </div>
                    <div id="competitors_totalsubs">Loading...</div>
                </div>
                <div class='admin_competitor_info_overview_detailed_stats'>
                    Detailed Stats
                </div>
                <div id="competitor_detailed_stats">
                    Loading...
                </div>
            </div>
        </div>
        <div id='admin_submissions'>
            <div>
                Submissions
            </div>
            <div id='admin_submissions_list'>
                Loading...
            </div>
        </div>
        <div id='admin_results'>
            <div>
                Scoreboard
            </div>
            <div id='admin_results_list'>
                Loading...
            </div>
        </div>
    </div>
    <div id='editCompPage'>
    </div>

    <div id='adminFieldSubShadow' onclick='adminReturnFromFieldSub();'>
        <div class="sidebarbutton">
            Close
        </div>
    </div>
    <div id='adminFieldSub'>
        <div>
            MCSC
        </div>
    </div>
</div>