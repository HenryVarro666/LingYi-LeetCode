CONFIG = dict(
    num=541, title='反转字符串 II', difficulty='Easy', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='每隔 2k 切一刀，反转前 k 个',
    tags=['灵神题单', '滑动窗口与双指针'],
    code='''
class Solution:
    def reverseStr(self, s: str, k: int) -> str:
        s = list(s)
        for i in range(0, len(s), k * 2):
            s[i: i + k] = s[i: i + k][::-1]  # 右端点自动和 n 取最小值
        return ''.join(s)
''',
    call='Solution().reverseStr("abcdefgh", 3)',
    expect='cbadefhg',
    views=[
        dict(type='text', fn=lambda S: (f"本段下标 `[{S['i']}, {min(S['i'] + S['k'], len(S['s']))})`，长度 `{min(S['i'] + S['k'], len(S['s'])) - S['i']}`" if 'i' in S and isinstance(S.get('s'), list) else ''), size=28),
        dict(type='array', var='s', label='s（蓝框 = 本段要反转的前 k 个）', cell=84, pointers={'i': 'pink'},
             window=('i', 'min(i + k, len(s)) - 1'), h=260),
    ],
    watch=[('i', 'i', 'pink'), ('k', 'k', 'blue'), ('2k', 'k * 2')],
    captions={
        's = list(s)': '字符串不能原地改，先转成列表 `{s}`',
        'for i in range': lambda S, B, r: ('i 超出长度，没有更多段了，循环结束' if 'i' in B and S.i == B.i else f"每隔 `2k = {S.k * 2}` 切一段，这一段从 `i = {S.i}` 开始"),
        's[i: i + k] =': '反转 `s[{i}:{i + k}]`：前 `k` 个字母翻个面；右端点越界时切片自动截到 `n`，所以最后不足 `k` 个也全部反转 → `{\'\'.join(s)}`',
        'return': '拼回字符串 `{ret}`',
    },
    cards=dict(
        one_liner='每隔 2k 切一刀，只反转每段的前 k 个',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['每 `2k` 个字符，反转其中前 `k` 个',
                 '剩余不足 `k` 个：全部反转；在 `k` 到 `2k` 之间：反转前 `k` 个',
                 '示例：`"abcdefg"`，`k = 2` → `"bacdfeg"`；本视频 `"abcdefgh"`，`k = 3`'],
        quote='所以我们要反转的下标区间为 [0,k),[2k,3k),[4k,5k),… 注意最后一个区间的右开端点要和 n 取最小值，防止下标越界。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`range(0, n, 2k)` 直接枚举每段的起点 `i`',
              '要反转的区间是 `[i, i+k)`，Python 切片越界会自动截断，不用手写 `min`',
              '切片反转 `[::-1]` 再赋值回去'],
        summary=['时间 `O(n)`，空间 `O(n)`（可原地改则 `O(1)`）',
                 '易错：步长是 `2k`，反转长度是 `k`，别搞混',
                 '易错：尾段不足 `k` 个也要整段反转，靠切片截断自动满足',
                 '反转字符串的双指针写法见第 344 题'],
    ),
)
