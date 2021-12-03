# XiaoFei  "小飞"四轴飞行器控制器(v0.9.4) 功能介绍

XiaoFei"小飞"是一个用于四轴无人机的飞行控制系统，目前仅支持X字型布局，通过4G移动网络进行飞行姿态控制和数据回传，可遥距飞行，一键回航.

硬件清单：树莓派3b+、 MPU9250陀螺仪、SIM7600 4G模块、外置GPS天线、DC5v-12V稳压电源、光电耦合模块、4G通信天线、动力电池(3S)、机架、电机、螺旋桨
软件清单：XiaoFei地面站、XiaoFei飞控

*****************飞控 FlyControl*****************
包括以下子系统：
1.飞行姿态控制系统（带自稳功能）
       启动后自检，起飞后自动在0.2米高度完成自稳转速比设置（标准转速比），后续飞行分两个状态：
       1）自稳状态  当没有接收到人工控制指令时，自动进入自稳悬停状态（当前高度、位置不变）
           根据实时获取的欧拉角、加速度、海拔高度信息实现
       2）人工控制  当接收到人工控制指令，即在自稳状态基础上进行飞行状态调整。
2.姿态及环境参数探测系统 （欧拉角、加速度、气压、温度、海拔高度、离地高度）
        更新频率20~100HZ(默认50HZ)
3.GPS导航(经度、纬度、海拔高度)
        更新频率1HZ
4.通信链路系统（人工操作、地图标注航行、视频传输）
        系统启动后自动打开通信链路，与地面站建立长连接，并发送心跳检测链接状态，一旦与地面站断开，即自动重连。
        状态检测：GPRS断开需重新建立拨号连接，并重建与地面站连接
        1)接收人工下发飞行指令:
          上升、
          下降、 
          前进、
          后退、
          左移、
          右移、
          起飞、
          降落、
          悬停;
        2)地图标注航行:
            人工在控制台上规划路径，生成航行点轨迹坐标，飞行器可根据航行点自动巡航。     
        3）视频传输   
           将实时视频通过4G模块走移动基站下传到PC上，并在遥控地面站上

*****************飞行地面站  GroundStation*****************
1.显示实时欧拉角度、海拔、地速
2.通过键盘控制飞行器的飞行
3.
