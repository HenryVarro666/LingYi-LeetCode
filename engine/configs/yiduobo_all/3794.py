CONFIG = dict(
    num=3794, title='反转字符串前缀', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='按题意直接切片',
    tags=['灵神题单·滑动窗口与双指针', '单序列双指针'],
    code='''
class Solution(object):
    def reversePrefix(self, s, k):
        return s[:k][::-1] + s[k:]
''',
    call='Solution().reversePrefix("hello", 3)',
    expect='lehlo',
    views=[
        dict(type='string', var='s', h=200, label='s（蓝色 = 前 k 个，灰 = 剩下的）', window=('0', 'k - 1'),
             color=lambda S, i, v: 'blue' if i < S['k'] else None,
             dim=lambda S, i, v: i >= S['k']),
        dict(type='text', fn=lambda S: f"`s[:k]` = `{S['s'][:S['k']]}`，`s[:k][::-1]` = `{S['s'][:S['k']][::-1]}`"),
        dict(type='text', fn=lambda S: f"`s[k:]` = `{S['s'][S['k']:]}`，拼起来 =={S['s'][:S['k']][::-1] + S['s'][S['k']:]}=="),
    ],
    watch=['s', ('k', 'k', 'blue')],
    captions={
        'return': '前半 `{s[:k]}` 反转成 `{s[:k][::-1]}`，再接上不变的 `{s[k:]}` → ==`{ret}`==',
    },
    cards=dict(
        one_liner='分成两段：前 k 个反转，其余不动',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给出字符串 `s` 和整数 `k`，反转前 `k` 个字符并返回',
                 '演示：`s="hello", k=3` → 前三位 `"hel"` 反转为 `"leh"`，结果 `"lehlo"`'],
        quote='比较基础的题目，直接按照题目要求执行就可以了。',
        quote_src='—— yiduobo 题解',
        idea=['用 `s[:k]` 和 `s[k:]` 把字符串拆成前缀和剩余部分',
              '`s[:k][::-1]` 就是反转后的前缀',
              '再与 `s[k:]` 拼接，就是最终答案'],
        after=[dict(heading='逐步拆解', lines=['第一步：`s[:k]` 取出要反转的前缀', '第二步：`[::-1]` 把前缀倒过来', '第三步：`s[k:]` 取出不动的后缀', '最后一步：两段字符串用 `+` 拼起来']),
               dict(heading='边界情况', lines=['`k = 1`：前缀只有一个字符，结果等于原串', '`k = len(s)`：后缀为空，整串被反转', '题目保证 `1 <= k <= len(s)`，不会越界', '切片越界在 Python 里也不会报错', '所以这题没有任何需要特判的地方'])],
        summary=['切片拷贝，时间空间都是 `O(n)`',
                 '代码与原文一致（仅空行不保留）',
                 '`[::-1]` 是 Python 反转序列的常用写法'],
    ),
)
