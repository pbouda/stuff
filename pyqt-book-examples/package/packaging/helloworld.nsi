; Name des Installationspakets
Name "Hello World"

; Name der Ausgabedatei
OutFile "setup-helloworld.exe"

; Standard-Installationsverzeichnis
InstallDir $PROGRAMFILES\HelloWorld

; Registry-Key mit Verzeichnis
InstallDirRegKey HKLM "Software\PB_HelloWorld" "Install_Dir"

;--------------------------------

; Pages

Page components
Page directory
Page instfiles

UninstPage uninstConfirm
UninstPage instfiles

;--------------------------------

; Was installiert wird
Section "HelloWorld (required)"

  SectionIn RO
  
  SetOutPath $INSTDIR
  
  ; Alle Dateien des Pakets liegen hier
  File /r "dist_win\*"
  
  ; Installationspfad in die Registry schreiben
  WriteRegStr HKLM SOFTWARE\PB_HelloWorld "Install_Dir" "$INSTDIR"
  
  ; Keys für Uninstall
  WriteRegStr HKLM \
    "Software\Microsoft\Windows\CurrentVersion\Uninstall\HelloWorld" \
    "DisplayName" "HelloWorld"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\HelloWorld" "UninstallString" '"$INSTDIR\uninstall.exe"'
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\HelloWorld" "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\HelloWorld" "NoRepair" 1
  WriteUninstaller "uninstall.exe"
  
SectionEnd

; Optionale Installationskomponenten
Section "Start Menu Shortcuts"

  CreateDirectory "$SMPROGRAMS\HelloWorld"
  CreateShortCut "$SMPROGRAMS\HelloWorld\Uninstall.lnk" "$INSTDIR\uninstall.exe" "" "$INSTDIR\uninstall.exe" 0
  CreateShortCut "$SMPROGRAMS\HelloWorld\HelloWorld.lnk" "$INSTDIR\bin\helloworld.exe" "" "$INSTDIR\bin\helloworld.exe" 0
  
SectionEnd

;--------------------------------

; Uninstaller

Section "Uninstall"
  
  ; Registry-Keys löschen
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\HelloWorld"
  DeleteRegKey HKLM SOFTWARE\PB_HelloWorld

  ; Dateien löschen
  Delete $INSTDIR\bin\*.*
  Delete $INSTDIR\*

  ; Shortcuts löschen
  Delete "$SMPROGRAMS\HelloWorld\*.*"

  ; Verzeichnisse löschen
  RMDir "$SMPROGRAMS\HelloWorld"
  RMDir "$INSTDIR\bin"
  RMDir "$INSTDIR"

SectionEnd
