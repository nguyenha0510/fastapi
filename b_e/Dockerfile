# IMAGE: tip-ws-report
FROM python:3.7.6

ARG app_name=TI_Portal_API

ENV http_proxy=http://10.255.249.100:3128
ENV httpS_proxy=http://10.255.249.100:3128
ENV TZ=Asia/Ho_Chi_Minh

RUN mkdir -p /opt/${app_name}

COPY ./requirements.txt     /opt/${app_name}
COPY ./test_requirements.txt     /opt/${app_name}
COPY ./wkhtmltox_0.12.6-1.buster_amd64.deb     /opt/${app_name}

WORKDIR /opt/${app_name}

RUN apt-get update
RUN apt-get upgrade -y

# Download and install wkhtmltopdf
RUN apt-get update \
    && apt-get -y install \
    apt-utils libfontenc1 xfonts-75dpi xfonts-base xfonts-encodings xfonts-utils openssl build-essential \
    libssl-dev libxrender-dev git-core libx11-dev libxext-dev libfontconfig1-dev libfreetype6-dev fontconfig \
    && chmod +x ./wkhtmltox_0.12.6-1.buster_amd64.deb \
    && apt-get -y install ./wkhtmltox_0.12.6-1.buster_amd64.deb \
    && apt-get -y clean \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir --upgrade pip -r requirements.txt -r test_requirements.txt && \
ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ADD ./app   /opt/${app_name}/app
ADD ./config    /opt/${app_name}/config
ADD ./database  /opt/${app_name}/database
ADD ./file_store  /opt/${app_name}/file_store
ADD ./header_footer_html  /opt/${app_name}/header_footer_html
ADD ./error_code    /opt/${app_name}/error_code
ADD ./helpers   /opt/${app_name}/helpers
ADD ./schemas   /opt/${app_name}/schemas
ADD ./tests    /opt/${app_name}/tests
ADD ./logs    /opt/${app_name}/logs
ADD ./coveragerc   /opt/${app_name}
ADD ./config.yaml   /opt/${app_name}
ADD ./logging.conf  /opt/${app_name}
ADD ./tox.ini   /opt/${app_name}
ADD ./run.sh    /opt/${app_name}
ADD ./requirements.txt    /opt/${app_name}
ADD ./test_requirements.txt    /opt/${app_name}
#ADD ./plugins    /opt/${app_name}/plugins


RUN mkdir -p /opt/${app_name}/data
RUN chmod +x run.sh

CMD ["./run.sh"]
