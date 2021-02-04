FROM python:3
EXPOSE 8000

RUN git clone https://github.com/corfa/homework_for_course.git
RUN pip install --no-cache-dir -r /homework_for_course/requirements.txt
