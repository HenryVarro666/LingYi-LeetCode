def _sn(n):
    s = '0'
    for _ in range(n - 1):
        s = s + '1' + ''.join('1' if c == '0' else '0' for c in reversed(s))
    return s


def _cur(S):
    return S.get('n'), S.get('k')


def _str(S):
    n = S.get('n')
    return _sn(n) if n else ''


def _color(S, i, v):
    n, k = _cur(S)
    if not n:
        return None
    if i == (1 << (n - 1)) - 1:
        return 'yellow'
    if i == k - 1:
        return 'pink'
    return 'dim' if False else None


def _top(S):
    n, k = _cur(S)
    if not n:
        return ''
    mid = 1 << (n - 1)
    if n == 1:
        return f"`S_1 = \"0\"`，只有一个字符"
    if k == mid:
        return f"`S_{n}` 长 {2 * mid - 1}：正中间是第 `{mid}` 位（黄），`k = {k}` 恰好就是它 → ==1=="
    if k < mid:
        return f"`S_{n}` 长 {2 * mid - 1}：`k = {k} < {mid}` 在==左半==，和 `S_{n - 1}` 的第 {k} 位一样"
    return f"`S_{n}` 长 {2 * mid - 1}：`k = {k} > {mid}` 在==右半==（反转再翻转的 `S_{n - 1}`）"


CONFIG = dict(
    num=1545, title='找出第 N 个二进制字符串中的第 K 位', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='递归 · 左半 / 正中 / 右半',
    tags=['灵神题单·位运算', '灵神题单·链表树与回溯'],
    code='''
class Solution:
    def findKthBit(self, n: int, k: int) -> str:
        if n == 1:
            return '0'
        if k == 1 << (n - 1):
            return '1'
        if k < 1 << (n - 1):
            return self.findKthBit(n - 1, k)
        res = self.findKthBit(n - 1, (1 << n) - k)
        return '0' if res == '1' else '1'
''',
    call='Solution().findKthBit(4, 11)',
    expect='1',
    views=[
        dict(type='text', fn=_top, size=24, h=70),
        dict(type='string', var=_str, label='当前这一层的 S_n（黄 = 正中间的 1，粉 = 第 k 位）', cell=64, h=170,
             color=_color),
        dict(type='calls', h=330, hide=('self',)),
    ],
    watch=['n', 'k', ('正中间', '1 << (n - 1)', 'yellow'), ('res', 'res', 'green')],
    captions={
        'if n == 1': lambda S, B, ret: ('`n = 1`：`S_1` 只有一个字符 `0` → 边界' if S.n == 1 else f'`n = {S.n} > 1`，还要继续判断'),
        4: '`S_1 = "0"`，直接返回 `0`',
        'if k == 1 << (n - 1)': lambda S, B, ret: (
            f'`k = {S.k}`，正中间是第 `2^{S.n - 1} = {1 << (S.n - 1)}` 位：==恰好是中间== → 它一定是 `1`' if S.k == 1 << (S.n - 1)
            else f'`k = {S.k} ≠ {1 << (S.n - 1)}`（中间位置），不在正中间'),
        6: '正中间一定是拼上去的 `1`，返回 `1`',
        'if k < 1 << (n - 1)': lambda S, B, ret: (
            f'`{S.k} < {1 << (S.n - 1)}` → 在==左半==：左半就是 `S_{S.n - 1}`，原样递归' if S.k < 1 << (S.n - 1)
            else f'`{S.k} > {1 << (S.n - 1)}` → 在==右半==：右半是 `S_{S.n - 1}` 反转再翻转'),
        'return self.findKthBit(n - 1, k)': '左半不用变换：直接问 `S_{n-1}` 的第 `{k}` 位',
        'res = self.findKthBit': lambda S, B, ret: (
            f'右半第 `k` 位 ↔ 反转前 `S_{B.n - 1}` 的第 `2^{B.n} − k = {(1 << B.n) - B.k}` 位，先递归去问它；回来后还要==翻转=='),
        "return '0' if res == '1'": lambda S, B, ret: f"下一层返回 `{B.res}`，右半要翻转 → =={ret}==",
    },
    cards=dict(
        one_liner='先判断 k 在左半、正中间还是右半，再缩小成 S_{n-1}',
        complexity='时间 `O(n)`，空间 `O(n)`（递归栈）',
        problem=['`S1 = "0"`，`Si = S(i-1) + "1" + reverse(invert(S(i-1)))`',
                 '求 `Sn` 的第 `k` 位字符',
                 '示例：`n = 4, k = 11` → `S4 = 011100110110001` → `"1"`'],
        quote='我们需要确定第 k 个字符位于 S_n 的左半、正中间还是右半。为此，首先要知道 S_n 的长度。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`|S_n| = 2^n − 1`：左半是前 `2^(n-1) − 1` 位，第 `2^(n-1)` 位是正中间的 `1`',
              '`k` 在左半：问题变成 `S_{n-1}` 的第 `k` 位',
              '`k` 在右半：对应反转前的第 `2^n − k` 位，递归回来后再==翻转==一次'],
        summary=['时间 `O(n)`，空间 `O(n)`；迭代写法只用一个 `rev` 记录翻转次数的奇偶，空间 `O(1)`',
                 '右半下标：`(1 << n) - k`，不是 `k - 2^(n-1)`',
                 '返回的是字符串 `"0"/"1"`，翻转时别写成整数运算',
                 '方法二：奇数位交替 `0101…`，偶数位去掉尾零后交替，`O(1)` 公式（用 `k & -k` 去尾零）'],
    ),
)
