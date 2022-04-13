#include "api_robot.h"

int _start() {
	setMotor(0, 20);
	int i =0;
	setMotor(1, 20);
	
	int s1;
	int s2;
	int s3;
	int s4;
	while(1)
	{
		s1 = read_sonar(3);//le sonares frontais
		s2 = read_sonar(4);//le sonares frontais
		s3 = read_sonar(5);//le sonares frontais
		s4 = read_sonar(2);//le sonares frontais
		if(s1<=1200||s2<=1200||s3<=1200||s4<=1200)//verifica se encontrou alguma parede
		{
			setMotor(1, 0);
			setMotor(0, 2);

		}
		s1 = read_sonar(7);
		s2 = read_sonar(8);
		if(s1<=1350  && abs(s1-s2)<=20) ///verifica se o robo esta paralelo a parede 
		{

			setMotor(1, 0);
			setMotor(0, 0);
			break;

		}
	}
	
	setMotor(1, 8);//inicia o robo quando o mesmo ja esta paralelo
	setMotor(0, 8);//inicia o robo quando o mesmo ja esta paralelo

	while(1)
	{
		
		s1 = read_sonar(7);// le os sonares laterais
		s2 = read_sonar(4);// le os sonares frontais
		s3 = read_sonar(6);// le os sonares laterais

		if (s2<1000) //verifica se o robo tem uma parde a frente
		{
			setMotor(1, 0);//vira para esquerda
			setMotor(0, 8);//vira para esquerda
			while (1) 
			{
				s2 = read_sonar(4);
				if(s2>1200)//verifica se a frente ficou livre
				{
					setMotor(1, 8);//volta a andar normalmente
					setMotor(0, 8);
					break;	
				}
			}
		}
		if (s1>500 && s3>500) //ve se o robo esta mto longe da parede
		{
			setMotor(0, 4);
			setMotor(1, 8);
		} else
		if (s1<40 || s3<400) //ve se esta mto perto
		{
			setMotor(1, 4);
			setMotor(0, 8);
		} else
		{
			setMotor(1, 8);
			setMotor(0, 8);
		}	
	}
	return 0;
}

void setMotor(int m, int v) {
	motor_cfg_t motor;
	motor.id = m;
	motor.speed = v;
	set_motor_speed(&motor);
}

int abs(int a){
	if (a < 0){
		return -a;
	}
	return a;
}
