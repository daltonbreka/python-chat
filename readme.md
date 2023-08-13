********** MY REQUIREMENT ******************************
please create new gmail for my effort of this project.

********** ENVIRONMENT *********************************
- python installation
- pip module - PyQt5

********* START APP ************************************
1) Start Server
    COMMAND: python server.py
2) Start Client
    COMMAND: python ui-client.py

*********** RESULT  *************************************
- server will be running on 5000 port
- client will be running on 5002 port

*********** CLIENT WINDOW *******************************
1) Input server IP address.
 - x.x.x.x(0<=x<=255)
2) Input message.
 - message is not supposed to be empty.

*********** Lamport timestamps **************************
- In pseudocode, the algorithm for sending is:
    # event is known
    time = time + 1;
    # event happens
    send(message, time);

- The algorithm for receiving a message is:
    (message, time_stamp) = receive();
    time = max(time_stamp, time) + 1;