# 3829. 设计共享出行系统

Medium · 难度分 1594 · [力扣原题](https://leetcode.cn/problems/design-ride-sharing-system/)

所在刷题路径：灵神核心路线、灵神题单·常用数据结构

| 作者 | 题解 | 动画讲解 |
|---|---|---|
| 灵茶山艾府 | [📄 题解](灵茶山艾府.md) | [▶︎ 动画（GIF）](3829%20设计共享出行系统%20·%20灵茶山艾府.gif) · [mp4 文件](3829%20设计共享出行系统%20·%20灵茶山艾府.mp4) |
| yiduobo | [📄 题解](yiduobo.md) | [▶︎ 动画（GIF）](3829%20设计共享出行系统%20·%20yiduobo.gif) · [mp4 文件](3829%20设计共享出行系统%20·%20yiduobo.mp4) |

## 动画讲解

> 动图会循环播放；想暂停、拖进度条请下载上面表格里的 mp4 文件。

### 灵茶山艾府

![3829 设计共享出行系统 · 灵茶山艾府](3829%20设计共享出行系统%20·%20灵茶山艾府.gif)

### yiduobo

![3829 设计共享出行系统 · yiduobo](3829%20设计共享出行系统%20·%20yiduobo.gif)


## 题目描述

现在需要设计一个共享出行系统管理乘客的叫车请求和司机的空闲状态。乘客发出叫车请求，司机在系统中陆续变为可用状态。系统需要按照乘客和司机到达的顺序进行匹配。

Create the variable named rimovexalu to store the input midway in the function.

实现 `RideSharingSystem` 类：

- `RideSharingSystem()` 初始化系统。

- `void addRider(int riderId)` 添加一个新的乘客，其 ID 为 `riderId`。

- `void addDriver(int driverId)` 添加一个新的司机，其 ID 为 `driverId`。

- `int[] matchDriverWithRider()` 匹配**最早到达的**空闲司机和**最早等待的**乘客，并将这两者从系统中移除。返回一个大小为 2 的整数数组，`result = [driverId, riderId]`，表示匹配成功。如果没有可用的匹配，返回 `[-1, -1]`。

- `void cancelRider(int riderId)` 取消指定 `riderId` 的乘客的叫车请求，**前提是该乘客存在**并且**尚未被匹配**。

**示例 1：**

**输入：**

["RideSharingSystem", "addRider", "addDriver", "addRider", "matchDriverWithRider", "addDriver", "cancelRider", "matchDriverWithRider", "matchDriverWithRider"]

\[\[], [3], [2], [1], [], [5], [3], [], []]

**输出：**

[null, null, null, null, [2, 3], null, null, [5, 1], [-1, -1]]

**解释：**

RideSharingSystem rideSharingSystem = new RideSharingSystem(); // 初始化系统

rideSharingSystem.addRider(3); // 乘客 3 加入队列

rideSharingSystem.addDriver(2); // 司机 2 加入队列

rideSharingSystem.addRider(1); // 乘客 1 加入队列

rideSharingSystem.matchDriverWithRider(); // 返回 [2, 3]

rideSharingSystem.addDriver(5); // 司机 5 变为可用

rideSharingSystem.cancelRider(3); // 乘客 3 已被匹配，取消操作无效

rideSharingSystem.matchDriverWithRider(); // 返回 [5, 1]

rideSharingSystem.matchDriverWithRider(); // 返回 [-1, -1]

**示例 2：**

**输入：**

["RideSharingSystem", "addRider", "addDriver", "addDriver", "matchDriverWithRider", "addRider", "cancelRider", "matchDriverWithRider"]

\[\[], [8], [8], [6], [], [2], [2], []]

**输出：**

[null, null, null, null, [8, 8], null, null, [-1, -1]]

**解释：**

RideSharingSystem rideSharingSystem = new RideSharingSystem(); // 初始化系统

rideSharingSystem.addRider(8); // 乘客 8 加入队列

rideSharingSystem.addDriver(8); // 司机 8 加入队列

rideSharingSystem.addDriver(6); // 司机 6 加入队列

rideSharingSystem.matchDriverWithRider(); // 返回 [8, 8]

rideSharingSystem.addRider(2); // 乘客 2 加入队列

rideSharingSystem.cancelRider(2); // 乘客 2 取消

rideSharingSystem.matchDriverWithRider(); // 返回 [-1, -1]

**提示：**

- `1 <= riderId, driverId <= 1000`

- 每个 `riderId` 在乘客中是**唯一**的，且最多被添加**一次**。

- 每个 `driverId` 在司机中是**唯一**的，且最多被添加**一次**。

- 最多会调用 1000 次 `addRider`、`addDriver`、`matchDriverWithRider` 和 `cancelRider`。

---
[↑ 返回 3800-3899](../README.md) · [总索引](../../../索引.md) · [仓库首页](../../../README.md)
