<div id="resetpasswordpage">
	<center>
		<h2 id="resetPageInstructions" style='color:white;'>Reset Password</h2>
	</center>
	<br><br>
	<form method="POST" onsubmit="return false;">
		<center>
			<span style='display:block;'>
				<input class='form-control' style='width:400px;padding:10px;height:auto;margin:5px;' type='text'
					name='mcst_username' id='mcst_username' placeholder='Username'>
				<input class='form-control' style='width:400px;padding:10px;height:auto;margin:5px;'
					type='password' name='mcst_newPassword1' id='mcst_newPassword1' placeholder='Enter New Password'>
				<input class='form-control' style='width:400px;padding:10px;height:auto;margin:5px;'
					type='password' name='mcst_newPassword2' id='mcst_newPassword2' placeholder='Re-enter New Password'>
				<input class='btn btn-primary' style='width:400px;padding:10px;margin:5px;'
					onclick="resetPassword();return false;" type='submit' id='mcst_resetPassword'
					value='Reset Password'> 
				<br>
				<div class="alert alert-danger" id='mcst_reset_notif_1'
					style='display:none;width:400px;padding:10px;height:auto;margin:5px;'>Incorrect Username, or your token expired.</div>
				<div class="alert alert-danger" id='mcst_reset_notif_2'
					style='display:none;width:400px;padding:10px;height:auto;margin:5px;'>Client lost
					connection.</div>
				<div class="alert alert-danger" id='mcst_reset_notif_3'
					style='display:none;width:400px;padding:10px;height:auto;margin:5px;'> Passwords don't match.</div>
				<div class="alert alert-danger" id='mcst_reset_notif_4'
					style='display:none;width:400px;padding:10px;height:auto;margin:5px;'> Please fill out all 
					the fields with valid entries.</div>
                    <div class="alert alert-danger" id='mcst_reset_notif_5'
					style='display:none;width:400px;padding:10px;height:auto;margin:5px;'> Reset Password link timed out.
                    Go through the forgot password process again.</div>
				<br>
				<br>
			</span>
		</center>
	</form>
		<div style='position:fixed;z-index:36236;left:0px;bottom:0px;' id='connstatus'>
			<span style='color:red'>Server Connection: No Connection</span>
		</div>
		<img style="position:fixed;bottom:0px;left:0px;width:100%;z-index:-1;" src="images/trianglebase.png">
</div>