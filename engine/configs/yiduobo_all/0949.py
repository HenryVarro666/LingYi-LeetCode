def _res(S):
    best = S.get('self.res', '')
    if 'now' not in S:
        return ''
    cur = ''.join(str(x) for x in S['now'])
    return f"当前排列 `{cur or '（空）'}`　　最大合法时间 ==res== = `{best or '无'}`"


def _used(S, i, v):
    u = S.get('used')
    if u is None:
        return None
    return 'green' if u[i] else None


def _fill(S, i, v):
    now = S.get('now')
    if now is None:
        return None
    return 'blue' if i < len(now) else None


def _check(S, B, ret):
    now = S.now
    if now[0] > 2:
        return f'小时十位 `{now[0]} > 2`：不可能是合法小时 → 丢弃'
    if now[0] == 2 and now[1] > 3:
        return f'小时 `2{now[1]}` 超过 23 → 丢弃'
    if now[2] > 5:
        return f'分钟十位 `{now[2]} > 5`：超过 59 → 丢弃'
    return f'`{now[0]}{now[1]}:{now[2]}{now[3]}` 是合法时间'


CONFIG = dict(
    num=949, title='给定数字能组成的最大时间', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='DFS 枚举全排列 + 校验',
    code='''
class Solution(object):
    def largestTimeFromDigits(self, arr):

        self.res = ""
        self.minute = None
        used = [False] * 4
        self.dfs(arr, used, [])

        return self.res
    
    def dfs(self, arr, used, now):
        if len(now) == 4:
            if now[0] > 2:
                return
            if now[0] == 2 and now[1] > 3:
                return
            if now[2] > 5:
                return

            minute = (now[0] * 10 + now[1]) * 60 + now[2] * 10 + now[3]
            if self.minute is None or minute > self.minute:
                self.minute = minute
                self.res = str(now[0]) + str(now[1]) + ':' + str(now[2]) + str(now[3])
            
            return
        
        for index in range(4):
            if not used[index]:
                now.append(arr[index])
                used[index] = True
                self.dfs(arr, used, now)
                used[index] = False
                now.pop()
''',
    call='Solution().largestTimeFromDigits([1, 2, 3, 4])',
    expect='23:41',
    views=[
        dict(type='text', fn=_res),
        dict(type='array', var='arr', label='arr（绿 = 已用）', cell=70, h=150, color=_used),
        dict(type='array', var='now', label='now（当前排列）', cell=70, h=150, color=_fill),
        dict(type='calls', h=210, hide=('arr', 'used', 'now')),
    ],
    watch=[('self.minute', 'self.minute', 'cyan'), ('self.res', 'self.res', 'green')],
    skip=['used = [False]', 'self.res = ""', 'self.minute = None', 'return self.res'],
    captions={
        'self.dfs(arr, used, [])': '只有 4 个数字，至多 `4! = 24` 种排列 → ==DFS 枚举每种排列==',
        'if len(now) == 4': lambda S, B, r: ('`now` 已有 4 个数字：排好了一个完整排列，去校验' if len(S.now) == 4
                                              else f'`now` 只有 {len(S.now)} 个数字，继续往后填'),
        'if now[0] > 2': lambda S, B, r: (f'小时十位 `{S.now[0]}` > 2 → ==非法=={"，丢弃" if S.now[0] > 2 else ""}' if S.now[0] > 2 else f'小时十位 `{S.now[0]}` ≤ 2，没问题'),
        'if now[0] == 2 and now[1] > 3': lambda S, B, r: (f'`{S.now[0]}{S.now[1]}` 超过 23 → ==非法==，丢弃' if S.now[0] == 2 and S.now[1] > 3 else f'小时 `{S.now[0]}{S.now[1]}` 没超过 23'),
        'if now[2] > 5': lambda S, B, r: (f'分钟十位 `{S.now[2]}` > 5 → ==非法==，丢弃' if S.now[2] > 5 else f'分钟十位 `{S.now[2]}` ≤ 5，合法'),
        'minute = (': '换算成分钟数：`({now[0]}×10+{now[1]})×60 + {now[2]}×10+{now[3]}` = =={minute}==，方便比大小',
        'if self.minute is None': lambda S, B, r: (f'`{S.minute}` 比当前最大 `{S['self.minute']}` 大（或还没有答案）→ ==更新答案==' if (S['self.minute'] is None or S.minute > S['self.minute']) else f'`{S.minute}` ≤ 当前最大 `{S['self.minute']}` → 不更新'),
        'self.minute = minute': '`self.minute` → {minute}',
        'self.res = str': '`self.res` → `{self.res}`',
        'for index in range(4)': lambda S, B, r: ('4 个下标都试过了，这一层结束' if (S.index == 3 and B.get('index') == 3) else f'尝试把 `arr[{S.index}]` 放到下一位'),
        'if not used[index]': lambda S, B, r: (f'`arr[{S.index}] = {S.arr[S.index]}` 还没用过 → 可以放' if not S.used[S.index] else f'`arr[{S.index}]` 已经在 now 里了 → 跳过，==每个数字只能用一次=='),
        'now.append(arr[index])': '放入 `{arr[index]}`：`now` = {now}',
        'used[index] = True': '标记下标 `{index}` 已使用',
        'self.dfs(arr, used, now)': '递归：填下一位',
        'used[index] = False': '回溯：释放下标 `{index}`',
        'now.pop()': '回溯：把 `{B.now[-1]}` 从 now 拿出来，换下一个数字试',
        'return': '这个排列处理完（或已丢弃），回到上一层',
    },
    max_steps=90,
    cards=dict(
        one_liner='只有 4 个数字，24 种排列全部试一遍',
        complexity='时间 `O(4!)`，空间 `O(1)`',
        problem=['给 4 个数字，每个恰好用一次，组成 24 小时制的最大时间 `HH:MM`',
                 '不存在合法时间就返回空字符串',
                 '示例：`[1,2,3,4]` → `23:41`'],
        quote='由于只有4个数字，那么至多也就4！= 24种排列，于是可以直接枚举每一种可能的排列，然后判断其是否合法并更新答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['原文说可以 4 重循环，他采用的是 DFS：`now` 存当前排列，`used` 标记已用的下标',
              '排满 4 位后校验：小时不超过 23，分钟十位不超过 5',
              '把时间换算成分钟数 `minute`，比大小更方便；更新时再拼成字符串'],
        summary=['时间 `O(4!)`，空间 `O(1)`',
                 '`used` 标记的是==下标==，数字可以重复（如 `[1,1,2,3]`）',
                 '易错：`now[0] == 2` 时要再限制 `now[1] <= 3`',
                 '没有合法排列时 `self.res` 保持空串',
                 '原文是 Python 2 风格写法，但在 Python 3 下无需修改，已逐字照搬'],
    ),
)
