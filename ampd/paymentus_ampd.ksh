#!/usr/bin/ksh
###############################################################################
# Name:         paymentus_ambp.ksh_
# Purpose:      get data from Paymentus for Amanda Building Permits
#               and upload to interface_paymentus.pus_ambp table
#               and otify user
# Created by    Scott Xu at Mar 04,2016
# Notes:        One Oracle Directories
#               EXT_TABLE
#               should be setup first
# Modification: M.Stojanovic 28-Nov-22 addapted code to process delivered file
#                                      for processing in the AMAP1 database
#
###############################################################################
#setup environment
#. /home/oracle/scripts/CRON_UTIL.sh
. /home/oracle/scripts/LIBRARY/CRON_UTIL.sh
DAY=`date '+%a'`
EXECUTE_DIR=/home/oracle/scripts/Interface/Paymentus/AMPD/script
LOG_DIR=/home/oracle/scripts/Interface/Paymentus/AMPD/log
IN_DIR=/home/oracle/scripts/Interface/Paymentus/AMPD/in
ARCHIVE_DIR=/home/oracle/scripts/Interface/Paymentus/AMPD/archive
RECEIVED_DIR=/home/oracle/scripts/Interface/Paymentus/AMPD/received
AUDIT_LOG=${LOG_DIR}/audit.log
EXT_DIR=/home/oracle/scripts/Interface/Paymentus/AMPD/exttable
EXT_FILE=${EXT_DIR}/paymentus_ampd_file
DEPOSIT_IN=/opt/fx/PAYMENTUS/INBOUND/RAW/AMPD/DEPOSIT/
DEPOSIT_OUT=/opt/fx/PAYMENTUS/INBOUND/PROCESSED/AMPD/DEPOSIT/
POSTING_IN=/opt/fx/PAYMENTUS/INBOUND/RAW/AMPD/POSTING/
POSTING_OUT=/opt/fx/PAYMENTUS/INBOUND/PROCESSED/AMPD/POSTING/
FROM_ADDR=DoNotReply@kitchener.ca
TO_ADDR="Scott.Xu@kitchener.ca"

# Process DEPOSITS if exists
if ls ${DEPOSIT_IN}*.csv 1> /dev/null 2>&1; then
  mv  ${DEPOSIT_IN}*.csv ${DEPOSIT_OUT}
fi

# Process RETURNS if exists
${EXECUTE_DIR}/paymentus_ampd_returns.ksh


# Remove old log file
if [ -f ${LOG_DIR}/paymentus_ampd.log ]; then
  rm ${LOG_DIR}/paymentus_ampd.log
fi
exec >>${LOG_DIR}/paymentus_ampd.log
exec 2>&1

# Download file(s)
for file in $(ls ${POSTING_IN} |awk '{print $1}'); do
# check if file exists in Archive or not
  # if not, then get it
  #echo $file
  if [ ! -f ${POSTING_OUT}/${file} ]; then
      mv ${POSTING_IN}$file ${IN_DIR}/
      echo "get file $file"
      cp  ${IN_DIR}/$file ${RECEIVED_DIR}/$file
      #echo "move file $file"
      #mv  ${POSTING_IN}$file ${POSTING_OUT}
  else
      echo "file $file already exists."
      rm ${POSTING_OUT}/${file}
  fi
done

if [ -z "$(ls -A ${IN_DIR}|head -n 5)" ];then
  echo "$(date) - No Planning Permit file get from Paymentus." <${LOG_DIR}/Error.log
#  mailx -s "No Planning Permit file get from Paymentus" -r ${FROM_ADDR} ${TO_ADDR} <${LOG_DIR}/Error.log
  # Audit
  echo "$(date) - No any Planning Permit file get from Paymentus.">>${AUDIT_LOG}
  exit
fi

# Go through all files
for f in ${IN_DIR}/*;do
  if [ -f "$f" ];then
    echo "$f"
    # copy file to oracle external table location
    cp $f ${EXT_FILE}
    if [ $? != 0 ];then
        echo "Copy file $f to oracle external table location failed"
        # Audit
        echo "$(date) - Copy file $f to oracle external table location failed">>${AUDIT_LOG}
    else
        # process data
        sqlplus /@AMAT1 @${EXECUTE_DIR}/paymentus_ampd.sql >  ${LOG_DIR}/sql.log
        if [ $(/usr/bin/grep -E 'PLS-|ORA-' ${LOG_DIR}/sql.log|wc -l) -ne 0 ]; then
           echo "Process $f data failed."
           # Audit
           echo "$(date) - Process $f data failed.">>${AUDIT_LOG}
           mailx -s "ERROR(AMAT1) - Process scripts/Interface/Interface/Paymentus file" ${RECEPIENT}  <${LOG_DIR}/paymentus_ambp.log
        else
           echo "Process $f data Succeed."

           # Archive file
           #mv $f ${ARCHIVE_DIR}
           mv  $f ${POSTING_OUT}

           # clean up
           rm ${EXT_DIR}/PUS_AMPD_EXT*.log

           # Audit file
           echo "$(date) - $f processed." >>${AUDIT_LOG}

        fi
    fi
  fi
done
