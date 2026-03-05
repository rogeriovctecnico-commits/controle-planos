[Setup]
AppName=Controle de Planos Flask
AppVersion=1.0
DefaultDirName={pf}\ControlePlanosFlask
DefaultGroupName=Controle de Planos Flask
OutputDir=.
OutputBaseFilename=Instalador_ControlePlanosFlask
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\app.exe"; DestDir: "{app}"; Flags: ignoreversion

Source: "planos.db"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Controle de Planos Flask"; Filename: "{app}\app.exe"
Name: "{userdesktop}\Controle de Planos Flask"; Filename: "{app}\app.exe"

[Run]
Filename: "{app}\app.exe"; Description: "Iniciar sistema agora"; Flags: nowait postinstall skipifsilent
