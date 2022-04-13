// Fábio Camargo Ricci  -  170781

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
#define MAXDATASIZE 100

int main(int argc, char **argv)
{
   int listenfd, connfd;        // sockets
   struct sockaddr_in servaddr; // endereço do socket
   char buf[MAXDATASIZE];       // buffer
   time_t ticks;

   struct sockaddr_in addr;
   socklen_t len = sizeof(addr);
   char name[128];

   if ((listenfd = socket(AF_INET, SOCK_STREAM, 0)) == -1) // cria socket
   {
      perror("socket");
      exit(1);
   }

   bzero(&servaddr, sizeof(servaddr));           // inicializa servaddr (preenche memória com zeros)
   servaddr.sin_family = AF_INET;                // IPv4
   servaddr.sin_addr.s_addr = htonl(INADDR_ANY); // aceita conexões em todos os IPs disponíveis
   servaddr.sin_port = 0;                        // força o sistema a escolher uma porta aleatória disponível ao chamar bind()

   if (bind(listenfd, (struct sockaddr *)&servaddr, sizeof(servaddr)) == -1) // faz o bind() do endereço obtido com o socket listenfd
   {
      perror("bind");
      exit(1);
   }

   if (listen(listenfd, LISTENQ) == -1) // espera por conexões no socket listenfd (listenfd vira um socket passivo)
   {
      perror("listen");
      exit(1);
   }

   // informação do socket local
   if (getsockname(listenfd, (struct sockaddr *)&addr, &len) < 0) // recupera informação do endereço do socket
   {
      perror("getsocketname");
      exit(1);
   }

   if (inet_ntop(AF_INET, &(addr.sin_addr), name, sizeof(name)) < 0) // recupera string IPv4 do endereço
   {
      perror("inet_ntop");
      exit(1);
   }

   printf("Listening on %s port %d\n\n", name, ntohs(addr.sin_port));

   for (;;) // loop aceitando conexões que cheguem
   {
      if ((connfd = accept(listenfd, (struct sockaddr *)NULL, NULL)) == -1) // aceita uma conexão no socket (cria um novo socket de conexão connfd)
      {
         perror("accept");
         exit(1);
      }

      // informações do socket cliente
      if (getpeername(connfd, (struct sockaddr *)&addr, &len) < 0) // recupera informação do endereço do socket
      {
         perror("getpeername");
         exit(1);
      }

      if (inet_ntop(AF_INET, &(addr.sin_addr), name, sizeof(name)) < 0) // recupera string IPv4 do endereço
      {
         perror("inet_ntop error");
         exit(1);
      }

      printf("Client connected on %s port %d\n", name, ntohs(addr.sin_port));

      ticks = time(NULL);
      snprintf(buf, sizeof(buf), "%.24s\r\n", ctime(&ticks)); // print horário atual em um buffer de saída
      write(connfd, buf, strlen(buf));                        // escreve o conteúdo do buffer no socket de conxão

      close(connfd); // fecha conexão
   }

   return (0);
}
