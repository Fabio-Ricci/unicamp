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

#define LISTENQ 10
#define BUFFER_SIZE 4096

char *gameMatrix[3][3] = {
    {"Draw", "Win", "Lose"},
    {"Lose", "Draw", "Win"},
    {"Win", "Lose", "Draw"},
};
char *movesNames[3] = {"Rock", "Paper", "Scizors"};

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

void show_connected_info(int clientId, int sockfd, struct sockaddr_in addr)
{
   char name[128];
   time_t ticks;

   ticks = time(NULL);

   if (inet_ntop(AF_INET, &(addr.sin_addr), name, sizeof(name)) < 0) // recupera string IPv4 do endereço
   {
      perror("inet_ntop error");
      exit(1);
   }

   printf("Client (ID: %d) with IP: %s Port: %d connected time: %s\n", clientId, name, ntohs(addr.sin_port), ctime(&ticks));
}

void show_disconnected_info(int clientId, int sockfd, struct sockaddr_in addr)
{
   char name[128];
   time_t ticks;

   ticks = time(NULL);

   if (inet_ntop(AF_INET, &(addr.sin_addr), name, sizeof(name)) < 0) // recupera string IPv4 do endereço
   {
      perror("inet_ntop error");
      exit(1);
   }

   printf("Client (ID: %d) with IP: %s Port: %d disconnected on: %s\n", clientId, name, ntohs(addr.sin_port), ctime(&ticks));
}

void handle_client(int clientId, int connfd, struct sockaddr_in addr)
{
   int score = 0;
   char buffer[BUFFER_SIZE];

   show_connected_info(clientId, connfd, addr);

   for (;;)
   {
      snprintf(buffer, sizeof(buffer), "Select an option:\n 1. Play against server\n 2. Quit\n");
      Write(connfd, buffer);

      // read command
      if (Read(connfd, buffer, BUFFER_SIZE) == 0) // 0 significa desconexão com sucesso
      {
         break;
      }

      if (buffer[0] == '1')
      { // vs server
         snprintf(buffer, sizeof(buffer), "Select your move:\n 1. Rock\n 2. Paper\n 3. Scizors\n");
         Write(connfd, buffer);

         // read move
         if (Read(connfd, buffer, BUFFER_SIZE) == 0) // 0 significa desconexão com sucesso
         {
            break;
         }

         int serverMove = rand() % 3;          // random move 0 (rock), 1 (paper) or 2 (scizors)
         int clientMove = (int)buffer[0] - 49; // parse client move

         char *gameRes = gameMatrix[serverMove][clientMove];
         if (strcmp(gameRes, "Win") == 0)
         {
            score++;
         }

         snprintf(buffer, sizeof(buffer), "You played: %s\nServer played: %s\n%s!\nYour score: %d\n", movesNames[clientMove], movesNames[serverMove], gameRes, score);
         Write(connfd, buffer);
      }
      else if (buffer[0] == '2')
      { // quit
         break;
      }
   }

   show_disconnected_info(clientId, connfd, addr);

   shutdown(connfd, SHUT_RDWR);
   close(connfd); // fecha conexão
}

int main(int argc, char **argv)
{
   int clientId = 1;
   int listenfd = Socket(AF_INET, SOCK_STREAM, 0); // socket() wrapper

   Bind(listenfd, AF_INET, htonl(INADDR_ANY), 0); // bind() wrapper

   Listen(listenfd, LISTENQ); // listen() wrapper

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
         handle_client(clientId, connfd, client_addr);
         break;
      }
      else
      {
         close(connfd); // fecha o connection socket caso esteja no processo pai (não afeta o filho)
      }

      clientId++;
   }

   return 0;
}
