CONFIG = dict(
    num=2264, title='字符串中最大的 3 位相同数字', difficulty='Easy', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='分组循环 · 计数器',
    tags=['灵神题单', '滑动窗口与双指针', '难度分 1309'],
    code='''
class Solution:
    def largestGoodInteger(self, num: str) -> str:
        mx = ""
        cnt = 1
        for i in range(1, len(num)):
            if num[i] != num[i - 1]:
                cnt = 1
                continue
            cnt += 1
            if cnt == 3 and num[i] > mx:
                mx = num[i]
        return mx * 3
''',
    call='Solution().largestGoodInteger("6777133339")',
    expect='777',
    views=[
        dict(type='string', var='num', pointers={'i': 'blue'}, h=260,
             color=lambda S, i, v: 'green' if 'i' in S and 'cnt' in S and S['cnt'] >= 1 and S['i'] - S['cnt'] < i <= S['i'] and S['cnt'] >= 2 else None),
        dict(type='text', h=120, fn=lambda S: f"当前连续相同长度 `cnt = {S['cnt']}`，目前最大数字 `mx = '{S['mx']}'`" if 'cnt' in S else ''),
    ],
    watch=['i', 'cnt', ('mx', 'mx', 'green')],
    captions={
        'mx = ""': '`mx` 记录目前找到的最大的优质数字（单个字符），空串比任何数字字符都小',
        'cnt = 1\n': '`cnt` 统计当前这段相同字符的长度，第 0 个字符自己算 1',
        'if num[i] != num[i - 1]': '`num[{i}] = {num[i]!r}` 和前一个 `{num[i-1]!r}` {"不同" if num[i] != num[i-1] else "相同"}',
        'cnt = 1': '和前一个字符不同 → 新的一段开始，`cnt` 重置为 1',
        'continue': '这一段断开了，直接看下一个字符',
        'cnt += 1': '和前一个相同 → 这段变长，`cnt` = =={cnt}==',
        'if cnt == 3': lambda S, B, r: (f"`cnt == 3` 且 `{S.num[S.i]} > {S.mx!r}` → 找到更大的优质数字" if S.cnt == 3 and S.num[S.i] > S.mx else (f"`cnt = {S.cnt}`，还没凑够 3 个" if S.cnt != 3 else f"凑够 3 个，但 `{S.num[S.i]}` 不大于当前的 `{S.mx!r}`，不更新")),
        'mx = num[i]': '更新答案：`mx = {mx!r}`（只存一个字符，最后再乘 3）',
        'return mx * 3': '`mx * 3` = =={ret!r}==；没找到时 `"" * 3` 仍是空串',
    },
    cards=dict(
        one_liner='用计数器数连续相同字符，数到 3 就更新最大值',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['字符串 `num` 由数字组成，找长为 3、由同一个数字重复 3 次的子串',
                 '返回其中最大的一个，没有就返回空串',
                 '示例：`"6777133339"` → `"777"`'],
        quote='用一个计数器 cnt 记录当前匹配长度，如果长度等于 3，则更新答案的最大值。如果相邻字母不同，则重置 cnt。',
        quote_src='—— 灵茶山艾府题解',
        idea=['按「分组循环」思路：相邻字符相同 `cnt` 加一，不同就从 1 重新数',
              '`cnt` 恰好等于 3 时说明出现了一个优质数字，和 `mx` 比大小',
              '这样即使把 3 改成别的数，也是线性时间'],
        after=[dict(heading='其他写法', lines=['十次遍历：从 `999` 到 `000` 依次判断是否在 `num` 中', '一次遍历：直接比较 `num[i]==num[i+1]==num[i+2]`'])],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`mx` 初始为空串，字符串比较保证任何数字都更大，包括 `0`',
                 '`cnt` 只在恰好等于 3 时更新，避免 4 连、5 连重复比较',
                 '最后返回 `mx * 3`，没找到时是空串'],
    ),
)
