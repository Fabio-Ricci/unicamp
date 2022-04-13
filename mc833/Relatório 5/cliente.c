// Fábio Camargo Ricci - 170781

#include <sys/socket.h>
#include <sys/types.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <stdio.h>
#include <netdb.h>
#include <string.h>
#include <errno.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

#define BUFFER_SIZE 4096
#define INPUT_SIZE 10 * BUFFER_SIZE

int Socket(int family, int type, int flags)
{
   int sockfd;
   if ((sockfd = socket(family, type, flags)) < 0) // cria socket
   {
      perror("socket");
      exit(1);
   }
   return sockfd;
}

void Connect(int sockfd, const char *host, struct sockaddr_in *addr)
{
   if (inet_pton(AF_INET, host, &addr->sin_addr) <= 0) // converte o endereço IP do servidor em representação binária
   {
      perror("inet_pton error");
      exit(1);
   }

   if (connect(sockfd, (struct sockaddr *)addr, sizeof(*addr)) < 0)
   {
      perror("connect error");
      exit(1);
   }
}

int Read(int sockfd, char *buf, size_t size)
{
   int n = read(sockfd, buf, size);
   if (n < 0)
   {
      perror("read error");
      exit(1);
   }

   buf[n] = 0;

   return n;
}

void Write(int sockfd, char *buf)
{
   if (write(sockfd, buf, strlen(buf)) < 0) // escreve o conteúdo do buffer no socket de conexão
   {
      perror("write error");
      exit(1);
   }
}

void Getsockname(int sockfd, struct sockaddr_in *addr)
{
   socklen_t len = sizeof(*addr);

   // informação do socket local
   if (getsockname(sockfd, (struct sockaddr *)addr, &len) < 0) // recupera informação do endereço do socket
   {
      perror("getsockname");
      exit(1);
   }
}

int Fork()
{
   pid_t child_pid = fork();
   if (child_pid < 0)
   {
      perror("Fork error");
      exit(1);
   }

   return child_pid;
}

void show_info_received(struct sockaddr_in server_addr, char *content)
{
   char name[128];

   if (inet_ntop(AF_INET, &(server_addr.sin_addr), name, sizeof(name)) < 0) // recupera string IPv4 do endereço
   {
      perror("inet_ntop error");
      exit(1);
   }

   printf("Received: '%s' from server on IP: %s Port: %d\n", content, name, ntohs(server_addr.sin_port));
   fflush(stdout);
}

int main(int argc, char **argv)
{
   int sockfd;
   struct sockaddr_in server_addr;
   char buffer[BUFFER_SIZE + 1] = "";
   char sentStr[INPUT_SIZE + 1] = "", recvStr[INPUT_SIZE + 1] = "";
   fd_set rset;

   if (argc != 3)
   {
      strcpy(buffer, "uso: ");
      strcat(buffer, argv[0]);
      strcat(buffer, " <IPaddress> <Port>");
      perror(buffer);
      exit(1);
   }

   char *host = argv[1];                  // server host
   in_port_t port = htons(atoi(argv[2])); // server port

   sockfd = Socket(AF_INET, SOCK_STREAM, 0); // socket() wrapper

   bzero(&server_addr, sizeof(server_addr));
   server_addr.sin_family = AF_INET; // familia de protocolos
   server_addr.sin_port = port;      // porta servidor

   Connect(sockfd, host, &server_addr); // connect() wrapper

   FD_ZERO(&rset);

   for (;;)
   {
      FD_SET(fileno(stdin), &rset); // watch stdin
      FD_SET(sockfd, &rset);        // watch socket

      int max_sd = (fileno(stdin) > sockfd) ? fileno(stdin) : sockfd;

      select(max_sd + 1, &rset, NULL, NULL, NULL);

      if (FD_ISSET(sockfd, &rset)) // atividade no socket
      {
         // le retorno do servidor
         if (Read(sockfd, buffer, BUFFER_SIZE) == 0) // 0 significa desconexão com sucesso
         {
            break;
         }
         strcat(recvStr, buffer); // append received

         show_info_received(server_addr, buffer); // save server info received on file

         if (strcmp(sentStr, recvStr) == 0) // if sent and received are equal, stop client
         {
            break;
         }
      }

      if (FD_ISSET(fileno(stdin), &rset)) // atividade na entrada padrão
      {
         // le da entrada padrão
         if (fgets(buffer, BUFFER_SIZE, stdin) != NULL)
         {
            Write(sockfd, buffer);   // write to server
            strcat(sentStr, buffer); // append sent
         }
      }
   }

   fclose(stdout);

   shutdown(sockfd, SHUT_RDWR);
   close(sockfd);

   return 0;
}
