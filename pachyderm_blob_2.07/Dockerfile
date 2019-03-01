FROM python:3
COPY crowe_input.py /
COPY requirements.txt /
RUN pip install -r requirements.txt
RUN cat /etc/os-release

#RUN curl -o /tmp/pachctl.deb -L https://github.com/pachyderm/pachyderm/releases/download/v1.8.2/pachctl_1.8.2_amd64.deb
#RUN dpkg -i /tmp/pachctl.deb
#COPY config.json /root/.pachyderm/config.json

#RUN pachctl port-forward &
