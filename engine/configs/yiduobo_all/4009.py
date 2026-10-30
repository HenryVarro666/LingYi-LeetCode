def _fmt(k, v):
    return f'(等{k[0]}, 余{k[1]}, 余{k[2]}) → {v}'


CONFIG = dict(
    num=4009, title='最小化最大可能等待时间', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='哈希表 DP · (wait, r0, r1) 打包为键',
    tags=['其他线性 DP', '多维 DP', '难度分 2499'],
    code='''
class Solution(object):
    def minMaxWaitingTime(self, demand, fuel):
        
        ma = max(demand)
        f = {}
        g = {}
        if demand[0] <= fuel[0]:
            f[(0, fuel[0] - demand[0], fuel[1])] = 0

        if demand[0] <= fuel[1]:
            g[(0, fuel[0], fuel[1] - demand[0])] = 0

        for index in range(1, len(demand)):
            d = demand[index]
            nxt_f = {}
            nxt_g = {}
            for pre in f:
                wait, r0, r1 = pre
                if r0 >= d:
                    nxt_wait = max(0, wait - demand[index - 1])
                    nxt_key = (nxt_wait, r0 - d, r1)
                    if nxt_key not in nxt_f or nxt_f[nxt_key] > max(f[pre], demand[index - 1]):
                        nxt_f[nxt_key] = max(f[pre], demand[index - 1])

                if r1 >= d:
                    nxt_wait = max(0, demand[index - 1] - wait)
                    nxt_key = (nxt_wait, r0, r1 - d)
                    if nxt_key not in nxt_g or nxt_g[nxt_key] > max(f[pre], wait):
                        nxt_g[nxt_key] = max(f[pre], wait)
            
            for pre in g:
                wait, r0, r1 = pre
                if r0 >= d:
                    nxt_wait = max(0, demand[index - 1] - wait)
                    nxt_key = (nxt_wait, r0 - d, r1)
                    if nxt_key not in nxt_f or nxt_f[nxt_key] > max(g[pre], wait):
                        nxt_f[nxt_key] = max(g[pre], wait)
                
                if r1 >= d:
                    nxt_wait = max(0, wait - demand[index - 1])
                    nxt_key = (nxt_wait, r0, r1 - d)
                    if nxt_key not in nxt_g or nxt_g[nxt_key] > max(g[pre], demand[index - 1]):
                        nxt_g[nxt_key] = max(g[pre], demand[index - 1])
            
            if not nxt_f and not nxt_g:
                break
            f = copy.deepcopy(nxt_f)
            g = copy.deepcopy(nxt_g)
    
        res = -1
        if f:
            res = min(f.values())
        if g:
            mi_g = min(g.values())
            if res == -1 or res > mi_g:
                res = mi_g
        
        return res
''',
    call='Solution().minMaxWaitingTime([3, 2, 4], [5, 6])',
    expect=2,
    setup='import copy',
    views=[
        dict(type='array', var='demand', label='demand（蓝 = 当前车 index）', cell=84, h=230,
             pointers={'index': 'blue'}, color=lambda S, k, v: 'blue' if k == S.get('index') else None,
             dim=lambda S, k, v: 'index' in S and k < S['index'] - 1),
        dict(type='map', var='f', label='f：上一辆在机器 0。键 (另一台等, 余0, 余1) → 最大等待', fmt=_fmt, h=150, font=26),
        dict(type='map', var='g', label='g：上一辆在机器 1（键含义同上）', fmt=_fmt, h=150, font=26),
        dict(type='map', var='nxt_f', label='nxt_f：当前车在机器 0（新一轮）', fmt=_fmt, h=130, font=26),
        dict(type='map', var='nxt_g', label='nxt_g：当前车在机器 1（新一轮）', fmt=_fmt, h=130, font=26),
    ],
    watch=[('index', 'index', 'blue'), ('d', 'd', 'yellow'), ('pre', 'pre', 'pink'), ('nxt_key', 'nxt_key', 'cyan'), ('res', 'res', 'green')],
    skip=['ma = max', 'wait, r0, r1 = pre', 'nxt_f = {}', 'nxt_g = {}', 'g = {}', 'nxt_key = (', 'if f:', 'if g:', 'mi_g = min', 'f = copy.deepcopy', 'g = copy.deepcopy', 'd = demand[index]'],
    captions={
        'f = {}': '`f` / `g`：用 ==字典== 存可达状态（不可达的不存），键是 `(wait, r0, r1)`，值是已有的最大等待',
        'if demand[0] <= fuel[0]': '车 0 能否放机器 0：`{demand[0]} <= {fuel[0]}` → {"可以" if demand[0] <= fuel[0] else "不行"}',
        'f[(0, fuel[0] - demand[0], fuel[1])] = 0': '车 0 在机器 0 加油：另一台不用等，余量 `({fuel[0]-demand[0]}, {fuel[1]})`，等待为 0',
        'if demand[0] <= fuel[1]': '车 0 能否放机器 1：`{demand[0]} <= {fuel[1]}` → {"可以" if demand[0] <= fuel[1] else "不行"}',
        'g[(0, fuel[0], fuel[1] - demand[0])] = 0': '车 0 在机器 1 加油，与 `f` 对称：余量 `({fuel[0]}, {fuel[1]-demand[0]})`',
        'for index in range': lambda S, B, r: (f'`index = {S.index}`：只依赖上一辆车的状态，==滚动==处理每辆车，当前车 `d = {S.demand[S.index]}`' if S.get('index') != B.get('index')
                                              else '所有车都处理完了'),
        'for pre in f': lambda S, B, r: (f'取出 `f` 的状态 `{S.pre}`（已有最大等待 `{S.f[S.pre]}`）：上一辆车在机器 0' if S.get('pre') != B.get('pre')
                                         else '`f` 里的状态枚举完了'),
        'for pre in g': lambda S, B, r: (f'取出 `g` 的状态 `{S.pre}`（已有最大等待 `{S.g[S.pre]}`）：上一辆车在机器 1' if S.get('pre') != B.get('pre')
                                         else '`g` 里的状态枚举完了'),
        'if r0 >= d': '机器 0 余量 `{r0}` vs 需求 `{d}`：{"够 → 当前车可上机器 0" if r0 >= d else "不够"}',
        'if r1 >= d': '机器 1 余量 `{r1}` vs 需求 `{d}`：{"够 → 当前车可上机器 1" if r1 >= d else "不够"}',
        'nxt_wait = max(0, wait - demand[index - 1])': '接着用同一台：要等上一辆加完；另一台再等 `max(0, {wait}-{demand[index-1]}) = {nxt_wait}`',
        'nxt_wait = max(0, demand[index - 1] - wait)': '换到另一台：要等 `wait = {wait}`；上一辆那台再忙 `max(0, {demand[index-1]}-{wait}) = {nxt_wait}`',
        'nxt_key = (nxt_wait, r0 - d, r1)': '新状态键 `{nxt_key}`：机器 0 用掉 `{d}`',
        'nxt_key = (nxt_wait, r0, r1 - d)': '新状态键 `{nxt_key}`：机器 1 用掉 `{d}`',
        'if nxt_key not in nxt_f': '新状态 `{nxt_key}`：是新键或旧值更大 → ==取最小==地更新',
        'if nxt_key not in nxt_g': '新状态 `{nxt_key}`：是新键或旧值更大 → ==取最小==地更新',
        'nxt_f[nxt_key] =': '`nxt_f[{nxt_key}] = {nxt_f[nxt_key]}`：到这个状态的最大等待最小为 `{nxt_f[nxt_key]}`',
        'nxt_g[nxt_key] =': '`nxt_g[{nxt_key}] = {nxt_g[nxt_key]}`：到这个状态的最大等待最小为 `{nxt_g[nxt_key]}`',
        'if not nxt_f and not nxt_g': '这辆车 ==两台机器都放不下== 吗？{"是 → 终止，答案取上一轮" if not nxt_f and not nxt_g else "否，继续下一辆车"}',
        'res = -1': '收尾：`f`、`g` 里是最后一轮的可达状态，取其中最小的最大等待',
        'res = min(f.values())': '最后一轮 `f` 中最小的最大等待：`{res}`',
        'mi_g = min': '`g` 中最小是 `{mi_g}`',
        'if res == -1 or res > mi_g': '`g` 的最小值是 `{min(g.values())}`，`f` 的是 `{res}`：{"g 更小，改用它" if res == -1 or res > min(g.values()) else "f 不大于 g，保持不变"}',
        'res = mi_g': '`g` 更优，`res = {mi_g}`',
        'return res': '车辆都被服务，最大等待最小为 ==`{res}`==',
    },
    max_steps=130,
    cards=dict(
        one_liner='只存可达状态：键 (wait, 余量0, 余量1)，一辆车一辆车往后滚',
        complexity='时间约 `O(n·可达状态数)`，空间 `O(可达状态数)`',
        problem=['`demand[i]` 是第 `i` 辆车需要的燃料，两台加油机各有初始燃料 `fuel[j]`，车按下标依次被允许加油',
                 '先==服务尽量多的车==，再让这些车中的最大等待时间最小；一辆都服务不了返回 -1',
                 '示例：`demand=[6,8,4,6,5], fuel=[16,13]` → `6`；本视频：`[3,2,4], [5,6]` → `2`'],
        quote='可达的状态应该并不多，因此在这里使用哈希表而不是数组是更好的方案，即将 (wait, r0, r1) 打包成为哈希表的 key。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f` 表示当前车在机器 0 加油，`g` 表示在机器 1 加油；`wait` 是另一台机器还要忙多久',
              '下一辆车要么接着用同一台（等 `demand[i-1]` 秒），要么换另一台（等 `wait` 秒）',
              '某一轮没有任何合法状态，说明这辆车放不下，答案取上一轮的最小值'],
        summary=['每轮只依赖上一轮，所以滚动用 `nxt_f` / `nxt_g`',
                 '易错：同台机器与换机器，等待时间和 `nxt_wait` 的算法不同',
                 '易错：若某轮 `break`，答案来自上一轮的 `f` 和 `g`',
                 '原文无 Python 2 专有写法，直接照搬；原文用到的 `copy` 在 setup 里 import',
                 '对比灵神：灵神用记忆化搜索 + 元组 `(-车数, 等待)`；yiduobo 用字典逐轮推进'],
    ),
)
