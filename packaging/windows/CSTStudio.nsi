Unicode True
Name "CST Studio"
OutFile "..\..\release\CST-Libraries-Windows-Setup.exe"
InstallDir "$LOCALAPPDATA\CST Studio"
RequestExecutionLevel user

Page directory
Page instfiles
UninstPage uninstConfirm
UninstPage instfiles

Section "CST Studio" SEC01
  SetOutPath "$INSTDIR"
  File /r "..\..\dist\CST Studio\*.*"
  CreateDirectory "$SMPROGRAMS\CST Studio"
  CreateShortCut "$SMPROGRAMS\CST Studio\CST Studio.lnk" "$INSTDIR\CST Studio.exe"
  CreateShortCut "$DESKTOP\CST Studio.lnk" "$INSTDIR\CST Studio.exe"
  WriteUninstaller "$INSTDIR\Uninstall.exe"
SectionEnd

Section "Uninstall"
  Delete "$DESKTOP\CST Studio.lnk"
  Delete "$SMPROGRAMS\CST Studio\CST Studio.lnk"
  RMDir "$SMPROGRAMS\CST Studio"
  RMDir /r "$INSTDIR"
SectionEnd
