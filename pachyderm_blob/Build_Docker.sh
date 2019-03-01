docker build --no-cache -t crowe_cron:v$1 .
docker tag crowe_cron:v$1 rajatmittal18/crowe_cron:v$1
docker push rajatmittal18/crowe_cron:v$1
