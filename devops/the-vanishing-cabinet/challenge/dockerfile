FROM alpine:latest
RUN mkdir /chamber_of_secrets /room_of_requirement /restricted_section /hogwarts /forbidden_forest
RUN echo "Not even Alohomora will help you here!" > /chamber_of_secrets/flag.txt
RUN echo "" > /chamber_of_secrets/flag.txt
COPY flag1.txt /chamber_of_secrets/flag1.txt
RUN base64 /chamber_of_secrets/flag1.txt > /room_of_requirement/vanishing_cabinet.txt
RUN base64 /room_of_requirement/vanishing_cabinet.txt > /room_of_requirement/marauders_map.txt
RUN rm -rf /chamber_of_secrets/* /room_of_requirement/*
RUN echo "Mischief managed! Look elsewhere." > /restricted_section/remembrall.txt
RUN rm -rf /restricted_section/remembrall.txt
RUN echo "Even Professor Snape couldn't find this secret!" > /flag.txt
COPY flag2.txt /forbidden_forest/flag2.txt
RUN rm -rf /flag.txt /chamber_of_secrets /room_of_requirement /restricted_section /hogwarts /forbidden_forest
ENTRYPOINT [ "/bin/sh" ]