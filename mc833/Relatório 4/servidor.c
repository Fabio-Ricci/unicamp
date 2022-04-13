// Fábio Camargo Ricci - 170781

#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include <netdb.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <time.h>
#include <unistd.h>
#include <arpa/inet.h>

#define BUFFER_SIZE 100

int Socket(sa_family_t family, int type, int flags)
{
   int sockfd;

   if ((sockfd = socket(family, type, flags)) < 0) // cria socket
   {
      perror("socket");
      exit(1);
   }

   return sockfd;
}

void Bind(int listenfd, sa_family_t family, in_addr_t s_addr, in_port_t port)
{
   struct sockaddr_in addr;

   bzero(&addr, sizeof(addr));    // inicializa addr (preenche memória com zeros)
   addr.sin_family = family;      // IPv4
   addr.sin_addr.s_addr = s_addr; // aceita conexões em todos os IPs disponíveis
   addr.sin_port = port;          // força o sistema a escolher uma porta aleatória disponível ao chamar bind()

   if (bind(listenfd, (struct sockaddr *)&addr, sizeof(addr)) == -1) // faz o bind() do endereço obtido com o socket sockfd
   {
      perror("bind");
      exit(1);
   }
}

void Listen(int listenfd, int backlog)
{
   if (listen(listenfd, backlog) == -1) // espera por conexões no socket sockfd (sockfd vira um socket passivo)
   {
      perror("listen");
      exit(1);
   }
}

int Accept(int listenfd, struct sockaddr_in *addr)
{
   int connfd;
   socklen_t len = sizeof(*addr);

   if ((connfd = accept(listenfd, (struct sockaddr *)addr, &len)) == -1) // aceita uma conexão no socket (cria um novo socket de conexão connfd)
   {
      perror("accept");
      exit(1);
   }

   return connfd;
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

void show_server_info(int sockfd)
{
   struct sockaddr_in addr;
   char name[128];

   Getsockname(sockfd, &addr); // getsockname() wrapper

   if (inet_ntop(AF_INET, &(addr.sin_addr), name, sizeof(name)) < 0) // recupera string IPv4 do endereço
   {
      perror("inet_ntop");
      exit(1);
   }

   printf("Listening on %s port %d\n\n", name, ntohs(addr.sin_port));
}

void show_client_connected_info(int sockfd, struct sockaddr_in addr)
{
   char name[128];
   time_t ticks;

   ticks = time(NULL);

   if (inet_ntop(AF_INET, &(addr.sin_addr), name, sizeof(name)) < 0) // recupera string IPv4 do endereço
   {
      perror("inet_ntop error");
      exit(1);
   }

   printf("Client with IP: %s Port: %d connected on: %s\n", name, ntohs(addr.sin_port), ctime(&ticks));
}

void show_client_disconnected_info(int sockfd, struct sockaddr_in addr)
{
   char name[128];
   time_t ticks;

   ticks = time(NULL);

   if (inet_ntop(AF_INET, &(addr.sin_addr), name, sizeof(name)) < 0) // recupera string IPv4 do endereço
   {
      perror("inet_ntop error");
      exit(1);
   }

   printf("Client with IP: %s Port: %d disconnected on: %s\n", name, ntohs(addr.sin_port), ctime(&ticks));
}

void handle_client(int connfd, struct sockaddr_in addr)
{
   show_client_connected_info(connfd, addr);

   sleep(10);

   show_client_disconnected_info(connfd, addr);

   shutdown(connfd, SHUT_RDWR);

   close(connfd); // fecha conexão
}

int main(int argc, char **argv)
{
   char error[BUFFER_SIZE + 1];

   if (argc != 2)
   {
      strcpy(error, "uso: ");
      strcat(error, argv[0]);
      strcat(error, " <Backlog>");
      perror(error);
      exit(1);
   }

   int backlog = atoi(argv[1]); // backlog

   int listenfd = Socket(AF_INET, SOCK_STREAM, 0); // socket() wrapper

   Bind(listenfd, AF_INET, htonl(INADDR_ANY), 0); // bind() wrapper

   Listen(listenfd, backlog); // listen() wrapper

   show_server_info(listenfd);

   int connfd;
   struct sockaddr_in client_addr;
   pid_t child_pid;

   for (;;) // loop aceitando conexões que cheguem
   {
      connfd = Accept(listenfd, &client_addr); // accept() wrapper

      child_pid = Fork(); // fork process to handle client and accept future concurrent connections
      if (child_pid == 0)
      {
         close(listenfd); // fecha o listen socket caso esteja no processo filho (não afeta o pai)
         handle_client(connfd, client_addr);
         exit(0);
      }
      else
      {
         close(connfd); // fecha o connection socket caso esteja no processo pai (não afeta o filho)
      }
   }

   return 0;
}
