def _pos(S):
    if 'zero' not in S or 'one' not in S:
        return None
    return S['zero'] + S['one'] - 1


def _eq(S):
    if 'v' not in S or 'zero' not in S:
        return '条件：区间内 `0 的个数 × num2 = 1 的个数 × num1`'
    return (f"`v = zero×num2 − one×num1 = {S['zero']}×{S['num2']} − {S['one']}×{S['num1']}` = =={S['v']}=="
            f"，答案累计 `res = {S['res']}`")


CONFIG = dict(
    num=2489, title='固定比率的子字符串数', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='前缀和变形 · 哈希表计数',
    tags=['常用数据结构', '前缀和'],
    code='''
class Solution(object):
    def fixedRatio(self, s, num1, num2):

        cnt = {0 : 1}
        zero = one = 0
        res = 0
        for char in s:
            if char == '0':
                zero += 1
            else:
                one += 1
        
            v = zero * num2 - one * num1
            res += cnt.get(v, 0)
            cnt[v] = cnt.get(v, 0) + 1
        
        return res
''',
    call="Solution().fixedRatio('0110011', 1, 2)",
    expect=4,
    views=[
        dict(type='string', var='s', label='s（蓝 = 当前字符，后面的还没读到）', cell=96, h=190,
             color=lambda S, i, v: ('blue' if i == _pos(S) else None),
             dim=lambda S, i, v: _pos(S) is not None and i > _pos(S)),
        dict(type='map', var='cnt', label='cnt：v 出现的次数', fmt=lambda k, v: f'{k}: {v}', h=170, font=32),
        dict(type='text', h=110, size=28, fn=_eq),
    ],
    watch=[('zero', 'zero', 'cyan'), ('one', 'one', 'pink'), ('v', 'v', 'yellow'), ('res', 'res', 'green')],
    captions={
        'cnt = {0 : 1}': '`cnt[0] = 1`：空前缀的 `v = 0`，它也能当区间的左端点',
        'for char in s': lambda S, B, r: ('读取下一个字符' if 'zero' not in S else (
            f"读取下一个字符：`s[{S.zero + S.one}] = '{S.s[S.zero + S.one]}'`" if S.zero + S.one < len(S.s) else '字符读完了，退出循环')),
        'zero += 1': '读到 `0`：`zero` = {zero}',
        'one += 1': '读到 `1`：`one` = {one}',
        'v = zero': '`v = {zero} × {num2} − {one} × {num1}` = =={v}==；两个前缀的 v 相等 ⇔ 中间这段比例恰好是 `{num1}:{num2}`',
        'res += cnt.get': '之前 `v = {v}` 出现过 `{cnt.get(v, 0)}` 次，每一次对应一个合法区间 → `res` = =={res}==',
        'cnt[v] = ': '先累加答案、再登记自己：`cnt[{v}] = {cnt[v]}`',
        'return res': '固定比率的子串共 `{res}` 个',
    },
    cards=dict(
        one_liner='把比例条件变形成 v 相等，哈希表数「相同的 v」有几个',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['01 串 `s` 与两个整数 `num1`、`num2`，数有多少个子串满足',
                 '子串里 `0` 的个数 : `1` 的个数 = `num1 : num2`（子串非空）',
                 '示例：`s = 0110011`，`num1 = 1`，`num2 = 2` → `4`'],
        quote='(zero[right] - zero[left - 1]) * nums2 = (one[right] - one[left - 1]) * nums1，将left - 1和right项放到一起……就可以利用哈希表来求解。',
        quote_src='—— yiduobo 题解原文',
        idea=['区间 0、1 个数用前缀之差表示，比例式交叉相乘去掉除法',
              '把 `right` 与 `left−1` 的项分到两边：`zero×num2 − one×num1` 两端相等',
              '一趟遍历：先查 `cnt` 里同值出现几次累加，再把自己放进去'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`cnt` 初始 `{0: 1}`：从下标 0 开始的子串要靠空前缀配对',
                 '先累加答案再登记 `cnt`，避免子串为空',
                 '`zero`、`one` 只依赖上一轮，用两个变量代替数组',
                 '原文已是 Python 3 可运行写法，未作修改'],
    ),
)
