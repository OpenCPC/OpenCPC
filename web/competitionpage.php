<div id="competition_page">
    <div id='competition_overlay'>
        <h1 id='competition_overlayTitle'>Loading...</h1>
        <h3 id='competition_overlayLong'>Retrieving info...</h3>
        <div id='competition_overlay_last_30_swipe'>
            <div>
                <div class="col30_title">
                    COMPETITION BEGINS IN
                </div>
                <div class="col30_between">
                    <div></div>
                    <div>
                        <div id='competition_overlay_last_30_countdown'></div>
                    </div>
                </div>
                <div class="col30_title_s">
                    SECONDS
                </div>
            </div>
        </div>
        <div id='competition_overlay_last_30'>
        </div>

    </div>

    <!-- loading circle -->
    <div id='loading' style=''>
        <div class='loadingSpinnerContainer' style="width:100px;display:inline-block;height:100px;">
            <?php
	for ($i = 0;$i<16;$i++) {
	echo "<div class=\" rect".$i."\"></div>";
	}
	?>
        </div>
    </div>

    <!-- Kill scrollbars by pushing them to the right  -->
    <div id='sidebar'>
        <div>
            <div>
                <div class='competition_title_area'>
                    <span id='competition_name'>
                        Loading...
                    </span><br>
                    <span id='competition_time'>
                        Loading...
                    </span><br>
                </div>
                <div class="sidebartextsmall siderbar_title_group">
                    <br>
                    Group:
                    <span id='sidebar_group'></span>
                </div>
                <div class="sidebartextsmall sidebar_title_division">
                    <br>
                    Division:
                    <span id='sidebar_division'></span>
                </div>
                <div class="sidebardivider"></div>
                <button class="sidebarbutton" onclick="sbScoreboard();">
                    Scoreboard
                </button>
                <button class="sidebarbutton" onclick="sbProblemList();">
                    Problem List
                </button>
                <button class="sidebarbutton" onclick="sbAllSubmissions();">
                    All Submissions
                </button>
                <div class="sidebardivider"></div>
                <div class="sidebartextsmall"><br>MCSC 2018-2019</div>
            </div>
            <div class="sidebardivider"></div>
        </div>
    </div>

    <!-- field is the rest of the screen, shows actual content -->
    <div id='field'>
        <div id="allSubmissions">
            <div>
                <div class="all_submissions_header_title">
                    All Submissions
                </div>
                <div id='allProblemSubmissions'>
                    Loading...
                </div>
            </div>
            <br><br><br>
        </div>
        <div id="scoreboard">
            <div>
                <div class='scoreboard_header_title'>
                    Scoreboard
                </div>
                <div id='scoreboardInner'>
                    Loading...
                </div>
            </div>
            <br><br><br>
        </div>

        <div id="problemlist">
            <div>
                <div class='problemlist_title'>
                    Problem List
                </div>
                <div class='problemlist_key_container'>
                    Key:
                    <div>
                        <div class='problemlist_unattempted'></div>
                        Unattempted
                    </div>

                    <div>
                        <div class='problemlist_0p'></div>
                        0%
                    </div>
                    <div>
                        <div class='problemlist_50p'></div>
                        &lt;50%
                    </div>
                    <div>
                        <div class='problemlist_ge50p'></div>
                        &gt;=50%
                    </div>
                    <div>
                        <div class='problemlist_100p'></div>
                        100%
                    </div>
                    <br><br>
                    Format: <i>Problem number</i>. <i>Problem name</i> (<i>Problem max score</i>)
                </div>
                <div id='problemListInner'>
                    <table>
                        <tr>
                            <td>
                                Easy
                            </td>
                            <td>
                                <div></div>
                            </td>
                        </tr>
                    </table>
                    <div id='pleasy'> </div>
                    <table>
                        <tr>
                            <td>
                                Medium
                            </td>
                            <td>
                                <div></div>
                            </td>
                        </tr>
                    </table>
                    <div id='plmedium'> </div>
                    <table>
                        <tr>
                            <td>
                                Hard
                            </td>
                            <td>
                                <div></div>
                            </td>
                        </tr>
                    </table>
                    <div id='plhard'> </div>
                </div>
            </div>
            <br><br><br>
        </div>
        <div id="backlay">
            MCSC
        </div>
    </div>

    <div id='fieldSubShadow' onclick='returnFromFieldSub();'>
        <div class="sidebarbutton">
            Close
        </div>
    </div>
    <div id='fieldSub'>
        <div>
            MCSC
        </div>
    </div>
</div>