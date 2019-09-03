#ifndef __STABILIZER_TYPES_H
#define __STABILIZER_TYPES_H
//#include "sys.h"
#include <stdbool.h>
#include "sensors_types.h"

/********************************************************************************
 * ������ֻ��ѧϰʹ�ã�δ��������ɣ��������������κ���;
 * ATKflight�ɿع̼�
 * �ṹ�����Ͷ���
 * ����ԭ��@ALIENTEK
 * ������̳:www.openedv.com
 * ��������:2018/5/2
 * �汾��V1.0
 * ��Ȩ���У�����ؾ���
 * Copyright(C) ������������ӿƼ����޹�˾ 2014-2024
 * All rights reserved
********************************************************************************/


#define RATE_5_HZ		5
#define RATE_10_HZ		10
#define RATE_20_HZ		20
#define RATE_25_HZ		25
#define RATE_50_HZ		50
#define RATE_100_HZ		100
#define RATE_200_HZ 	200
#define RATE_250_HZ 	250
#define RATE_500_HZ 	500
#define RATE_1000_HZ 	1000

#define RATE_DO_EXECUTE(RATE_HZ, TICK) ((TICK % (RATE_1000_HZ / RATE_HZ)) == 0)


//��̬���ݽṹ
typedef struct
{
	uint32_t timestamp;	/*ʱ���*/
	float roll;
	float pitch;
	float yaw;
} attitude_t;

struct  vec3_s
{
	uint32_t timestamp;
	float x;
	float y;
	float z;
};

typedef struct vec3_s point_t;
typedef struct vec3_s velocity_t;
typedef struct vec3_s acc_t;

//Z����봫�������ݽṹ
typedef struct zDistance_s
{
	uint32_t timestamp;
	float distance;
} zDistance_t;

//�������ݽṹ
typedef struct flowMeasurement_s
{
	uint32_t timestamp;
	union
	{
		struct
		{
			float dpixelx;  // Accumulated pixel count x
			float dpixely;  // Accumulated pixel count y
		};
		float dpixel[2];  // Accumulated pixel count
	};
	float stdDevX;      // Measurement standard deviation
	float stdDevY;      // Measurement standard deviation
	float dt;           // Time during which pixels were accumulated
} flowMeasurement_t;

//TOF���ݽṹ
typedef struct tofMeasurement_s
{
	uint32_t timestamp;
	float distance;
	float stdDev;
} tofMeasurement_t;

//��ѹ���ݽṹ
typedef struct
{
	uint32_t timestamp;
	float pressure;
	float temperature;
	uint16_t asl;
} baro_t;

//���д��������ݼ���
typedef struct
{
	Axis3f acc;				//���ٶȣ�G��
	Axis3f gyro;			//�����ǣ�deg/s��
	Axis3f mag;				//�����ƣ�gauss��
	baro_t baro;
} sensorData_t;

//������̬���ݽṹ
typedef struct
{
	attitude_t 	attitude;	//��̬�Ƕȣ�deg��
	point_t 	position;	//�����λ�ã�cm��
	velocity_t 	velocity;	//������ٶȣ�cm/s��
	acc_t acc;				//����ļ��ٶȣ�cm/ss��
} state_t;


typedef enum
{
	modeDisable = 0,
	modeAbs,
	modeVelocity
} mode_e;

typedef struct
{
	mode_e x;
	mode_e y;
	mode_e z;
	mode_e roll;
	mode_e pitch;
	mode_e yaw;
}mode_tt;

//Ŀ����̬���ݽṹ
typedef struct
{
	attitude_t attitude;		//Ŀ����̬�Ƕȣ�deg��
	attitude_t attitudeRate;	//Ŀ����ٶȣ�deg/s��
	point_t position;         	//Ŀ��λ�ã�cm��
	velocity_t velocity;      	//Ŀ���ٶȣ�cm/s��
	mode_tt mode;
	float thrust;
} setpoint_t;

//�������ݽṹ
typedef struct
{
	float roll;
	float pitch;
	float yaw;
	float thrust;
} control_t;


#endif

