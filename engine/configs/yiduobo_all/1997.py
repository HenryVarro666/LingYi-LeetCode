def _fm(S):
    if 'index' not in S or 'f' not in S or len(S['f']) < 3:
        return '`f[i]` = 访问到第 `i` 个房间所需的步数（天数 + 1），`f = [1, 3]` 是手算出的头两项'
    k = S['index'] - 1
    j = S['nextVisit'][k]
    f = S['f']
    return f'`f[{S["index"]}] = 2×f[{k}] − f[{j}] + 2` = 2×{f[k]} − {f[j]} + 2 = =={2 * f[k] - f[j] + 2}=='


CONFIG = dict(
    num=1997, title='访问完所有房间的第一天', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='打表找规律 + 递推',
    tags=['灵神题单·动态规划', '难度分 2260'],
    code='''
class Solution(object):
    def firstDayBeenInAllRooms(self, nextVisit):

        f = [1, 3]
        n = len(nextVisit)
        mod = 10 ** 9 + 7
        for index in range(2, n):
            f.append((f[index - 1] + f[index - 1] - f[nextVisit[index - 1]] + 2) % mod)
        
        res = f[-1] - 1
        if res < 0:
            res += mod
        return res
''',
    call='Solution().firstDayBeenInAllRooms([0,0,1,2,1])',
    expect=20,
    skip=['for index in range'],
    views=[
        dict(type='text', h=70, size=24, fn=_fm),
        dict(type='array', var='nextVisit', label='nextVisit（蓝 = 刚到的房间，粉 = 被送回的房间）', h=250, cell=100,
             pointers={'index - 1': 'blue', 'nextVisit[index - 1]': 'pink'},
             pointer_labels={'index - 1': 'i-1', 'nextVisit[index - 1]': '送回'}),
        dict(type='array', var='f', label='f[i]：到达第 i 个房间所需步数', h=250, cell=100,
             pointers={'index': 'green', 'nextVisit[index - 1]': 'pink'},
             pointer_labels={'nextVisit[index - 1]': '减去'},
             color=lambda S, i, v: 'green' if i == len(S['f']) - 1 and len(S['f']) > 2 else None),
    ],
    watch=[('index', 'index', 'blue'), ('f', 'f', 'green'), ('res', 'res', 'orange')],
    captions={
        'f = [1, 3]': '头两项靠手算：到 0 号房要 1 步，到 1 号房要 3 步（`f[0] = 1`，`f[1] = 3`）',
        'n = len': '`n = {n}` 个房间',
        'mod = ': '答案要取模',
        'f.append': '`f[{index}] = 2×f[{index - 1}] − f[{nextVisit[index - 1]}] + 2` = =={f[-1]}==：走到 {index - 1} 号房、被送回 {nextVisit[index - 1]} 号房、重走回来，+2 是两次到访',
        'res = f[-1] - 1': '`f` 数的是步数（含起点），日期编号要减 1：`res = {f[-1]} − 1` = =={res}==',
        'if res < 0': '`res < 0` 吗？{res < 0}（取模后 `f[-1]` 可能为 0）',
        'res += mod': '加回 `mod`',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='打表观察：被送回后重走一遍，递推出到每个房间的步数',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['访问次数为奇数 → 次日去 `nextVisit[i]`，偶数 → 去 `i+1`',
                 '求第一次访问完所有房间的日期编号，对 `10^9+7` 取模',
                 '示例：`[0,0,2]` → `6`；本视频：`[0,0,1,2,1]` → `20`'],
        quote='直接推导规律比较复杂，数组下标倒来倒去的太麻烦了，不妨直接把较小的情况打印出来看看。',
        quote_src='—— yiduobo 题解原文',
        idea=['`nextVisit[0]` 必为 0，序列总以 `[0, 0]` 开头；观察 `[0,0,1,1,2]` 与 `[0,0,2]` 的差别',
              '`f[i]` 为到第 `i` 个房间的步数：`f[i] = f[i-1] + f[i-1] − f[nextVisit[i-1]] + 2`',
              '作者先打表验证猜想，再写成递推'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '最后一个房间的 `nextVisit` 没有意义，递推到 `n-1` 为止',
                 '`f` 数的是「步数」，日期编号要 `− 1`',
                 '取模后相减可能为负，所以 `res < 0` 时要加回 `mod`',
                 '原文已是 Python 3 可运行的写法，未做修改'],
    ),
)
