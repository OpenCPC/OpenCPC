<div id="loginpage">
    <div id='loginpage_overlay'>
        <h1 id='loginpage_overlayTitle'>
            Under Maintenance
        </h1>
        <h3 id='loginpage_overlayLong'>
            Sorry, but this site is down for maintenance for the time being.
            Thank you for your patience.
        </h3>
    </div>

    <div>
        <h1 class='large_login_page_name'>
            MCSC
        </h1>
        <h2 id="loginPageInstructions">
            Log In
        </h2>
    </div>
    <br><br>
    <form method="POST" onsubmit="return false;">
        <div class="alert alert-danger red_box">
            <b>Warning:</b>
            Hacking is not part of the competition.
            Hacking or exploitation of the scoring system will
            result in school-wide disqualification.
        </div>
        <br>
        <div class="alert alert-danger red_box">
            We are currently in maintenance mode while we prepare to become
            open source. Expect downtime and errors.
        </div>
        <br>
        <div 
            class="alert alert-warning red_box login_page_input_display_none"
            id="mcst_tmpforgotpassword"    
        >
            For the time being, the reset password functionality isn't working. 
            Please email contact@mcsc.enrog.com if you need your password changed.
            You must include your username in that email.
        </div>
        <input
            class='form-control loginpage login_page_input_1'
            type='text'
            name='mcst_username'
            id='mcst_username'
            placeholder='Username'
        >
        <input
            class='form-control loginpage login_page_input_1'
            type='password'
            name='mcst_password'
            id='mcst_password'
            placeholder='Password'
        >
        <input
            class='form-control loginpage login_page_input_1 login_page_input_display_none'
            type='text'
            name='mcst_name'
            id='mcst_name'
            placeholder='Name'
        >
        <input
            class='form-control loginpage login_page_input_1 login_page_input_display_none'
            type='text'
            name='mcst_school'
            id='mcst_school'
            placeholder='School'
        >
        <input
            class='form-control loginpage login_page_input_1 login_page_input_display_none'
            type='email'
            name='mcst_email'
            id='mcst_email'
            placeholder='Email'
        >
        <input
            class='btn btn-primary login_page_input_button'
            onclick="tryLoginAction();return false;"
            type='submit'
            id='mcst_login'
            value='Sign in to the dashboard'
        >
        <input
            class='btn btn-primary login_page_input_display_none login_page_input_button'
            onclick="tryLoginAction();return false;"
            type='submit'
            id='mcst_signup'
            value='Sign Up'
        >
        <input
            class='btn btn-primary login_page_input_display_none login_page_input_button'
            onclick="tryLoginAction();return false;"
            type='submit'
            id='mcst_forgotPassword'
            value='Send Email'
        >
        <br>
        <input
            class='btn btn-link login_page_input_button_2'
            onclick="gotoSignup();return false;"
            type='button'
            id='mcst_gotoSignup'
            value="Don't have an account? Sign up!"
        >
        <input
            class='btn btn-link login_page_input_button_2'
            onclick="gotoLogin();return false;"
            type='button'
            id='mcst_gotoLogin'
            value="Already have an account? Log In!"
        >
        <input
            class='btn btn-link login_page_input_button_2'
            onclick="gotoForgotPassword();return false;"
            type='button'
            id='mcst_gotoForgotPassword'
            value="Forgot Password?"
        >
        <br>
        <div class="alert alert-danger mcst_login_notif" id='mcst_login_notif_1'>
            Incorrect username/ competition id/ password.
        </div>
        <div class="alert alert-danger mcst_login_notif" id='mcst_login_notif_2'>
            Client lost connection.
        </div>
        <div class="alert alert-danger mcst_login_notif" id='mcst_login_notif_3'>
            Username already taken.
        </div>
        <div class="alert alert-danger mcst_login_notif" id='mcst_login_notif_4'>
            Please fill out all the fields with valid entries.
        </div>
        <div class="alert alert-danger mcst_login_notif" id='mcst_login_notif_5'>
            User not found.
        </div>
        <div class="alert alert-success mcst_login_notif" id='mcst_login_notif_6'>
            Email Sent. Check your inbox and spam.
        </div>
        <br>
        <br>
    </form>
    <div id='connstatus'>
        <span class='connstatus_bad'>
            Server Connection: No Connection
        </span>
    </div>
    <img class="background_image" src="images/trianglebase.png">
</div>