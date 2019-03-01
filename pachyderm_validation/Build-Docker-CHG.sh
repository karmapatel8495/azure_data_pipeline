docker build --no-cache -t chg_validate_image:v$1 .
docker tag chg_validate_image:v$1 rajatmittal18/chg_validate_image:v$1
docker push rajatmittal18/chg_validate_image:v$1
