#!/bin/bash
chmod +x gerar_atalho.sh
chmod +x FeiTV
dir=$(dirname $(realpath "$0"))
file="FeiTV"
icon="icon.png"
TARGET_EXEC="${dir}/${file}"
TARGET_ICON="${dir}/${icon}"

cat << EOF > FeiTV.desktop
[Desktop Entry]
Type=Application
Exec="${TARGET_EXEC}"
Icon=${TARGET_ICON}
Terminal=true
EOF

chmod +x FeiTV.desktop
