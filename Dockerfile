FROM public.ecr.aws/lambda/python:3.8 as build
RUN yum install -y unzip && \
    curl -SL https://chromedriver.storage.googleapis.com/86.0.4240.22/chromedriver_linux64.zip > /tmp/chromedriver.zip && \
    curl -SL https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-57/stable-headless-chromium-amazonlinux-2.zip > /tmp/headless-chromium.zip && \
    unzip /tmp/chromedriver.zip -d /opt/ && \
    unzip /tmp/headless-chromium.zip -d /opt/

FROM public.ecr.aws/lambda/python:3.8

# driverのバイナリ等を /opt 配下にコピー(lambdaでの処理実行時に /tmp にコピーする)
COPY --from=build /opt/headless-chromium /opt/
COPY --from=build /opt/chromedriver /opt/

RUN yum install -y https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
RUN pip install selenium
RUN pip install requests

# lambda実行に必要なコード等
COPY app.py ./

# RUN python3.8 -m pip install --upgrade pip
# RUN pip install -r requirements.txt

# ENV DISPLAY=:0.0

CMD ["app.handler"]
