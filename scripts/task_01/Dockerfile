FROM alpine:latest

RUN apk update && apk add openssh

RUN adduser -D ansible
RUN echo "ansible:ansible" | chpasswd

RUN mkdir /home/ansible/.ssh

COPY authorized_keys /home/ansible/.ssh/authorized_keys

RUN chown -R ansible:ansible /home/ansible/.ssh
RUN chmod 700 /home/ansible/.ssh
RUN chmod 600 /home/ansible/.ssh/authorized_keys

CMD ["/usr/sbin/sshd", "-D"]
