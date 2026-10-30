# setup 里的 Seq 只是普通 list，额外记下题解里 for 循环当前走到的下标 pos（仅用于画图，不影响代码逻辑）
SETUP = '''
import sys


class Seq(list):
    def __iter__(self):
        if sys._getframe(1).f_code.co_filename != '<solution>':
            return list.__iter__(self)
        return self._walk()

    def _walk(self):
        for k in range(len(self)):
            self.pos = k
            yield self[k]
        self.pos = len(self)
'''

NUMS = [4, 2, 4, 5, 6]


def _pos(S):
    return getattr(S.get('nums'), 'pos', None)


def _right(S):
    """窗口右端：s += x 之前窗口是 [left, pos-1]，之后是 [left, pos]"""
    p = _pos(S)
    if p is None:
        return None
    if p >= len(S['nums']):
        return len(S['nums']) - 1
    return p if S.get('_line') in (11, 12) else p - 1


def _win(S):
    if 'left' not in S or _pos(S) is None:
        return ''
    l, r, nums = S['left'], _right(S), S['nums']
    if S.get('_line') in (7, 8):
        return f'`{S["x"]}` 重复 → 移出左端点 `nums[{l}] = {nums[l]}`，窗口和 s = =={S["s"]}=='
    part = ' + '.join(str(v) for v in nums[l:r + 1]) or '空'
    return f'窗口 `[{l}, {r}]`：s = {part} = =={S["s"]}==，ans = {S["ans"]}'


def _color(S, k, v):
    p = _pos(S)
    if p is None or p >= len(S['nums']):
        return None
    if k == p and S.get('_line') in (6, 7, 8, 9):
        return 'red' if S.get('_line') == 6 and v in S['st'] else 'pink'
    if k == p:
        return 'pink'
    return None


def _cap_while(S, B, ret):
    x = S['x']
    if x in B['st']:
        return f'`{x}` ==已经在窗口里==了 → 加进来会重复，必须先从左边缩小窗口'
    return f'`{x}` 不在窗口里 → 可以直接加入'


CONFIG = dict(
    num=1695, title='删除子数组的最大得分', difficulty='Medium', category='滑动窗口',
    author='灵茶山艾府', technique='不定长滑动窗口 + 哈希集合',
    tags=['字节3个月', '字节6个月'],
    setup=SETUP,
    code='''
class Solution:
    def maximumUniqueSubarray(self, nums: List[int]) -> int:
        st = set()
        ans = s = left = 0
        for x in nums:
            while x in st:
                st.remove(nums[left])
                s -= nums[left]
                left += 1
            st.add(x)
            s += x
            ans = max(ans, s)
        return ans
''',
    call=f'Solution().maximumUniqueSubarray(Seq({NUMS}))',
    expect=17,
    views=[
        dict(type='text', fn=_win, h=60),
        dict(type='array', var='nums', label='nums（框 = 当前窗口，粉 = 新进来的 x）',
             pointers={'left': 'blue', 'nums.pos if nums.pos < len(nums) else None': 'pink'},
             pointer_labels={'nums.pos if nums.pos < len(nums) else None': 'x'},
             window=('left', lambda S: _right(S)), color=_color,
             dim=lambda S, k, v: _pos(S) is not None and k < S['left'], h=270, cell=110),
        dict(type='set', var='st', label='st（窗口里有哪些数，保证互不相同）', h=150),
    ],
    watch=[('left', 'left', 'blue'), ('x', 'x', 'pink'), ('s（窗口和）', 's', 'purple'), ('ans', 'ans', 'green')],
    captions={
        'st = set()': '`st` 记录窗口里的元素：==窗口内元素互不相同==',
        'ans = s = left': '`s` 维护窗口元素和，`left` 是窗口左端点',
        'for x in nums': lambda S, B, ret: (f'枚举右端点：新元素 `x = nums[{_pos(S)}] = {S["x"]}`'
                                            if _pos(S) is not None and _pos(S) < len(S['nums']) else '右端点枚举完毕'),
        'while x in st': _cap_while,
        'st.remove(nums[left])': '把左端点 `nums[{left}] = {nums[left]}` 移出集合',
        's -= nums[left]': '窗口和减去它：`s = {B.s} - {nums[left]} = {s}`',
        'left += 1': '左端点右移：`left` → {left}',
        'st.add(x)': '现在窗口里没有 `{x}` 了，放心加入',
        's += x': '窗口和加上 `{x}`：`s = {B.s} + {x} = {s}`',
        'ans = max': '窗口是合法的（无重复）→ 用窗口和更新答案：`ans = max({B.ans}, {s}) = {ans}`',
        'return ans': '最大得分 =={ret}==',
    },
    cards=dict(
        one_liner='和「无重复字符的最长子串」一样，只是额外维护窗口和',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['正整数数组 `nums`，删除一个==元素互不相同==的子数组，得分 = 子数组元素和',
                 '只删除一个子数组，求==最大得分==',
                 '示例：`[4,2,4,5,6]` → `17`（子数组 `[2,4,5,6]`）'],
        quote='本题和 3. 无重复字符的最长子串 是一样的，额外维护窗口中的元素和即可。',
        quote_src='—— 灵茶山艾府题解',
        idea=['枚举右端点 `x`：如果 `x` 已在窗口里，就==不断移出左端点==直到没有重复',
              '集合 `st` 判重，变量 `s` 维护窗口和，每个合法窗口都更新 `ans`',
              '元素都是正数 → 窗口越长和越大，所以「最长无重复」的思路直接适用'],
        summary=['时间 `O(n)`：`left` 总共最多右移 `n` 次；空间 `O(n)`',
                 '易错：用 `while` 而不是 `if`，重复的元素可能在窗口中间',
                 '先缩窗口、再加入 `x`、最后更新答案',
                 '灵神还给了布尔数组 `has` 的写法：值域小（`<= 10^4`）时更快',
                 '思考题：如果 `nums` 里有负数，还能这样滑窗吗？'],
    ),
)
