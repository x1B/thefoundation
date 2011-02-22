# include this in all tools that require a database connection
SETTINGS="${1}"
if [ -z "${USAGE}" ]; then
    USAGE="usage: ${0} SETTINGS" 
fi

if [ ! -f "${SETTINGS}.py" ]; then
   echo "[!] ${USAGE}"
   echo "    where SETTINGS is one of:"
   ls ./settings_*.py | sed s/\.py// | grep -v settings_base
   exit 1
fi
