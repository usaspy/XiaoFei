#ifndef __IMU_H
#define __IMU_H

//#include "axis.h"
#include "maths.h"
#include "stabilizer_types.h"

typedef struct AHRS
{
        float roll;
        float pitch;
        float yaw;
}AHRS, *StructPointer;

/********************************************************************************
 * 本程序只供学习使用，未经作者许可，不得用于其它任何用途
 * ATKflight飞控固件
 * 姿态解算驱动代码
 * 正点原子@ALIENTEK
 * 技术论坛:www.openedv.com
 * 创建日期:2018/5/2
 * 版本：V1.2
 * 版权所有，盗版必究。
 * Copyright(C) 广州市星翼电子科技有限公司 2014-2024
 * All rights reserved
********************************************************************************/

extern float imuAttitudeYaw;

void imuInit(void);
void imuTransformVectorBodyToEarth(Axis3f * v);
void imuTransformVectorEarthToBody(Axis3f * v);
void imuUpdateAttitude(const sensorData_t *sensorData, state_t *state, float dt);
StructPointer imuUpdateEA(float gx, float gy, float gz, float ax, float ay, float az, float mx, float my, float mz, float dt);
#endif