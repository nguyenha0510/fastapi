# IMAGE: tip-ws-report

FROM python:3.7.6

ARG app_name=TI_Portal_API

ENV HTTP_PROXY=http://10.30.118.20:8080
ENV HTTPS_PROXY=http://10.30.118.20:8080
ENV TZ=Asia/Ho_Chi_Minh

RUN mkdir -p /opt/${app_name}

COPY ./requirements.txt     /opt/${app_name}

WORKDIR /opt/${app_name}

RUN pip install --no-cache-dir -r requirements.txt && \
ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ADD ./app   /opt/${app_name}/app
ADD ./config    /opt/${app_name}/config
ADD ./database  /opt/${app_name}/database
ADD ./file_store  /opt/${app_name}/file_store
ADD ./error_code    /opt/${app_name}/error_code
ADD ./helpers   /opt/${app_name}/helpers
ADD ./models    /opt/${app_name}/models
ADD ./config.yaml   /opt/${app_name}
ADD ./logging.conf  /opt/${app_name}
ADD ./run.sh    /opt/${app_name}
ADD ./requirements.txt    /opt/${app_name}
ADD ./test_requirements.txt    /opt/${app_name}
RUN mkdir -p /opt/${app_name}/data
RUN chmod +x run.sh


CMD ["./run.sh"]
