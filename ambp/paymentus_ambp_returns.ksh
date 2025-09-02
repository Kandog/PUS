#!/usr/bin/ksh
####################################################################
# Name:         paymentus_ambp_returns.ksh
# Purpose:      Processing RETURNS of Building Permits payments
# Created by    M.Stojanovic at 28 Nov 2022
# Notes:
# Modification:
#
####################################################################
#setup environment
#. /home/oracle/scripts/CRON_UTIL.sh
. /home/oracle/scripts/LIBRARY/CRON_UTIL.sh
DAY=`date '+%a'`
EXECUTE_DIR=/home/oracle/scripts/Interface/Paymentus/AMBP/script
LOG_DIR=/home/oracle/scripts/Interface/Paymentus/AMBP/log
IN_DIR=/home/oracle/scripts/Interface/Paymentus/AMBP/in
ARCHIVE_DIR=/home/oracle/scripts/Interface/Paymentus/AMBP/archive
RECEIVED_DIR=/home/oracle/scripts/Interface/Paymentus/AMBP/received
RETURN_LOG=${LOG_DIR}/return.log
RETURNS_IN=/opt/fx/PAYMENTUS/INBOUND/RAW/AMBP/RETURNS
RETURNS_OUT=/opt/fx/PAYMENTUS/INBOUND/PROCESSED/AMBP/RETURNS
FROM_ADDR=DoNotReply@kitchener.ca
TO_ADDR="building@kitchener.ca"
TO_ADDR1="Scott.Xu@kitchener.ca"
TO_ADDR2="Tatiana.Makarova@kitchener.ca"


if [ $(ls -A ${RETURNS_IN}|wc -l) -eq 0 ]; then
    echo "no return file"
    exit 0
fi

# through all files
for FileName in ${RETURNS_IN}/*;do
# if file is large then certain size email it to specified address
        FSize=350
        if [ $(wc -c "$FileName" | awk '{print $1}') -gt $FSize ]; then
 #              printf "File %s is larger than %d bytes.\n" "$FileName" $FSize
               echo "Building Permit Return is attached." | mailx -a $FileName -s "Paymentus (AMMP) - Return" -r ${FROM_ADDR} ${TO_ADDR}
                echo "Building Permit Return is attached." | mailx -a $FileName -s "Paymentus (AMBP) - Return" -r ${FROM_ADDR} ${TO_ADDR1}
#               echo "Building Permit Return is attached." | mailx -a $FileName -s "Paymentus (AMBP) - Return" -r ${FROM_ADDR} ${TO_ADDR2}

                # copy file to processed files location for RETURNS
                cp $FileName ${RETURNS_OUT}

                # archive file
                mv $FileName ${ARCHIVE_DIR}
        else
#               printf "File $FileName is smaller than $FSize bytes.\n"

                # archive file
                mv $FileName ${ARCHIVE_DIR}
        fi

           # Audit file
           echo "$(date) - $FileName processed." >>${RETURN_LOG}
done
