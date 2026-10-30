CONFIG = dict(
    num=2211, title='统计道路上的碰撞次数', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='双指针找边界 · 再数非静止',
    tags=['灵神题单', '贪心与思维', '难度分 1581'],
    code='''
class Solution(object):
    def countCollisions(self, directions):

        n = len(directions)
        l = 0
        while l < n and directions[l] == 'L':
            l += 1
        
        if l == n:
            return 0
        
        r = n - 1
        while r >= 0 and directions[r] == 'R':
            r -= 1
        
        if r == -1:
            return 0
        
        res = r - l + 1
        for d in directions[l : r + 1]:
            if d == 'S':
                res -= 1
        
        return res
''',
    call='Solution().countCollisions("LLRSRLRR")',
    expect=3,
    views=[
        dict(type='string', var='directions', label='directions（蓝 = 向右，粉 = 向左，黄 = 静止）', cell=84,
             pointers={'l': 'blue', 'r': 'pink'},
             window=('l', 'r'),
             color=lambda S, i, v: 'yellow' if v == 'S' else ('blue' if v == 'R' else 'pink'),
             dim=lambda S, i, v: ('res' in S and (i < S['l'] or i > S['r']))),
        dict(type='text', size=28, fn=lambda S: (f"`res = {S['res']}`：[l, r] 内的车数，遇到静止的减 1" if 'res' in S else '')),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('res', 'res', 'green'), ('d', 'd', 'yellow')],
    captions={
        'n = len': '共 `n = {n}` 辆车',
        'l = 0': '`l` 从左往右，跳过开头向左的车',
        'while l < n': lambda S, B, r: (f"`directions[{S.l}] = 'L'` → 向左开出去，不会碰撞，`l` 右移" if S.l < S.n and S.directions[S.l] == 'L'
                                        else f"`directions[{S.l}] = '{S.directions[S.l]}'` 不是 L → 左边界停在 `l = {S.l}`"),
        'l += 1': '`l` → {l}',
        'if l == n': '`l = {l}`，不等于 `n = {n}`，不是全向左',
        'r = n - 1': '`r` 从右往左，跳过结尾向右的车',
        'while r >= 0': lambda S, B, rt: (f"`directions[{S.r}] = 'R'` → 向右开出去，不会碰撞，`r` 左移" if S.r >= 0 and S.directions[S.r] == 'R'
                                          else f"`directions[{S.r}] = '{S.directions[S.r]}'` 不是 R → 右边界停在 `r = {S.r}`"),
        'r -= 1': '`r` → {r}',
        'if r == -1': '`r = {r}`，不是全向右',
        'res = r - l + 1': '区间 `[{l}, {r}]` 内共 `res = =={res}==` 辆车，每辆都会碰撞或静止',
        'for d in': '遍历区间内的车 `d = {d}`',
        'if d ==': lambda S, B, r: (f"`d = 'S'` → 静止的车不算碰撞" if S.d == 'S' else f"`d = '{S.d}'` → 在移动，会撞上别的车，保留"),
        'res -= 1': '去掉静止的车，`res` → =={res}==',
        'return res': '剩下每辆移动的车贡献一次碰撞 → ==`{res}`==',
    },
    cards=dict(
        one_liner='两侧向外开的车不碰撞，中间去掉静止的就是答案',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['公路上有 `n` 辆车，方向为 `L` 向左、`R` 向右、`S` 静止',
                 '相向相撞 +2，移动车撞静止车 +1，撞后停下；求碰撞总次数',
                 '本视频：`"LLRSRLRR"` → `3`'],
        quote='在去除掉两侧向外开的车辆后，再去掉静止的车辆后，剩余所有的车辆都将贡献一次碰撞，也就是最终答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['因为有静止的车，只有==两侧向外开==的车不会碰撞',
              '用 `l`、`r` 两个指针找出第一辆非 L、最后一辆非 R 的车',
              '区间内车数 `r-l+1`，减去静止的，就是还在动、会撞车的数量'],
        summary=['时间 `O(n)`，空间 `O(1)`（切片遍历会临时复制）',
                 '`l == n` 或 `r == -1` 要提前返回 0，对应全 L / 全 R',
                 '原文为 Python 2 风格，代码未改',
                 '对比灵神：灵神用 `lstrip/rstrip` 一行去首尾，yiduobo 手写双指针'],
    ),
)
