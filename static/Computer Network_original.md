## 1. 单交换机的VLAN划分
需求：使用单交换机进行vlan划分，使得PC0 PC1在一个vlan内，可以相互ping通，PC2 PC3在一个vlan内，可以相互ping通
## 1.1 前述知识
不同vlan间的主机不能直接通信，需要通过路由器或三层交换机等网络层设备进行转发，设备提供vlan接口实现对报文进行三层转发的功能。

vlan接口是一种三层模式下的虚拟接口，主要用于实现vlan间的三层互通，它不作为物理实体存在于设备上。每个vlan对应一个vlan接口，**在为vlan接口配置了ip地址后，该接口即可作为本vlan内网络设备的网关**，对需要跨网段的报文进行基于ip地址的三层转发。
![image.png](https://cdn.nlark.com/yuque/0/2022/png/26910220/1652846478923-84ef384e-2f86-4102-a416-976b948ce7a2.png#clientId=u4d32acdb-ca6f-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=364&id=W6mM8&margin=%5Bobject%20Object%5D&name=image.png&originHeight=364&originWidth=608&originalType=binary&ratio=1&rotation=0&showTitle=false&size=19528&status=done&style=none&taskId=ue8c12f7f-1546-4a28-9c69-2384aeef358&title=&width=608)
## 1.2 具体操作
![image.png](https://cdn.nlark.com/yuque/0/2022/png/26910220/1652853069772-b5586f54-3a83-4c6d-b650-a14a05759873.png#clientId=u4d32acdb-ca6f-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=143&id=u9d2ebd3d&margin=%5Bobject%20Object%5D&name=image.png&originHeight=143&originWidth=542&originalType=binary&ratio=1&rotation=0&showTitle=false&size=4964&status=done&style=none&taskId=ud0aa8541-2503-4709-9f17-4be798cadb5&title=&width=542)

- 绘制拓扑图如上图所示
- 配置IP地址

![image.png](https://cdn.nlark.com/yuque/0/2022/png/26910220/1652852910070-1cd3198f-c964-4927-929c-c034242d3839.png#clientId=u4d32acdb-ca6f-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=204&id=ud33a1fc1&margin=%5Bobject%20Object%5D&name=image.png&originHeight=204&originWidth=695&originalType=binary&ratio=1&rotation=0&showTitle=false&size=51924&status=done&style=none&taskId=uae64e612-fc8c-4b25-ac76-e1dc0bedefc&title=&width=695)

- VLAN划分switch配置，按照如下状态划分

![image.png](https://cdn.nlark.com/yuque/0/2022/png/26910220/1652852933952-cea17327-6c96-4aec-a8ae-4190ece1f5f8.png#clientId=u4d32acdb-ca6f-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=339&id=u3896319f&margin=%5Bobject%20Object%5D&name=image.png&originHeight=339&originWidth=743&originalType=binary&ratio=1&rotation=0&showTitle=false&size=78301&status=done&style=none&taskId=uf9c99275-0d9e-41a8-a5be-1a1c4278757&title=&width=743)
```json
Switch>en
Switch#conf t                                //进入全局配置模式
Switch(config)#hostname Switch1              //修改交换机的名字
Switch1(config)#vlan 10                       //创建vlan 10
Switch1(config-vlan)#exit        
Switch1(config)#vlan 20                       //创建vlan 20
Switch1(config-vlan)#exit
Switch1(config)#int fa 0/1                    //打开0/1端口
Switch1(config-if)#switchport mode access     //设置接口为access
Switch1(config-if)#switchport access vlan 10  // 将端口换分到vlan 10中
Switch1(config-if)#exit
Switch1(config)#int fa 0/2                   //打开0/2端口
Switch1(config-if)#switchport mode access     //设置接口为access
Switch1(config-if)#switchport access vlan 10  // 将端口换分到vlan 20中
Switch1(config)#int fa 0/3                    //打开0/1端口
Switch1(config-if)#switchport mode access     //设置接口为access
Switch1(config-if)#switchport access vlan 20  // 将端口换分到vlan 10中
Switch1(config-if)#exit
Switch1(config)#int fa 0/4                   //打开0/2端口
Switch1(config-if)#switchport mode access     //设置接口为access
Switch1(config-if)#switchport access vlan 20  // 将端口换分到vlan 20中
Switch1(config-if)#exit
switch1#show vlan brief												// 查看vlan配置

```
## 
## 2. 跨交换机划分VLAN
需求：使用两个交换机，使得PC0 PC2处在一个vlan下可以ping通，PC1 PC3处在一个vlan下可以ping通。

### 2.1 前述知识
#### 2.1.1 关于switch中access和trunk模式
Access 类型的端口：只能属于1 个VLAN，一般用于连接计算机的端口；
Trunk 类型的端口：可以允许多个VLAN 通过，可以接收和发送多个VLAN 的报文，一般用于交换机之间连接的端口
> 1.[交换机接口类型Access和Trunk详解](https://blog.csdn.net/qq_42868577/article/details/121563476?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522165285368616782350921366%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=165285368616782350921366&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduend~default-1-121563476-null-null.142^v10^control,157^v4^new_style&utm_term=%E4%BA%A4%E6%8D%A2%E6%9C%BAaccess%E5%92%8Ctrunk&spm=1018.2226.3001.4187)
> 2.[交换机的Access口与Trunk口](https://blog.csdn.net/qq_20817327/article/details/120839493?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522165285368616782350921366%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=165285368616782350921366&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduend~default-3-120839493-null-null.142^v10^control,157^v4^new_style&utm_term=%E4%BA%A4%E6%8D%A2%E6%9C%BAaccess%E5%92%8Ctrunk&spm=1018.2226.3001.4187)

![image.png](https://cdn.nlark.com/yuque/0/2022/png/26910220/1652854843153-ce48316c-ac48-4821-9ad5-bee4898056c8.png#clientId=u4d32acdb-ca6f-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=549&id=u8c27bfac&margin=%5Bobject%20Object%5D&name=image.png&originHeight=549&originWidth=828&originalType=binary&ratio=1&rotation=0&showTitle=false&size=92161&status=done&style=none&taskId=ucc9aa214-9144-454c-805b-7549fc7ab78&title=&width=828)
### 2.2 具体操作
![image.png](https://cdn.nlark.com/yuque/0/2022/png/26910220/1652852833518-fe1c77c5-eb30-4d2f-8cc3-ddc1f874fdea.png#clientId=u4d32acdb-ca6f-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=280&id=u65e6f5b4&margin=%5Bobject%20Object%5D&name=image.png&originHeight=280&originWidth=598&originalType=binary&ratio=1&rotation=0&showTitle=false&size=13038&status=done&style=none&taskId=uf623895d-439c-4940-908f-67269b592b1&title=&width=598)
**基本流程如下图所示：**
![image.png](https://cdn.nlark.com/yuque/0/2022/png/26910220/1652853074348-f8fce2e4-c7f8-4b7a-bbf8-ed5e6da0cd95.png#clientId=u4d32acdb-ca6f-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=143&id=u3d08895a&margin=%5Bobject%20Object%5D&name=image.png&originHeight=143&originWidth=542&originalType=binary&ratio=1&rotation=0&showTitle=false&size=4964&status=done&style=none&taskId=u55b14d21-2a69-4678-904f-cb6bbb688a7&title=&width=542)

- 绘制拓扑图如上图所示
- 配置IP地址

![image.png](https://cdn.nlark.com/yuque/0/2022/png/26910220/1652852975202-47555131-da37-47b5-acf2-ff6f18495a8c.png#clientId=u4d32acdb-ca6f-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=270&id=xEn6L&margin=%5Bobject%20Object%5D&name=image.png&originHeight=270&originWidth=865&originalType=binary&ratio=1&rotation=0&showTitle=false&size=82174&status=done&style=none&taskId=u631fc7fe-9690-4097-8fe3-a2df677f6c2&title=&width=865)

- 配置switch0
```bash
Switch>en
Switch#conf t
# 划分vlan
Switch(config)#vlan 10
Switch(config-vlan)#exit
Switch(config)#vlan 20
Switch(config-vlan)#exit
Switch(config)#int fa 0/1
Switch(config-if)#switchport mode access 
Switch(config-if)#switchport access vlan 10
Switch(config-if)#exit
Switch(config)#int fa 0/2
Switch(config-if)#switchport mode access 
Switch(config-if)#switchport  access vlan 20
Switch(config-if)#exit
Switch(config)#exit

# 配置trunk
Switch(config)#int fa 0/12
Switch(config-if)#switchport mode trunk
Switch(config-if)#no shutdown
```

- 配置switch1
```bash
Switch>en
Switch#conf t
Enter configuration commands, one per line.  End with CNTL/Z.
Switch(config)#vlan 10
Switch(config-vlan)#exit
Switch(config)#vlan 20
Switch(config-vlan)#exit
Switch(config)#int fa 0/1
Switch(config-if)#switchport mode access
Switch(config-if)#switchport access vlan 10
Switch(config-if)#exit
Switch(config)#int fa 0/2
Switch(config-if)#switchport mode access
Switch(config-if)#switchport access vlan 20
Switch(config-if)#exit
Switch(config)#exit

# 配置trunk
Switch(config)#int fa 0/12
Switch(config-if)#switchport mode trunk
Switch(config-if)#no shutdown
```


## 3. 单臂路由
需求:使用单臂路由实现不同vlan之间的PC可以ping通
### 3.1 前述知识
> （1）[单臂路由实现原理](https://blog.csdn.net/weixin_44032232/article/details/107206924?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522165292703816781435440118%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=165292703816781435440118&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~top_positive~default-1-107206924-null-null.142^v10^control,157^v4^new_style&utm_term=%E5%8D%95%E8%87%82%E8%B7%AF%E7%94%B1%E5%8E%9F%E7%90%86&spm=1018.2226.3001.4187)
> （2）[802.1Q VLAN 简介](https://blog.csdn.net/u013490557/article/details/37512045?ops_request_misc=&request_id=&biz_id=102&utm_term=%E5%B0%81%E8%A3%85802.1q%E7%9A%84Vlan%E5%8D%8F%E8%AE%AE&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduweb~default-0-37512045.142^v11^control,157^v12^new_style&spm=1018.2226.3001.4187)


![image.png](https://cdn.nlark.com/yuque/0/2022/png/26910220/1652928865850-06459327-e3e0-4147-b871-7b80a904e335.png#clientId=u4d32acdb-ca6f-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=428&id=u3ca31201&margin=%5Bobject%20Object%5D&name=image.png&originHeight=428&originWidth=696&originalType=binary&ratio=1&rotation=0&showTitle=false&size=101877&status=done&style=none&taskId=u4356596c-c503-4761-86c6-4c04343a51d&title=&width=696)
### 3.2 具体操作
![image.png](https://cdn.nlark.com/yuque/0/2022/png/26910220/1652928143301-0063e44c-c51a-4742-b113-8df85486476a.png#clientId=u4d32acdb-ca6f-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=235&id=u00faf50a&margin=%5Bobject%20Object%5D&name=image.png&originHeight=235&originWidth=534&originalType=binary&ratio=1&rotation=0&showTitle=false&size=8003&status=done&style=none&taskId=uc3626a2e-0d18-4636-a85e-902f18561c6&title=&width=534)

- 绘制拓扑图，如上图所示
- 配置四个PC的ip，对应的ip如下所示

![image.png](https://cdn.nlark.com/yuque/0/2022/png/26910220/1652928206283-7dda0a09-37a6-4a03-9b4b-aeaa9c3c2e3b.png#clientId=u4d32acdb-ca6f-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=266&id=u187618de&margin=%5Bobject%20Object%5D&name=image.png&originHeight=266&originWidth=707&originalType=binary&ratio=1&rotation=0&showTitle=false&size=73239&status=done&style=none&taskId=ue4758402-6406-44f9-ae78-76b42305164&title=&width=707)

- 交换机划分vlan，具体方法参考**1.单交换机划分vlan**
```bash
# 还需要给0/24配置trunk模式
Switch(config)#int fa 0/24
Switch(config-if)#switc.hport mode trunk
Switch(config-if)#no shutdown
```



- 单臂路由配置router
```bash
Router0(config)#interface fastEthernet 0/0    				//进入Fa 0/0口
Router0(config-if)#no ip address 							//删除以前的IP
Router0(config-if)#no shutdown 							//接口重启生效
Router0(config-if)#exit
Router0(config-if)#interface fastEthernet 0/0.10				//进入Fa 0/0.10子接口
Router0(config-subif)#encapsulation dot1q 10				//封装802.1q的Vlan协议
Router0(config-subif)#ip address 192.168.10.1 255.255.255.0	//设置子接口IP与掩码
Router0(config-subif)#exit
Router0(config-if)#interface fastEthernet 0/0.20					//进入Fa 0/0.20子接口
Router0(config-subif)#encapsulation dot1q 20
Router0(config-subif)#ip address 192.168.20.1 255.255.255.0
Router0(config-subif)#exit
Router0#show ip route															//查看当前路由配置
```

- ping测试

PC0可以ping通同一VLAN下的PC1，也可以ping通不同VLAN下的PC2,PC3（通过route）

> ps:PC0第一次ping PC2比较慢的原因是因为PC0将数据包发送至交换机的时候，交换机还没有建立起对应的路由连接，因此交换机现在内部广播询问trunk路和对应的vlan10路是否有相应的ip时，trunk路连接的路由器将其信息发送给交换机，交换机建立起对应的路由表。


## 4. 双臂路由
需求：使用双臂路由ping通不同vlan下的PC

### 4.1 前述知识
> 双臂路由划分了两个VLAN，那么两个不同的VLAN为什么可以ping通呢？

实际上，举一个例子，在路由器配置好之后，VLAN10传进来的数据报A中的**关于VLAN10的tag会被去掉**，此时数据报A在路由器内不属于任何VLAN，因此该数据报会在路由器内直接进行数据转发。

下图展示了数据在PC1pingPC2时的流转过程，其中方框内的内容为数据报，tag10表示带有VLAN10tag的数据。
![image.png](https://cdn.nlark.com/yuque/0/2022/png/26910220/1654003349551-f397e908-2210-4b2f-bb28-c3b6d424b5ea.png#clientId=u983d84f7-9cdb-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=938&id=u7b61a95c&margin=%5Bobject%20Object%5D&name=image.png&originHeight=938&originWidth=1655&originalType=binary&ratio=1&rotation=0&showTitle=false&size=385008&status=done&style=none&taskId=uf723f425-e6e0-4421-b2ef-df1068e3770&title=&width=1655)

> 单臂路由和双臂路由的差别：单臂路由和双臂路由的差别就只在交换机和路由器的连接处，单臂路由只是简单的进行了连线，但是双臂路由对连接到交换机的两条线进行了VLAN的划分，这个时候路由器不用配置801.1q协议，只要配置好IP地址，就可以作为一个VLAN的网关进行通信了！

![image.png](https://cdn.nlark.com/yuque/0/2022/png/26910220/1652928853106-3b04456b-aab9-477d-8be0-114fe41f7017.png#clientId=u4d32acdb-ca6f-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=458&id=u7692ecae&margin=%5Bobject%20Object%5D&name=image.png&originHeight=458&originWidth=780&originalType=binary&ratio=1&rotation=0&showTitle=false&size=101576&status=done&style=none&taskId=u940e3df7-1f44-4f25-a5bf-191b94b4bf5&title=&width=780)
### 4.2 具体操作
![image.png](https://cdn.nlark.com/yuque/0/2022/png/26910220/1652928143301-0063e44c-c51a-4742-b113-8df85486476a.png#clientId=u4d32acdb-ca6f-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=235&id=du5PX&margin=%5Bobject%20Object%5D&name=image.png&originHeight=235&originWidth=534&originalType=binary&ratio=1&rotation=0&showTitle=false&size=8003&status=done&style=none&taskId=uc3626a2e-0d18-4636-a85e-902f18561c6&title=&width=534)

- 绘制拓扑图，如上图所示
- IP配置如下所示

![image.png](https://cdn.nlark.com/yuque/0/2022/png/26910220/1652930332687-353f6151-af6b-44e2-9bf8-336d75bc38a6.png#clientId=u4d32acdb-ca6f-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=315&id=ua2de7819&margin=%5Bobject%20Object%5D&name=image.png&originHeight=315&originWidth=740&originalType=binary&ratio=1&rotation=0&showTitle=false&size=95172&status=done&style=none&taskId=u9fabe3b0-476a-44fe-b81a-f6a95b44564&title=&width=740)

- 配置switch的VLAN划分，需要注意的是，Fa0/23和Fa0/24也需要划分vlan
```bash
Switch>en
Switch#conf t
# 划分vlan
Switch(config)#vlan 10
Switch(config-vlan)#exit
Switch(config)#vlan 20
Switch(config-vlan)#exit
Switch(config)#int fa 0/1
Switch(config-if)#switchport mode access 
Switch(config-if)#switchport access vlan 10
Switch(config-if)#exit
Switch(config)#int fa 0/2
Switch(config-if)#switchport mode access 
Switch(config-if)#switchport  access vlan 10
Switch(config-if)#exit
Switch(config)#int fa 0/11
Switch(config-if)#switchport mode access 
Switch(config-if)#switchport access vlan 20
Switch(config-if)#exit
Switch(config)#int fa 0/12
Switch(config-if)#switchport mode access 
Switch(config-if)#switchport  access vlan 20
Switch(config-if)#exit
Switch(config)#int fa 0/23
Switch(config-if)#switchport mode access 
Switch(config-if)#switchport  access vlan 10
Switch(config-if)#exit
Switch(config)#int fa 0/24
Switch(config-if)#switchport mode access 
Switch(config-if)#switchport  access vlan 20
Switch(config-if)#exit

```

- 配置路由器
```bash
Router0(config)#interface fastEthernet 0/0
Router0(config-if)#ip address 192.168.10.1 255.255.255.0
Router0(config-if)#no shutdown
Router0(config)#interface fastEthernet 0/1
Router0(config-if)#ip address 192.168.20.1 255.255.255.0
Router0(config-if)#no shutdown

```

- ping测试，PC0可以ping通所有PC



## 5.三层交换机实现VLAN间路由
需求：实现和双臂路由相同的功能，跨vlan之间的PC可以相互ping通
![image.png](https://cdn.nlark.com/yuque/0/2022/png/26910220/1652943341550-c2012539-edfa-429a-bc36-e3e9dfcadc9f.png#clientId=u4d32acdb-ca6f-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=453&id=ua04688bb&margin=%5Bobject%20Object%5D&name=image.png&originHeight=453&originWidth=803&originalType=binary&ratio=1&rotation=0&showTitle=false&size=110764&status=done&style=none&taskId=u14fade42-4dcf-40ef-b2dd-41a5fb29b63&title=&width=803)


![image.png](https://cdn.nlark.com/yuque/0/2022/png/26910220/1652931182756-42c0a85f-9f7a-48f8-9893-a259613a581c.png#clientId=u4d32acdb-ca6f-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=319&id=u515bcbe3&margin=%5Bobject%20Object%5D&name=image.png&originHeight=319&originWidth=732&originalType=binary&ratio=1&rotation=0&showTitle=false&size=94240&status=done&style=none&taskId=uf8e12fd2-6f7e-4526-afe3-562fee091e5&title=&width=732) 
### 5.2 具体操作

- 配置三层交换机
```bash
Switch(config)#ip routing 
Switch(config)#interface fastEthernet 0/1 
Switch(config-if)#switchport mode access 
Switch(config-if)#switchport access vlan 10 
Switch(config)#interface vlan 10 
Switch(config-if)#ip add 192.168.10.1 255.255.255.0 
Switch3(config-if)#no shutdown 
Switch(config)#interface vlan 20 
Switch(config-if)#ip add 192.168.20.1 255.255.255.0 
Switch3(config-if)#no shutdown
```

## 6. 静态路由
需求：任意两个PC之间可以相互ping通
![image.png](https://cdn.nlark.com/yuque/0/2022/png/26910220/1654066867626-5c870ad2-4b52-44e9-a972-c6ada81ac441.png#clientId=u983d84f7-9cdb-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=312&id=u465c2aa9&margin=%5Bobject%20Object%5D&name=image.png&originHeight=390&originWidth=611&originalType=binary&ratio=1&rotation=0&showTitle=false&size=19003&status=done&style=none&taskId=u68877f65-d6fe-409a-ac15-0c9eccf624c&title=&width=488.8)
![image.png](https://cdn.nlark.com/yuque/0/2022/png/26910220/1654066903412-736a7a38-470c-403b-82e8-71b78bbe723f.png#clientId=u983d84f7-9cdb-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=154&id=u522d27b7&margin=%5Bobject%20Object%5D&name=image.png&originHeight=193&originWidth=534&originalType=binary&ratio=1&rotation=0&showTitle=false&size=33157&status=done&style=none&taskId=u14ff1a62-06f9-4dd8-950e-8e276c4bc96&title=&width=427.2)
### 6.2 具体操作


> 该实验中交换机什么都不需要配置


- route0配置
```shell
// 关闭域名解释
Router(config)#no ip domain-look
Router(config)#int fa0/0
Router(config-if)#ip address 192.168.1.1 255.255.255.0
Router(config-if)#no shutdown
Router(config-if)#exit
Router(config)#int fa0/1
Router(config-if)#ip address 172.1.1.1 255.255.255.0
Router(config-if)#no shutdown 

// 配置静态路由
Router(config)#ip route  172.2.2.0 255.255.255.0 192.168.1.2
Router(config)#end

```

- route1配置
```shell
// 关闭域名解释
Router(config)#no ip domain-look
Router(config-if)#ip address 172.2.2.1 255.255.255.0
Router(config-if)#no shutdown
Router(config)#int fa0/1
Router(config-if)#ip address 192.168.1.2 255.255.255.0
Router(config-if)#no shutdown 

// 配置静态路由
Router(config)#ip route  172.1.1.0 255.255.255.0 192.168.1.1
Router(config)#end

```

## 7. 动态路由——RIP协议
需求：不同的PC之间可以相互ping通，拓扑结构配置和6.静态路由一致

![image.png](https://cdn.nlark.com/yuque/0/2022/png/26910220/1654067219656-df50135f-e118-4139-ac0e-d74812059fd5.png#clientId=u983d84f7-9cdb-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=307&id=uc58a3849&margin=%5Bobject%20Object%5D&name=image.png&originHeight=384&originWidth=613&originalType=binary&ratio=1&rotation=0&showTitle=false&size=18973&status=done&style=none&taskId=u5a154468-eef4-47fa-a3bf-66678e3b138&title=&width=490.4)
### ![image.png](https://cdn.nlark.com/yuque/0/2022/png/26910220/1654079411884-efefd718-b98a-4797-bc41-ed6fa0e2b794.png#clientId=ucc7c1e0e-ae99-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=183&id=u60a2e04f&margin=%5Bobject%20Object%5D&name=image.png&originHeight=229&originWidth=847&originalType=binary&ratio=1&rotation=0&showTitle=false&size=7157&status=done&style=none&taskId=ue980593f-1677-42d5-83ef-0e3b6a9bdd8&title=&width=677.6)
### 7.2 具体操作

- 拓扑图如上所示
- IP配置如下所示

![image.png](https://cdn.nlark.com/yuque/0/2022/png/26910220/1654079454498-f2e34206-c734-4545-a4a7-aeef2b186151.png#clientId=ucc7c1e0e-ae99-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=162&id=uc6d2f6eb&margin=%5Bobject%20Object%5D&name=image.png&originHeight=203&originWidth=550&originalType=binary&ratio=1&rotation=0&showTitle=false&size=33260&status=done&style=none&taskId=uad01c266-3478-4cf8-b916-d7050346288&title=&width=440)

- route0配置
```shell
// 关闭域名解释
Router(config)#no ip domain-look
Router(config)#int fa0/0
Router(config-if)#ip address 192.168.1.1 255.255.255.0
Router(config-if)#no shutdown
Router(config-if)#exit
Router(config)#int fa0/1
Router(config-if)#ip address 172.1.1.1 255.255.255.0
Router(config-if)#no shutdown 

// 配置RIP协议
Router(config)#router rip
Router(config-router)#version 2
Router(config-router)#network 172.1.1.0
Router(config-router)#network 192.168.1.0
Router(config-router)#end

```

- route1配置
```shell
// 关闭域名解释
Router(config)#no ip domain-look
Router(config)#int fa0/0
Router(config-if)#ip address 172.2.2.1 255.255.255.0
Router(config-if)#no shutdown
Router(config)#int fa0/1
Router(config-if)#ip address 192.168.1.2 255.255.255.0
Router(config-if)#no shutdown 

// 配置RIP协议
Router(config)#router rip
Router(config-router)#version 2
Router(config-router)#network 172.2.2.0
Router(config-router)#network 192.168.1.0
Router(config-router)#end

```
## 
