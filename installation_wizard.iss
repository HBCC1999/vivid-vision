; VividVision.iss
; Inno Setup script for Vivid Vision installer

[Setup]
AppName=Vivid Vision
AppVersion=1.0
AppPublisher=Your Name
DefaultDirName={localappdata}\VividVision
DisableProgramGroupPage=yes
DisableDirPage=yes
DisableReadyPage=yes
OutputDir=dist_installer
OutputBaseFilename=VividVisionSetup
Compression=lzma2
SolidCompression=yes
PrivilegesRequired=lowest
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

; Bundle installer.exe into the setup, extracted to a temp folder at runtime.
; "dontcopy" means it goes to {tmp} and is NOT left behind in the install dir.
[Files]
Source: "dist\installer.exe"; DestDir: "{tmp}"; Flags: dontcopy

[Code]
var
  IntensityPage: TInputOptionWizardPage;

procedure InitializeWizard;
begin
  IntensityPage := CreateInputOptionPage(
    wpWelcome,
    'Notification Style',
    'Choose how eye-care reminders should appear',
    'Select an option, then click Next to continue.',
    True,   { Exclusive = radio-button style, only one choice }
    False   { ListBox = false, shows as radio buttons }
  );
  IntensityPage.Add('Silent (small toast notification)');
  IntensityPage.Add('Critical (fullscreen, must wait 20 seconds)');
  IntensityPage.SelectedValueIndex := 0;
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  Intensity: string;
  ResultCode: Integer;
  InstallerExePath: string;
begin
  if CurStep = ssPostInstall then
  begin
    if IntensityPage.SelectedValueIndex = 0 then
      Intensity := 'silent'
    else
      Intensity := 'critical';

    ExtractTemporaryFile('installer.exe');

    InstallerExePath := ExpandConstant('{tmp}\installer.exe');

    if not Exec(InstallerExePath,
         '--intensity ' + Intensity + ' --interval 1200',
         '', SW_HIDE, ewWaitUntilTerminated, ResultCode) then
    begin
      MsgBox('Failed to run installer: ' + SysErrorMessage(ResultCode), mbError, MB_OK);
    end
    else if ResultCode <> 0 then
    begin
      MsgBox('Installer exited with an error (code ' + IntToStr(ResultCode) + ').', mbError, MB_OK);
    end;
  end;
end;

[Run]
; Optional: nothing extra to launch after — installer.exe already did the work above.
; Left empty on purpose. Add a "Filename" line here only if you want to
; offer "Launch Vivid Vision now" as a checkbox on the finish page.
