def _sn(n):
    s = '0'
    for _ in range(n - 1):
        s = s + '1' + ''.join('1' if c == '0' else '0' for c in reversed(s))
    return s


def _live(S):
    return 'now' in S and 'flag' in S and 'k' in S and S['k'] > 0


def _str(S):
    return _sn(S['now'] + 1) if _live(S) else ''


def _color(S, i, v):
    if not _live(S):
        return None
    if i == S['pow2'][S['now']] - 1:
        return 'yellow'
    if i == S['k'] - 1:
        return 'pink'
    return None


def _top(S):
    if not _live(S):
        return '先把 2 的幂列出来：`pow2[i] = 2^i`，找 `k` 附近的位置'
    k, now, p = S['k'], S['now'], S['pow2'][S['now']]
    f = '翻转过奇数次' if S['flag'] else '没翻转（或偶数次）'
    if k == p == 1:
        return f"`k = 1`：整个串最开头的 `0`（flag = {S['flag']}，{f}）"
    if k == p:
        return f"`k = {k} = 2^{now}`：正好是 `S_{now + 1}` 正中间的 `1`（flag = {S['flag']}，{f}）"
    if k < p:
        return f"`2^{now} = {p} > k = {k}`：`now` 还太大，往下找最大的 `2^m ≤ k`"
    return f"`2^{now} = {p} < k = {k}`：`k` 在 `S_{now + 1}` 的==右半==（flag = {S['flag']}，{f}）"


CONFIG = dict(
    num=1545, title='找出第 N 个二进制字符串中的第 K 位', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='找最大的 2^m ≤ k · 镜像折回 + flag 记翻转',
    tags=['灵神题单·位运算', '灵神题单·链表树与回溯'],
    code='''
class Solution(object):
    def findKthBit(self, n, k):

        pow2 = [1]
        while pow2[-1] < k:
            pow2.append(pow2[-1] + pow2[-1])
        
        now = len(pow2) - 1
        flag = 0
        while k > 0:
            while pow2[now] > k:
                now -= 1

            if k == pow2[now]:
                if k == 1:
                    return str(flag ^ 0)
                else:
                    return str(flag ^ 1)
            else:
                k = pow2[now] + pow2[now] - k
                flag ^= 1
''',
    call='Solution().findKthBit(4, 11)',
    expect='1',
    views=[
        dict(type='text', fn=_top, size=24, h=70),
        dict(type='array', var='pow2', label='pow2（粉 = now：当前比较的 2 的幂）', cell=80, pointers={'now': 'pink'}, h=170),
        dict(type='string', var=_str, label='S_(now+1)（黄 = 正中间的 1，粉 = 第 k 位）', cell=48, h=170, color=_color),
        dict(type='text', fn=lambda S: (f"每折回一次 `flag` 翻转一次 → 现在 `flag = {S['flag']}`，最后的答案 = 中间字符 ^ flag"
                                        if 'flag' in S else ''), size=24, h=60),
    ],
    watch=['k', ('now', 'now', 'pink'), ('flag', 'flag', 'green')],
    captions={
        'pow2 = [1]': '`pow2` 存 `1, 2, 4, 8…`：`S_m` 正中间的 `1` 就在第 `2^(m-1)` 位',
        'while pow2[-1] < k': lambda S, B, ret: (f'`{S.pow2[-1]} < k = {S.k}`：还不够大 → 再放一个' if S.pow2[-1] < S.k
                                                 else f'`{S.pow2[-1]} >= k = {S.k}`：够了，停止'),
        'pow2.append': '`pow2` 追加 `{pow2[-1]}`',
        'now = len(pow2) - 1': '`now` 指向 `pow2` 末尾：目前最大的 2 的幂',
        'flag = 0': '`flag` 记录==翻转次数的奇偶==：右半是左半反转再翻转，每折回一次就翻转一次',
        'while k > 0': lambda S, B, ret: (f'`k = {S.k}`，继续找' if S.k > 0 else '结束'),
        'while pow2[now] > k': lambda S, B, ret: (f'`pow2[{S.now}] = {S.pow2[S.now]} > k = {S.k}`：太大 → `now` 减 1' if S.pow2[S.now] > S.k
                                                  else f'`pow2[{S.now}] = {S.pow2[S.now]} ≤ k = {S.k}`：找到最大的 `2^m ≤ k`'),
        'now -= 1': '`now` → {now}',
        'if k == pow2[now]': lambda S, B, ret: ((f'`k = {S.k} == {S.pow2[S.now]}`：正好是==中间那个 1== 的位置' if S.k > 1 else '`k = 1 == pow2[0]`：折回到了串的最开头') if S.k == S.pow2[S.now]
                                                else f'`k = {S.k} > {S.pow2[S.now]}`：落在中间 1 的右边，要折回去'),
        'if k == 1': lambda S, B, ret: ('`k = 1`：是整个串最开头的 `0`' if S.k == 1 else f'`k = {S.k} ≠ 1`：是某次拼接时夹在中间的 `1`'),
        'return str(flag ^ 0)': '开头的 `0`，再按翻转奇偶 `flag = {flag}` 异或 → 返回 =={ret}==',
        'return str(flag ^ 1)': '中间的 `1`，再按翻转奇偶 `flag = {flag}` 异或 → 返回 =={ret}==',
        'k = pow2[now] + pow2[now] - k': '右半的第 `k` 位 ↔ 左半镜像位置 `2^m + 2^m − k` = =={k}==',
        'flag ^= 1': '折回左半要多翻转一次：`flag` → {flag}',
    },
    cards=dict(
        one_liner='k 在右半就折回左半的镜像位置，同时记一次翻转',
        complexity='时间 `O(log k)`，空间 `O(log k)`',
        problem=['`S1 = "0"`，`Si = S(i-1) + "1" + reverse(invert(S(i-1)))`',
                 '求 `Sn` 的第 `k` 位字符',
                 '示例：`n = 4, k = 11` → `S4 = 011100110110001` → `"1"`'],
        quote='若此时的k大于2^m，其对应回s[m]的位置就是2^m + 2^m - k。此时问题就转化为了s中第2^m + 2^m - k这个位置的字符是什么。重复这个过程直到某一时刻2^m = k。',
        quote_src='—— yiduobo 题解原文',
        idea=['`|S_n| = 2^n − 1`，所以找最大的 `2^m ≤ k`：`k` 恰等于它就是中间的 `1`（`k=1` 则是开头的 `0`）',
              '`k` 更大：位于 `1` 之后的 `reverse(invert(s[m]))`，镜像回 `2^m + 2^m − k`',
              '每折回一次相当于翻转一次，用 `flag` 异或记录，不需要递归'],
        summary=['时间 `O(log k)`，空间 `O(log k)`（`pow2` 数组）',
                 '`k` 每折回一次，最大的 `2^m` 至少减 1，所以循环很快结束',
                 '`k == 1` 要特判：它是开头的 `0`，不是拼接的 `1`',
                 '原文本身是 Python 3 可运行的写法，未做修改（参数 `n` 没有用到）',
                 '对比灵神：灵神用 `1 << (n-1)` 直接比较并递归，yiduobo 用 `pow2` 表找 m，用 `flag` 代替返回值翻转'],
    ),
)
