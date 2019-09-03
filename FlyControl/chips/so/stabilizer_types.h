#ifndef __STABILIZER_TYPES_H
#define __STABILIZER_TYPES_H
//#include "sys.h"
#include <stdbool.h>
#include "sensors_types.h"

/********************************************************************************
 * 本程序只供学习使用，未经作者许可，不得用于其它任何用途
 * ATKflight飞控固件
 * 结构体类型定义
 * 正点原子@ALIENTEK
 * 技术论坛:www.openedv.com
 * 创建日期:2018/5/2
 * 版本：V1.0
 * 版权所有，盗版必究。
 * Copyright(C) 广州市星翼电子科技有限公司 2014-2024
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


//姿态数据结构
typedef struct
{
	uint32_t timestamp;	/*时间戳*/
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

//Z轴距离传感器数据结构
typedef struct zDistance_s
{
	uint32_t timestamp;
	float distance;
} zDistance_t;

//光流数据结构
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

//TOF数据结构
typedef struct tofMeasurement_s
{
	uint32_t timestamp;
	float distance;
	float stdDev;
} tofMeasurement_t;

//气压数据结构
typedef struct
{
	uint32_t timestamp;
	float pressure;
	float temperature;
	uint16_t asl;
} baro_t;

//所有传感器数据集合
typedef struct
{
	Axis3f acc;				//加速度（G）
	Axis3f gyro;			//陀螺仪（deg/s）
	Axis3f mag;				//磁力计（gauss）
	baro_t baro;
} sensorData_t;

//四轴姿态数据结构
typedef struct
{
	attitude_t 	attitude;	//姿态角度（deg）
	point_t 	position;	//估算的位置（cm）
	velocity_t 	velocity;	//估算的速度（cm/s）
	acc_t acc;				//估算的加速度（cm/ss）
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

//目标姿态数据结构
typedef struct
{
	attitude_t attitude;		//目标姿态角度（deg）
	attitude_t attitudeRate;	//目标角速度（deg/s）
	point_t position;         	//目标位置（cm）
	velocity_t velocity;      	//目标速度（cm/s）
	mode_tt mode;
	float thrust;
} setpoint_t;

//控制数据结构
typedef struct
{
	float roll;
	float pitch;
	float yaw;
	float thrust;
} control_t;


#endif

