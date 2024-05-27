; Name of the installer
Outfile "TheBot_Installer.exe"

; Name of the installation directory
InstallDir $PROGRAMFILES\TheBot

; Request application privileges for Windows Vista and above
RequestExecutionLevel admin

; Page configuration
Page directory
Page instfiles
UninstPage uninstConfirm
UninstPage instfiles

; Define installation section
Section "Install"

    ; Set output path to the installation directory
    SetOutPath "$INSTDIR"
    
    ; Include the Python executable file
    File "C:\Users\neela\Desktop\Miscellaneous\VS CODE\Install\TheBot.exe"

    ; Execute Python script silently (no console window)
    ExecWait '"$INSTDIR\TheBot.exe"'

    ; Launch the Ollama setup file
    ExecWait 'C:\Users\neela\Desktop\Miscellaneous\VS CODE\Install\OllamaSetup.exe'

    ; Wait for Ollama installation to complete
    Sleep 5000 ; Wait for 5 seconds (adjust as needed)

    ; Run the command to pull phi3:mini
    nsExec::ExecToLog 'cmd /c "ollama pull phi3:mini"'

    ; Write the uninstaller
    WriteUninstaller "$INSTDIR\Uninstall.exe"

SectionEnd

; Define uninstallation section
Section "Uninstall"

    ; Remove files and directories
    Delete "$INSTDIR\TheBot.exe"
    ; Delete other files as needed
    ; Delete "$INSTDIR\ollama_setup.exe"
    Delete "$INSTDIR\Uninstall.exe"
    RMDir "$INSTDIR"
    
SectionEnd
