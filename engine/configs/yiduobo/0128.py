def _order(S):
    return list(S['num_set']) if 'num_set' in S else None


def _idx(name):
    def f(S):
        if name not in S or 'num_set' not in S or S[name] not in S['num_set']:
            return None
        return list(S['num_set']).index(S[name])
    return f


_NUM = _idx('num')
_X = _idx('x')


def _counting(S):
    """True when x/tmp belong to the current num (not left over from an earlier num)."""
    ns, num, x, tmp = S.get('num_set'), S.get('num'), S.get('x'), S.get('tmp')
    if ns is None or num is None or x is None or tmp is None or num + 1 in ns:
        return False
    return x <= num and num - x in (tmp, tmp - 1) and all(v in ns for v in range(num - tmp + 1, num + 1))


def _color(S, i, v):
    if 'num' not in S:
        return None
    ns, num = S['num_set'], S['num']
    if _counting(S) and num - S['tmp'] < v <= num:
        return 'green'
    if v == num:
        return 'purple' if num + 1 in ns else 'blue'
    return None


def _chain_text(S):
    ns, num = S.get('num_set'), S.get('num')
    if ns is None or num is None:
        return '只让每段序列的==最大数==往下数'
    if num + 1 in ns:
        return f"`num = {num}`：`num + 1 = {num + 1}` 存在 → ==不是最大数，跳过=="
    if not _counting(S):
        return f"`num = {num}`：`num + 1 = {num + 1}` 不存在 → ==是最大数=="
    x, tmp = S['x'], S['tmp']
    got = ' '.join(f'`{v}`' for v in range(num, num - tmp, -1))
    if num - x == tmp:
        tail = f'  → 查 `{x}`：' + ('存在' if x in ns else '==不存在==，数完了')
    else:
        tail = ''
    return f"从 `{num}` 往下数：{got or '（还没数）'}{tail}　长度 `tmp = {tmp}`"


def _is_max(S, B, ret):
    n, ns = S.num, S.num_set
    if n + 1 in ns:
        return f'`{n + 1}` 存在 → `{n}` 不是序列中的最大数，==跳过=='
    return f'`{n + 1}` 不存在 → `{n}` 是序列的==最大数==，开始逐个往下检测'


CONFIG = dict(
    num=128, title='最长连续序列', difficulty='Medium', category='哈希',
    author='yiduobo', technique='哈希表 + 只从序列最大数往下数',
    code='''
class Solution(object):
    def longestConsecutive(self, nums):
        num_set = set(nums)
        res = 0
        for num in num_set:
            if num + 1 not in num_set:
                x = num
                tmp = 0
                while x in num_set:
                    tmp += 1
                    x -= 1
                res = max(res, tmp)
        return res
''',
    call='Solution().longestConsecutive([100, 4, 200, 1, 3, 2])',
    expect=4,
    views=[
        dict(type='array', var='nums', h=170, cell=80, label='nums（原数组）'),
        dict(type='array', var=_order, pointers={_NUM: 'blue', _X: 'yellow'}, pointer_labels={_NUM: 'num', _X: 'x'},
             color=_color, h=230, cell=96, label='num_set（按遍历顺序；紫 = 不是最大数，绿 = 已数到的段）'),
        dict(type='text', fn=_chain_text, size=30),
    ],
    watch=[('num', 'num', 'blue'), ('x', 'x', 'yellow'), ('tmp', 'tmp', 'green'), ('res', 'res', 'orange')],
    captions={
        'num_set = set(nums)': '哈希表：==常数时间==判断一个数在不在数组中',
        'res = 0': '`res` 记录答案',
        'for num in num_set': lambda S, B, r: ('遍历结束' if 'num' in B and B.num == S.num else f'考察 `num = {S.num}`'),
        'if num + 1 not in num_set': _is_max,
        'x = num': '从最大数 `x = {x}` 开始往下数',
        'tmp = 0': '`tmp` 统计这段序列的长度',
        'while x in num_set': lambda S, B, r: (f'`{S.x}` 在集合中' if S.x in S.num_set
                                               else f'`{S.x}` 不在集合中 → 这段序列数完了'),
        'tmp += 1': '长度 `tmp` → {tmp}',
        'x -= 1': '继续检测 `x − 1 = {x}`',
        'res = max': '这段序列长 `{tmp}`：`res = max({B.res}, {tmp}) = {res}`',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='每段序列只从它的==最大数==开始往下数一遍',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['未排序整数数组 `nums`，求==数值连续==的最长序列长度（不要求在原数组中相邻）',
                 '要求 `O(n)` 时间',
                 '示例：`[100,4,200,1,3,2]` → `4`（最长是 `1,2,3,4`）'],
        quote='一个很自然的想法就是==从序列的最大数开始判断==，若x不是序列中的最大数，那么跳过……如何判断呢？检测x + 1是否存在即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['朴素：每个数都向两边探测 `x±1, x±2, …`，同一段被反复判断，`O(n²)`',
              '例：对 2 判断了 1、3、4，对 3 又判断 1、2、4 —— 非常浪费',
              '只让==最大数==往下探测：`x+1` 存在就跳过，每个数最多被检测一遍'],
        summary=['时间 `O(n)`：每段序列只被它的最大数完整扫一遍',
                 '排序后扫描的 `O(n log n)` 做法更好想，但不满足题目要求',
                 '和灵神对称：灵神从==最小数==往上数（看 `x−1`），yiduobo 从==最大数==往下数（看 `x+1`）',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串'],
    ),
)
