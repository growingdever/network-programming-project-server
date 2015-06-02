#include "client_worker.h"
#include "constants.h"
#include "data_structure.h"
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>


int client_worker_main_loop(pid_t pid, int sock) {
	key_t msg_queue_key_id = msgget((key_t)MQ_KEY, IPC_CREAT | 0666);
	if( msg_queue_key_id == -1 ) {
		// error!
		return 1;
	}
	printf("(client_worker) msg_queue_key_id : %d\n", msg_queue_key_id);

	char buffer[MAX_LENGTH];
	while(1) {
		memset(buffer, 0, sizeof(buffer));
		ssize_t length = read_line(sock, buffer, MAX_LENGTH);
		if( length > 0 ) {
			// send message that is received from client to main server
			send_message_to_main_server(msg_queue_key_id, sock, buffer);
		}

		// check message queue
		int msg_exist = check_message_queue(sock);

		// if exist message to send, write message to client
		if( msg_exist ) {
			if( ! send_message_to_client(sock, "") ) {

			} else {
				// error
			}
		}
	}

	return 0;
}

int send_message_to_main_server(key_t mq_key, int sock, char message[MAX_LENGTH]) {
	struct message_buffer msg;
	msg.type = MQ_ID_MAIN_SERVER;
	msg.sock = sock;
	strcpy(msg.buffer, message);
	if( msgsnd(mq_key, (void *)&msg, sizeof(struct message_buffer), 0) == -1 ) {
		// error!
	}

	return 0;
}

int check_message_queue(int sock) {
	return 0;
}

int send_message_to_client(int sock, char message[MAX_LENGTH]) {
	write(sock, message, strlen(message));
	return 0;
}