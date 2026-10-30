def _txt(S):
    if 'k' in S and 'x' in S and 'd' in S:
        return f'`(x − mn) ÷ d = {S["x"] - S["mn"]} ÷ {S["d"]}` → 第 `k = {S["k"]}` 项'
    if 'd' in S and 'n' in S:
        return f'公差 `d = ({S["mx"]} − {S["mn"]}) ÷ {S["n"] - 1} = {S["d"]}`，等差数列：' + ', '.join(str(S['mn'] + i * S['d']) for i in range(S['n']))
    return ''


CONFIG = dict(
    num=1502, title='判断能否形成等差数列', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='从公差入手 · 项号去重',
    tags=['灵神题单', '数学算法'],
    code='''
class Solution:
    def canMakeArithmeticProgression(self, arr: List[int]) -> bool:
        mn, mx = min(arr), max(arr)
        if mn == mx:  # 特殊情况：公差为 0 的等差数列
            return True

        n = len(arr)
        d, r = divmod(mx - mn, n - 1)
        if r:  # 公差 d 必须是整数
            return False

        has = [False] * n
        for x in arr:
            k, r = divmod(x - mn, d)
            if r or has[k]:  # k 不是整数或者之前遇到过
                return False
            has[k] = True
        return True
''',
    call='Solution().canMakeArithmeticProgression([5,1,9,3,7])',
    expect=True,
    views=[
        dict(type='array', var='arr', label='arr', h=190,
             color=lambda S, i, v: 'green' if 'x' in S and v == S['x'] and 'has' in S else None),
        dict(type='array', var=lambda S: S['has'] if 'has' in S else [], label='has[k]：第 k 项是否出现过', h=210,
             color=lambda S, i, v: 'green' if v else None),
        dict(type='text', fn=_txt, size=30, h=110),
    ],
    watch=['mn', 'mx', 'd', 'r', 'k', 'x'],
    captions={
        'mn, mx = min': '最小值 `mn = {mn}`，最大值 `mx = {mx}`：等差数列的首项和末项',
        'if mn == mx': '`mn == mx`？{mn} vs {mx}：不相等，不是公差为 0 的特殊情况',
        'divmod(mx - mn': '`M = m + (n-1)·d` → `d = ({mx} − {mn}) ÷ {n - 1}` = =={d}==，余数 `r = {r}`',
        'if r:  # 公差': '余数 `r = {r}`：{"不是整数公差，返回 False" if r else "能整除，公差是整数"}',
        'has = [False]': '`has[k]` 记录第 `k` 项（`mn + k·d`）有没有遇到，`k = 0 … n-1` 要各出现一次',
        'k, r = divmod': '`x = {x}`：`({x} − {mn}) ÷ {d}` → 第 `k = {k}` 项，余数 `r = {r}`',
        'if r or has[k]': '`r = {r}`，`has[{k}] = {has[k]}`：{"不是整数项或重复，返回 False" if r or has[k] else "是整数项、没出现过 → 继续"}',
        'has[k] = True': '第 `{k}` 项到位：`has[{k}] = True`',
        'return True': '`n` 个项号恰好各出现一次 → ==可以重排成等差数列==',
    },
    cards=dict(
        one_liner='首项末项定公差，每个数对应唯一项号，项号不重复即可',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`arr` 能否重新排列成等差数列（相邻两项差为同一常数）',
                 '示例：`[3,5,1]` → `true`；`[1,2,4]` → `false`',
                 '本视频：`[5,1,9,3,7]` → `true`'],
        quote='如果 k = 0,1,2,…,n−1 各恰好出现一次，那么 arr 可以重排成等差数列。',
        quote_src='—— 灵茶山艾府题解',
        idea=['若能排成等差数列，首项 `m`、末项 `M` 就是最小、最大值',
              '公差 `d = (M − m) / (n − 1)` 必须是整数',
              '每个数 `x = m + k·d`，==项号 `k` 必须是整数且不重复==，不用排序也不用哈希集合'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`mn == mx` 要先特判，否则 `d = 0` 会除零',
                 '灵神还给了「排序」和「哈希集合」两种写法，本视频演示最后的优化写法'],
    ),
)
