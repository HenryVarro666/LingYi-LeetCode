A = [1, 2, 3, 7, -4, 5]


def _fcol(S, k, v):
    if 'index' not in S:
        return None
    if k == S['index'] and len(S['f']) == S['index'] + 1:
        return 'yellow'
    if S['index'] - 3 <= k < S['index'] and len(S['f']) == S['index'] + 1:
        return 'blue' if k >= S['index'] - 1 else 'cyan'
    return None


def _formula(S):
    if 'index' not in S:
        return '`f[k]` = 只剩最右边 `k` 堆时，先手最多拿多少'
    return f'只剩最右 `{S["index"]}` 堆，总和 `s = {S["s"]}`：先手 + 后手 = {S["s"]}，先手 = `s − 后手`'



CONFIG = dict(
    num=1406, title='石子游戏 III', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='倒着扫 · 先手最多得分',
    tags=['灵神题单·动态规划', '灵神题单·数学算法', '难度分 2027'],
    code='''
class Solution(object):
    def stoneGameIII(self, stoneValue):

        f = [0]
        s =  0
        for index in range(1, len(stoneValue) + 1):
            s += stoneValue[-index]
            f.append(s - f[-1])
            if index > 1 and f[-1] < s - f[-3]:
                f[-1] = s - f[-3]
            if index > 2 and f[-1] < s - f[-4]:
                f[-1] = s - f[-4]

        if f[-1] > s - f[-1]:
            return "Alice"
        elif f[-1] == s - f[-1]:
            return "Tie"
        else:
            return "Bob"
''',
    call=f'Solution().stoneGameIII({A!r})',
    expect='Bob',
    views=[
        dict(type='text', fn=_formula, size=24, h=60),
        dict(type='array', var='stoneValue', label='stoneValue（从右往左处理）', h=200, cell=90,
             pointers={'len(stoneValue) - index': 'blue'}, pointer_labels={'len(stoneValue) - index': 'stone[-index]'},
             color=lambda S, i, v: 'blue' if 'index' in S and i == len(S['stoneValue']) - S['index'] else None,
             dim=lambda S, i, v: 'index' in S and i > len(S['stoneValue']) - S['index']),
        dict(type='array', var='f', label='f[k]：只剩最右 k 堆时先手最多拿多少（黄 = 正在算，蓝 = 后手的选择）', h=240, cell=90,
             pointers={'len(f) - 1': 'yellow'}, pointer_labels={'len(f) - 1': 'f[-1]'}, color=_fcol),
    ],
    watch=[('index', 'index', 'blue'), ('s', 's', 'cyan'), ('f[-1]', 'f[-1]', 'green')],
    captions={
        'f = [0]': '`f[0] = 0`：一堆石子都没有，先手拿 0',
        's =  0': '`s` 是当前这段后缀的石子总和（倒着扫，所以是前缀和）',
        'for index in range': lambda S, B, r: (f'`index = {S.index}`：现在只剩最右边 `{S.index}` 堆石子' if S.get('index') != B.get('index') else '所有后缀都算完了'),
        's += stoneValue[-index]': '加入 `stoneValue[-{index}] = {stoneValue[-index]}` → `s = {s}`',
        'f.append(s - f[-1])': '先手只拿 1 堆：后手从剩下拿到 `f[{index-1}] = {f[-2]}`，先手 = `{s} - {f[-2]}` = =={f[-1]}==',
        'if index > 1': lambda S, B, r: (f'先手拿 2 堆：剩下后手拿 `f[{S.index-2}] = {S.f[-3]}`，先手 `{S.s} - {S.f[-3]}` = {S.s - S.f[-3]}，比 {S.f[-1]} ' + ('更大 → ==换成它==' if S.f[-1] < S.s - S.f[-3] else '不更大 → 不换')) if S.index > 1 else '只剩 1 堆，没法拿 2 堆，跳过',
        'f[-1] = s - f[-3]': '`f[-1]` 更新为 =={f[-1]}==',
        'if index > 2': lambda S, B, r: (f'先手拿 3 堆：剩下后手拿 `f[{S.index-3}] = {S.f[-4]}`，先手 `{S.s} - {S.f[-4]}` = {S.s - S.f[-4]}，比 {S.f[-1]} ' + ('更大 → ==换成它==' if S.f[-1] < S.s - S.f[-4] else '不更大 → 不换')) if S.index > 2 else '不足 3 堆，没法拿 3 堆，跳过',
        'f[-1] = s - f[-4]': '`f[-1]` 更新为 =={f[-1]}==',
        'if f[-1] > s - f[-1]': '先手 `f[-1] = {f[-1]}`，后手 `s - f[-1] = {s - f[-1]}`：{"先手更多" if f[-1] > s - f[-1] else "先手不更多"}',
        'return "Alice"': '先手（Alice）拿得更多，Alice 赢',
        'elif f[-1] == s - f[-1]': '`{f[-1]} == {s - f[-1]}`？{"相等 → 平局" if f[-1] == s - f[-1] else "不相等"}',
        'return "Tie"': '分数相同，平局',
        'return "Bob"': '先手 `{f[-1]}` < 后手 `{s - f[-1]}` → ==Bob 赢==',
    },
    cards=dict(
        one_liner='f[i]：先手最多拿多少 = 剩余总和 − 后手最多拿多少',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['石子排成一行，两人轮流从左边拿 1、2 或 3 堆，拿完为止，分高者赢',
                 '双方都最优，返回 `"Alice"` / `"Bob"` / `"Tie"`',
                 '本视频：`[1,2,3,7,-4,5]` → `"Bob"`'],
        quote='先手能拿到的石子数，就可以用剩下石子的总数减去后手能拿到的石子数……f[i] = max(s - f[i + 1], s - f[i + 2], s - f[i + 3])',
        quote_src='—— yiduobo 题解原文',
        idea=['令 `f[i]` = 剩下第 i 到 n-1 堆时先手最多拿到的石子分',
              '先手拿 1/2/3 堆后，后手面对的是 `f[i+1]`、`f[i+2]`、`f[i+3]`',
              '三种情况写出来，去括号后都是 `s - f[…]`：取最大即可',
              '作者把数组倒过来处理，后缀和变成了前缀和'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`index > 1`、`index > 2` 是边界：石子不够就不能取 2、3 堆',
                 '最后比较 `f[-1]` 和 `s - f[-1]`，不是看 f 的正负',
                 '对比灵神：灵神把 f 向后多开 3 格省去边界判断；yiduobo 用 append 加条件判断'],
    ),
)
