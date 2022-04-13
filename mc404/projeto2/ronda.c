#include "api_robot.h"

int _start() {
	setMotor(0, 10);
	setMotor(1, 10);
	int actualTime = get_time();
	int timeBase = actualTime;
	int timeBaseAux;
	int aux;
	int i = 1;
	int sonar3 = 2000;
	int sonar4 = 2000;
	int wall = 0;

	while (1) {
		if (i==50){
			i=1;
		}
		set_time(0);

		/*vira*/
		if (!wall) { // se nao encontrou parede, vira 90 graus para a direita
			actualTime = get_time();
			timeBase = actualTime;
			setMotor(0, 0);
			while (actualTime < timeBase + 1950) {
				actualTime = get_time();
			}
			setMotor(0, 10);
		}
		/*reto*/
		actualTime = get_time();
		timeBase = actualTime;	
		aux = actualTime;
		while (actualTime < timeBase + i) { // segue reto até actualTime + i
			if (actualTime != aux) {
				aux = actualTime;
				sonar3 = read_sonar(3); // sonares dianteiros
				sonar4 = read_sonar(4);
			}
			if (sonar3 < 1500 || sonar4 < 1500) { // se esta perto da parede
				/*sonar*/
				wall = 1; // encontrou parede
				actualTime = get_time();
				timeBaseAux = actualTime;
				setMotor(0, 0);
				while (actualTime < timeBaseAux + 1950){ // vira 90 graus para a direita
					actualTime = get_time();
				}
				setMotor(0, 10);
				sonar3 = read_sonar(3); // le os sonares novamente
				sonar4 = read_sonar(4);
				break; // cancela a iteracao atual e passa para a proxima
			} else {
				wall = 0; // nao encontrou parede
			}
			actualTime = get_time();
		}
		i++;
	}
	return 0;
}

void setMotor(int m, int v) {
	motor_cfg_t motor;
	motor.id = m;
	motor.speed = v;
	set_motor_speed(&motor);
}