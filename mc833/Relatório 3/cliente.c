// Fábio Camargo Ricci  -  170781

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

#define MAXLINE 4096

int main(int argc, char **argv)
{
   int sockfd, n;
   char recvline[MAXLINE + 1];
   char error[MAXLINE + 1];
   struct sockaddr_in servaddr;

   struct sockaddr_in addr;
   socklen_t len = sizeof(addr);
   char name[128];

   if (argc != 3)
   {
      strcpy(error, "uso: ");
      strcat(error, argv[0]);
      strcat(error, " <IPaddress> <Port>");
      perror(error);
      exit(1);
   }

   if ((sockfd = socket(AF_INET, SOCK_STREAM, 0)) < 0) // cria o socket
   {
      perror("socket error");
      exit(1);
   }

   bzero(&servaddr, sizeof(servaddr));
   servaddr.sin_family = AF_INET;                            // IPv4
   servaddr.sin_port = htons(atoi(argv[2]));                 // porta servidor
   if (inet_pton(AF_INET, argv[1], &servaddr.sin_addr) <= 0) // converte o endereço IP do servidor em representação binária
   {
      perror("inet_pton error");
      exit(1);
   }

   if (connect(sockfd, (struct sockaddr *)&servaddr, sizeof(servaddr)) < 0)
   {
      perror("connect error");
      exit(1);
   }

   // informações do socket local
   if (getsockname(sockfd, (struct sockaddr *)&addr, &len) < 0) // recupera informação do endereço do socket
   {
      perror("getsocketname");
      exit(1);
   }

   if (inet_ntop(AF_INET, &(addr.sin_addr), name, sizeof(name)) < 0) // recupera string IPv4 do endereço
   {
      perror("inet_ntop");
      exit(1);
   }

   printf("Connected on %s port %d\n\n", name, ntohs(addr.sin_port));

   while ((n = read(sockfd, recvline, MAXLINE)) > 0)
   {
      recvline[n] = 0;
      if (fputs(recvline, stdout) == EOF)
      {
         perror("fputs error");
         exit(1);
      }
   }

   if (n < 0)
   {
      perror("read error");
      exit(1);
   }

   exit(0);
}
