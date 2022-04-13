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
#include <unistd.h>

#define BUFFER_SIZE 4096

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

void Read(int sockfd, char *buf, size_t size)
{
   int n = read(sockfd, buf, size);
   if (n < 0)
   {
      perror("read error");
      exit(1);
   }

   buf[n] = 0;
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

void show_server_info(int sockfd, struct sockaddr_in addr)
{
   char name[128];

   if (inet_ntop(AF_INET, &(addr.sin_addr), name, sizeof(name)) < 0) // recupera string IPv4 do endereço
   {
      perror("inet_ntop");
      exit(1);
   }

   printf("Connected on server IP: %s Port: %d\n", name, ntohs(addr.sin_port));
}

void show_local_info(int sockfd)
{
   struct sockaddr_in addr;
   char name[128];

   Getsockname(sockfd, &addr); // getsockname() wrapper

   if (inet_ntop(AF_INET, &(addr.sin_addr), name, sizeof(name)) < 0) // recupera string IPv4 do endereço
   {
      perror("inet_ntop");
      exit(1);
   }

   printf("Connected on local IP: %s Port %d\n", name, ntohs(addr.sin_port));
}

void execute(char *cmd, char *res)
{
   FILE *fp;

   fp = popen(cmd, "r");
   if (fp == NULL)
   {
      perror("popen");
      exit(1);
   }

   fgets(res, BUFFER_SIZE, fp);

   if (pclose(fp) < 0)
   {
      perror("pclose");
      exit(1);
   }
}

int main(int argc, char **argv)
{
   int sockfd;
   struct sockaddr_in server_addr;
   char buffer[BUFFER_SIZE + 1];
   char error[BUFFER_SIZE + 1];

   if (argc != 3)
   {
      strcpy(error, "uso: ");
      strcat(error, argv[0]);
      strcat(error, " <IPaddress> <Port>");
      perror(error);
      exit(1);
   }

   char *host = argv[1];                  // server host
   in_port_t port = htons(atoi(argv[2])); // server port

   sockfd = Socket(AF_INET, SOCK_STREAM, 0); // socket() wrapper

   bzero(&server_addr, sizeof(server_addr));
   server_addr.sin_family = AF_INET;    // familia de protocolos
   server_addr.sin_port = port;         // porta servidor
   Connect(sockfd, host, &server_addr); // connect() wrapper

   show_server_info(sockfd, server_addr); // show server peer IP and port
   show_local_info(sockfd);               // show local IP and port

   pid_t child_pid = Fork();

   if (child_pid == 0) // child
   {
      for (;;)
      {
         Read(STDIN_FILENO, buffer, BUFFER_SIZE); // read() wrapper

         if (strcmp(buffer, "exit\n") == 0) // check if received exit from stdin
         {
            exit(0);
         }
      }
   }
   else // parent
   {
      for (;;)
      {
         Read(sockfd, buffer, BUFFER_SIZE); // read() wrapper

         if (strcmp(buffer, "exit") == 0) // check if server sent exit
         {
            exit(0);
         }

         execute(buffer, buffer); // executa o comando recebido pelo servidor e guarda o retorno em buffer

         Write(sockfd, buffer); // write() wrapper
      }
      waitpid(child_pid, NULL, 0); // wait for child process to finish
   }

   return 0;
}
