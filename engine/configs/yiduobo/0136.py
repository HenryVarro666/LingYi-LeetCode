NUMS = [2, 3, 5, 3, 2]

TRACK = '''
class KList(list):  # 快照用的普通 list（带上下标 k）
    pass

class TList(list):  # 只用于动画：记录 for 循环当前遍历到的下标 k
    def __iter__(self):
        for k in range(len(self)):
            self.k = k
            yield list.__getitem__(self, k)
        self.k = None

    def __deepcopy__(self, memo):
        c = KList(list.copy(self))
        c.k = getattr(self, 'k', -1)
        return c
'''


def _k(S):
    nums = S.get('nums')
    k = getattr(nums, 'k', None)
    return k if isinstance(k, int) and k >= 0 else None


def _applied(S):
    """这一步是否已经执行了 res ^= num（只用于画图）"""
    k, res = _k(S), S.get('res')
    if k is None or res is None:
        return False
    acc = 0
    for v in NUMS[:k + 1]:
        acc ^= v
    return res == acc


def _bin_line(S):
    if 'res' not in S:
        return ''
    res, num = S['res'], S.get('num')
    if _applied(S):
        return f'`{res ^ num:03b}` ⊕ `{num:03b}` = =={res:03b}==　（{res ^ num} ⊕ {num} = {res}）'
    return f'当前 `res = {res:03b}`（{res}）'


def _xor_cap(S, B, ret):
    k = _k(S)
    s = f'`res = {B.res} ⊕ {S.num} = {S.res}`（`{B.res:03b} ⊕ {S.num:03b} = {S.res:03b}`）'
    if k is not None:
        seen = NUMS[:k + 1]
        odd = [v for i, v in enumerate(seen) if seen.count(v) % 2 and v not in seen[:i]]
        if seen.count(S.num) == 2:
            s += f'：第二个 `{S.num}` 与第一个==抵消==，res 等价于 `{" ⊕ ".join(map(str, odd))}`'
    return s


CONFIG = dict(
    num=136, title='只出现一次的数字', difficulty='Easy', category='技巧',
    author='yiduobo', technique='异或 · 一次遍历',
    code='''
class Solution(object):
    def singleNumber(self, nums):
        res = 0
        for num in nums:
            res ^= num

        return res
''',
    setup=TRACK,
    call=f'Solution().singleNumber(TList({NUMS}))',
    expect=5,
    views=[
        dict(type='array', var='nums', label='nums（灰色 = 已异或进 res）', cell=110, h=220,
             pointers={_k: 'cyan'}, pointer_labels={_k: 'num'},
             dim=lambda S, i, v: _k(S) is not None and (i < _k(S) or (i == _k(S) and _applied(S))) if 'res' in S else False),
        dict(type='text', fn=_bin_line, size=34, h=80),
        dict(type='text', fn=lambda S: '`x ⊕ 0 = x`，`x ⊕ x = 0`：出现两次的数异或后变成 0', size=26),
        dict(type='table', var=lambda S: [[v >> b & 1 for b in (2, 1, 0)] for v in NUMS],
             label='每个数的二进制（每一列 1 的个数为偶数 → 结果这一位是 0）',
             rows=lambda S: [str(v) for v in NUMS], cols=lambda S: ['第2位', '第1位', '第0位'],
             color=lambda S, i, j, v: ('cyan' if v else None) if _k(S) is not None and (i < _k(S) or (i == _k(S) and _applied(S))) else None,
             cell=56, h=280),
    ],
    watch=[('num', 'num', 'cyan'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 从 0 开始：`x ⊕ 0 = x`，不影响结果',
        'for num in nums': lambda S, B, ret: (f'取下一个数 `num = {S.num}`' if _k(S) is not None else '所有数都异或完了'),
        'res ^= num': _xor_cap,
        'return res': '成对的数都抵消成 0，只剩落单的 → 返回 =={ret}==',
    },
    cards=dict(
        one_liner='把所有数异或起来，出现两次的数自己消掉',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['非空数组 `nums` 中，除了某个元素只出现一次，其余每个元素都出现==两次==',
                 '找出只出现一次的元素；要求==线性时间、常量空间==',
                 '示例：`[4,1,2,1,2]` → `4`'],
        quote='利用到异或运算的性质，==x异或0等于x，且x异或x等于0==。于是可以将所有数全部异或起来，出现两次数因为异或了自身于是变成了0，最后就剩下那个只出现一次的数了。',
        quote_src='—— yiduobo 题解',
        idea=['`res` 初始为 0：`0 ⊕ x = x`',
              '依次 `res ^= num`：异或不看顺序，两个相同的数迟早抵消',
              '看二进制：每一位上，成对的数贡献偶数个 1 → 这一位结果为 0'],
        result='`2、3` 都出现两次被抵消，返回 `5` ✓',
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`res` 必须从 0 开始（`0` 是异或的“单位元”）',
                 '中间的 `res` 看起来乱跳没关系，最后成对的都会抵消',
                 '原文为 Python 2 写法：仅删去文档字符串，逻辑未改'],
    ),
)
