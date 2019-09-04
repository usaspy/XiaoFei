#include <stdbool.h>
#include <stdint.h>
#include <math.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include "axis.h"
#include "maths.h"
#include "imu.h"
#include "stabilizer_types.h"
attitude_t attitude;
/**
 * 姿态解算规则如下：
 *     ROLL  = 绕X轴旋转，右手定则，逆时针为正顺时针为负。
 *     PITCH = 绕Y轴旋转，右手定则，逆时针为正顺时针为负。
 *     YAW   = 绕Z轴旋转，右手定则，逆时针为正顺时针为负。
 */

#define DCM_KP_ACC			0.600f		//加速度补偿陀螺仪PI参数
#define DCM_KI_ACC			0.005f

#define DCM_KP_MAG			1.000f		//磁力计补偿陀螺仪PI参数
#define DCM_KI_MAG			0.000f

#define IMU_SMALL_ANGLE		15.0f		//满足水平状态的最小角度（单位deg）

#define SPIN_RATE_LIMIT     20			//旋转速率
#define DEADBAND            0.45        //死区
#define DEADBAND_YAW            0.45        //死区
static float q0 = 1.0f, q1 = 0.0f, q2 = 0.0f, q3 = 0.0f;//四元数
static float rMat[3][3];//四元数的旋转矩阵
static float smallAngleCosZ;//水平最小角余弦值

static float invSqrt(float x)
{
    return 1.0f / sqrtf(x);
}

static void imuComputeRotationMatrix(void)
{
    float q1q1 = q1 * q1;
    float q2q2 = q2 * q2;
    float q3q3 = q3 * q3;

    float q0q1 = q0 * q1;
    float q0q2 = q0 * q2;
    float q0q3 = q0 * q3;
    float q1q2 = q1 * q2;
    float q1q3 = q1 * q3;
    float q2q3 = q2 * q3;

    rMat[0][0] = 1.0f - 2.0f * q2q2 - 2.0f * q3q3;
    rMat[0][1] = 2.0f * (q1q2 + -q0q3);
    rMat[0][2] = 2.0f * (q1q3 - -q0q2);

    rMat[1][0] = 2.0f * (q1q2 - -q0q3);
    rMat[1][1] = 1.0f - 2.0f * q1q1 - 2.0f * q3q3;
    rMat[1][2] = 2.0f * (q2q3 + -q0q1);

    rMat[2][0] = 2.0f * (q1q3 + -q0q2);
    rMat[2][1] = 2.0f * (q2q3 - -q0q1);
    rMat[2][2] = 1.0f - 2.0f * q1q1 - 2.0f * q2q2;
}


static void imuMahonyAHRSupdate(float gx, float gy, float gz,
                                float ax, float ay, float az,
                                float mx, float my, float mz,
								bool useMag,float dt)
{
	static float integralAccX = 0.0f,  integralAccY = 0.0f, integralAccZ = 0.0f;    //加速度积分误差
	static float integralMagX = 0.0f,  integralMagY = 0.0f, integralMagZ = 0.0f;    //磁力计积分误差
	float ex, ey, ez;

    //计算旋转速率(rad/s)
    const float spin_rate_sq = sq(gx) + sq(gy) + sq(gz);

    //Step 1: Yaw correction
    if (useMag)
	{
		const float magMagnitudeSq = mx * mx + my * my + mz * mz;
		float kpMag = DCM_KP_MAG * 10.0f;//imuMagFastPGainSaleFactor();

		if (magMagnitudeSq > 0.01f)
		{
			//单位化磁力计测量值
			const float magRecipNorm = invSqrt(magMagnitudeSq);
			mx *= magRecipNorm;
			my *= magRecipNorm;
			mz *= magRecipNorm;

			//计算X\Y方向的磁通，磁北方向磁通
			const float hx = rMat[0][0] * mx + rMat[0][1] * my + rMat[0][2] * mz;
			const float hy = rMat[1][0] * mx + rMat[1][1] * my + rMat[1][2] * mz;
			const float bx = sqrtf(hx * hx + hy * hy);

			//磁力计误差是估计磁北和测量磁北之间的交叉乘积
			const float ez_ef = -(hy * bx);

			//旋转误差到机体坐标系
			ex = rMat[2][0] * ez_ef;
			ey = rMat[2][1] * ez_ef;
			ez = rMat[2][2] * ez_ef;
		}
		else
		{
			ex = 0;
			ey = 0;
			ez = 0;
		}

		//累计误差补偿
		if (DCM_KI_MAG > 0.0f)
		{
			//如果旋转速率大于限制值则停止积分
			if (spin_rate_sq < sq(DEGREES_TO_RADIANS(SPIN_RATE_LIMIT)))
			{
				integralMagX += DCM_KI_MAG * ex * dt;
				integralMagY += DCM_KI_MAG * ey * dt;
				integralMagZ += DCM_KI_MAG * ez * dt;

				gx += integralMagX;
				gy += integralMagY;
				gz += integralMagZ;
			}
		}

		//误差补偿
		gx += kpMag * ex;
		gy += kpMag * ey;
		gz += kpMag * ez;
	}


    //Step 2: Roll and pitch correction
	if(!((ax == 0.0f) && (ay == 0.0f) && (az == 0.0f)))
	{
		//单位化加速计测量值
		const float accRecipNorm = invSqrt(ax * ax + ay * ay + az * az);
		ax *= accRecipNorm;
		ay *= accRecipNorm;
		az *= accRecipNorm;

		//加速计读取的方向与重力加速计方向的差值，用向量叉乘计算
		ex = (ay * rMat[2][2] - az * rMat[2][1]);
		ey = (az * rMat[2][0] - ax * rMat[2][2]);
		ez = (ax * rMat[2][1] - ay * rMat[2][0]);

		//累计误差补偿
		if (DCM_KI_ACC > 0.0f)
		{
			//如果旋转速率大于限制值则停止积分
			if (spin_rate_sq < sq(DEGREES_TO_RADIANS(SPIN_RATE_LIMIT)))
			{
				integralAccX += DCM_KI_ACC * ex * dt;
				integralAccY += DCM_KI_ACC * ey * dt;
				integralAccZ += DCM_KI_ACC * ez * dt;

				gx += integralAccX;
				gy += integralAccY;
				gz += integralAccZ;
			}
		}

		//误差补偿
		gx += DCM_KP_ACC * ex;
		gy += DCM_KP_ACC * ey;
		gz += DCM_KP_ACC * ez;
	}

	//一阶近似算法，四元数运动学方程的离散化形式和积分
    gx *= (0.5f * dt);
    gy *= (0.5f * dt);
    gz *= (0.5f * dt);

    const float qa = q0;
    const float qb = q1;
    const float qc = q2;
    q0 += (-qb * gx - qc * gy - q3 * gz);
    q1 += (qa * gx + qc * gz - q3 * gy);
    q2 += (qa * gy - qb * gz + q3 * gx);
    q3 += (qa * gz + qb * gy - qc * gx);

	//单位化四元数
    const float quatRecipNorm = invSqrt(q0 * q0 + q1 * q1 + q2 * q2 + q3 * q3);
    q0 *= quatRecipNorm;
    q1 *= quatRecipNorm;
    q2 *= quatRecipNorm;
    q3 *= quatRecipNorm;

    //计算四元数的旋转矩阵
    imuComputeRotationMatrix();
}

float imuAttitudeYaw;//范围：-180~180，用于上传到匿名上位机（支持范围-180~180）

//更新欧拉角
static void imuUpdateEulerAngles(attitude_t *attitude)
{
	attitude->roll = fapplyDeadband(RADIANS_TO_DEGREES(atan2_approx(rMat[2][1], rMat[2][2])), DEADBAND);
	attitude->pitch = fapplyDeadband(RADIANS_TO_DEGREES((0.5f * M_PIf) - acos_approx(-rMat[2][0])), DEADBAND);//arcsin = 0.5PI - arccos
	attitude->yaw = fapplyDeadband(RADIANS_TO_DEGREES(atan2_approx(rMat[1][0], rMat[0][0])), DEADBAND_YAW);

	imuAttitudeYaw = attitude->yaw;

	if (attitude->yaw < 0.0f)//转换位0~360
		attitude->yaw += 360.0f;
    /*
	//更新最小倾角状态
	if (rMat[2][2] > smallAngleCosZ)
		//ENABLE_STATE(SMALL_ANGLE);
	else
		//DISABLE_STATE(SMALL_ANGLE);
	*/
}

/*
主函数，通过9轴原始数据计算欧拉角
*/
void imuUpdateAttitude(const sensorData_t *sensorData, state_t *state, float dt)
{
	//bool useMag = compassIsHealthy();

	Axis3f gyro = sensorData->gyro;
	Axis3f acc  = sensorData->acc;
	Axis3f mag  = sensorData->mag;

	//角速度单位由度转为弧度
	gyro.x = gyro.x * DEG2RAD;
	gyro.y = gyro.y * DEG2RAD;
	gyro.z = gyro.z * DEG2RAD;

	//计算四元数和旋转矩阵

    imuMahonyAHRSupdate(gyro.x, gyro.y, gyro.z,
                        acc.x, acc.y, acc.z,
                        mag.x, mag.y, mag.z,
						true,dt);

    //计算欧拉角
    imuUpdateEulerAngles(&state->attitude);
}

/*
初始化。。。
*/
void imuInit(void)
{
	smallAngleCosZ = cos_approx(degreesToRadians(IMU_SMALL_ANGLE));//最小倾角余弦值
    imuComputeRotationMatrix();
}

/*
计算返回当前得欧拉角
add by zhanghong
*/
StructPointer imuUpdateEA(float gx, float gy, float gz,
                                float ax, float ay, float az,
                                float mx, float my, float mz, float dt)
{
        StructPointer p = (StructPointer)malloc(sizeof(AHRS));

        //角速度单位由度转为弧度    DEG2RAD = Π/180
	    gx = gx * DEG2RAD;
	    gy = gy * DEG2RAD;
	    gz = gz * DEG2RAD;

	    //计算四元数和旋转矩阵
        imuMahonyAHRSupdate(gx, gy, gz,
                        ax, ay, az,
                        mx, my, mz,
						true,dt);

        //计算欧拉角
        imuUpdateEulerAngles(&attitude);

        p->roll = attitude.roll;
        p->pitch = attitude.pitch;
        p->yaw = attitude.yaw;

        return p;
}