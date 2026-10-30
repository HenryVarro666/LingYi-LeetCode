def _d(x):
    return f'{x:04d}' if isinstance(x, int) else '?'


def _wheel(S):
    if 'now' not in S or 'base' not in S:
        return None
    return list(_d(S['now']))


def _pos(S):
    b = S.get('base')
    return {1: 3, 10: 2, 100: 1, 1000: 0}.get(b)


def _used_cap(var):
    def f(S, B, r):
        v = getattr(S, var)
        if _d(v) in S.deadends:
            return f'`{_d(v)}` 是==死亡数字== → 不能入队'
        if B.used[v]:
            return f'`{_d(v)}` 之前已经出现过 → 跳过'
        return f'`{_d(v)}` 没出现过，标记并加入队列'
    return f


def _tgt(var):
    def f(S, B, r):
        v = getattr(S, var)
        if v == int(S.target):
            return f'`{_d(v)}` == 目标 `{S.target}` → 找到了！'
        return f'`{_d(v)}` 不是目标'
    return f


CONFIG = dict(
    num=752, title='打开转盘锁', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='BFS（数字编码 + 数组队列）',
    tags=['labuladong', '灵神题单·图论算法'],
    setup='',
    code='''
class Solution(object):
    def openLock(self, deadends, target):

        if target == '0000':
            return 0
        

        used = [False] * 10000
        for num in deadends:
            used[int(num)] = True
        
        if used[0]:
            return -1

        q = [0]
        l = 0
        r = 1
        step = 0
        while l < r:
            step += 1
            for now in q[l:r]:
                base = 1
                for index in range(4):
                    mod = now // base % 10
                    if mod == 0:
                        prev = now + base * 9
                    else:
                        prev = now - base
                    if prev == int(target):
                        return step
                    if not used[prev]:
                        used[prev] = True
                        q.append(prev)

                    if mod == 9:
                        next = now - base * 9
                    else:
                        next = now + base
                    if next == int(target):
                        return step
                    if not used[next]:
                        used[next] = True
                        q.append(next)

                    base *= 10
            
            l = r
            r = len(q)
        
        return -1
''',
    call="Solution().openLock(['0010'], '0008')",
    expect=2,
    skip=['l = 0', 'r = 1', 'for index in range', 'if mod == 0', 'if mod == 9', 'used[prev] = True', 'q.append(',
          'used[next] = True', 'for num in deadends', 'used[int(num)]'],
    views=[
        dict(type='text', fn=lambda S: (f"死亡数字 `{S['deadends']}`，目标 `{S['target']}`" if 'deadends' in S else ''),
             size=28, h=60),
        dict(type='string', var=_wheel, label='当前出队的密码 now（黄 = 正在转的那一位，base = 10 的几次方）', cell=100, h=160,
             color=lambda S, i, v: 'yellow' if i == _pos(S) else None, index=False),
        dict(type='text', fn=lambda S: (f"往下转 `prev = {_d(S['prev'])}`" if 'prev' in S and S.get('prev') is not None else '')
             + (f"　　往上转 `next = {_d(S['next'])}`" if isinstance(S.get('next'), int) else ''), size=28, h=60),
        dict(type='array', var=lambda S: [_d(x) for x in S['q']] if 'q' in S else None,
             label='q（暗 = 之前的轮次，[l, r) = 当前这一轮）', cell=86, h=190,
             pointers={'l': 'blue', 'r': 'pink'}, dim=lambda S, i, v: i < S.get('l', 0)),
    ],
    watch=[('step', 'step', 'green'), ('now', lambda S: _d(S['now']) if 'now' in S else None, 'blue'),
           ('base', 'base', 'yellow'), ('mod', 'mod')],
    captions={
        "if target == '0000'": '目标不是 `0000`，需要转',
        'used = [False] * 10000': '把密码看成 ==0~9999 的整数==，`used` 同时记录死亡数字和访问过的状态',
        'if used[0]': '起点 `0000` 不是死亡数字，可以开始',
        'q = [0]': '从 `0000` 开始 BFS，`q[l:r]` 是当前这一轮',
        'step = 0': '`step` = 转动次数（BFS 轮次）',
        'while l < r': lambda S, B, r: (f'`l = {S.l} < r = {S.r}`：还有状态，继续' if S.l < S.r else '队列空了'),
        'step += 1': '第 =={step}== 轮：这一轮新得到的数字都要转 {step} 次',
        'for now in q[l:r]': lambda S, B, r: (f'取出 `{_d(S.now)}`，依次转个位、十位、百位、千位' if 'base' not in B or B.now != S.now else '这一轮的状态都处理完了'),
        'base = 1': '`base = 1` 对应个位',
        'mod = now // base % 10': lambda S, B, r: f'`{S.now} // {S.base} % 10 = {S.mod}`：取出这一位的数字',
        'prev = now + base * 9': lambda S, B, r: f'这一位是 0，往下转变成 9：`{S.now} + {S.base}×9` → `{_d(S.prev)}`',
        'prev = now - base': lambda S, B, r: f'这一位往下转 1：`{S.now} − {S.base}` → `{_d(S.prev)}`',
        'if prev == int(target)': _tgt('prev'),
        'if not used[prev]': _used_cap('prev'),
        'next = now - base * 9': lambda S, B, r: f'这一位是 9，往上转变成 0：`{S.now} − {S.base}×9` → `{_d(S.next)}`',
        'next = now + base': lambda S, B, r: f'这一位往上转 1：`{S.now} + {S.base}` → `{_d(S.next)}`',
        'if next == int(target)': _tgt('next'),
        'if not used[next]': _used_cap('next'),
        'base *= 10': '`base` → {base}：去转下一位',
        'return step': '第 {step} 轮转到目标 → 最少转 =={step}== 次',
        'l = r': '这一轮结束：`l` → {l}',
        'r = len(q)': '`r` → {r}：新加入的就是下一轮',
    },
    cards=dict(
        one_liner='把密码当成 0~9999 的整数，从 0000 一轮轮 BFS',
        complexity='时间 `O(10^4 × 8)`，空间 `O(10^4)`',
        problem=['4 位转盘锁初始 `0000`，每次把某一位往上或往下转 1（9 和 0 相邻）',
                 '转到 `deadends` 里的数字就锁死，求转到 `target` 的最少次数，不行返回 -1',
                 '本视频：`deadends = ["0010"]`，`target = "0008"` → `2`'],
        quote='我们的目标就是从0000开始进行bfs，每次可以选择其中的一位进行旋转。若新得到的数字==没有被使用过，且不是死亡数字==，那么就将其加入到bfs队列中。',
        quote_src='—— yiduobo 题解原文',
        idea=['状态 = 整数，`now // base % 10` 取出某一位',
              '死亡数字==预先标成 used==，和访问过的状态一起拦截',
              '转到目标时，当前轮次 `step` 就是答案'],
        summary=['时间 `O(10^4 × 8)`：每个状态最多入队一次，每次 8 个邻居',
                 '易错：`0000` 本身是死亡数字要直接返回 -1；目标是 `0000` 返回 0',
                 '易错：0 往下转是 9、9 往上转是 0，要单独处理',
                 '原文为 Python 2 写法，整数除法 `now / base` 已改为 `now // base`'],
    ),
)
