def _info(S):
    if 'cnt1' in S and 'mid' not in S:
        return f"改成 `1010…` 要翻 ==cnt1 = {S['cnt1']}== 个，改成 `0101…` 要翻 ==cnt2 = {S['cnt2']}== 个"
    if 'mid' not in S:
        return ''
    t = f"二分答案：`[left, right] = [{S['left']}, {S['right']}]`，试 `mid` =={S['mid']}==（每 `{S['mid'] + 1}` 个字符里翻 1 个）"
    if 'cnt' in S:
        t += f"，已需翻转 `{S['cnt']}` 次"
    return t


CONFIG = dict(
    num=3398, title='字符相同的最短子字符串 I', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='二分答案 · 按 mid+1 切分相同段',
    code='''
class Solution(object):
    def minLength(self, s, numOps):
        
        cnt1 = 0
        cnt2 = 0

        for index, char in enumerate(s):
            if index % 2 == 0:
                cnt1 += int(char)
                cnt2 += 1 - int(char)
            else:
                cnt1 += 1 - int(char)
                cnt2 += int(char)
        
        if min(cnt1, cnt2) <= numOps:
            return 1
        
        left = 2
        right = len(s)
        while left < right:
            mid = (left + right) // 2
            cnt = 0
            p = 0
            while p < len(s):
                q = p + 1
                while q < len(s) and s[q] == s[p]:
                    q += 1
                
                length = q - p
                cnt += length // (mid + 1)
                p = q

            if cnt <= numOps:
                right = mid
            else:
                left = mid + 1
        
        return left
''',
    call='Solution().minLength("000001", 1)',
    expect=2,
    views=[
        dict(type='text', fn=_info, size=26, h=110),
        dict(type='string', var='s', pointers={'p': 'blue', 'q': 'pink'}, h=300,
             color=lambda S, i, v: ('blue' if 'p' in S and 'q' in S and S['p'] <= i < S['q'] and S['_line'] >= 25 else None)),
    ],
    watch=['cnt1', 'cnt2', 'left', 'right', 'mid', 'cnt', ('numOps', 'numOps', 'green')],
    captions={
        'cnt1 = 0': '`cnt1`：把 s 改成 `1010…` 需要翻转的个数',
        'cnt2 = 0': '`cnt2`：把 s 改成 `0101…` 需要翻转的个数',
        'cnt1 += int': '偶数位 `s[{index}] = {char}`：`1010…` 要它是 1、`0101…` 要它是 0 → `cnt1` = {cnt1}；`cnt2` 同步累加',
        'cnt2 += 1 - int': '偶数位应为 0：`s[{index}] = {char}` → `cnt2` = {cnt2}',
        'cnt1 += 1 - int': '奇数位 `s[{index}] = {char}`：`1010…` 要它是 0、`0101…` 要它是 1 → `cnt1` = {cnt1}；`cnt2` 同步累加',
        'cnt2 += int': '奇数位应为 1：`s[{index}] = {char}` → `cnt2` = {cnt2}',
        'if min(cnt1': lambda S, B, r: f'`min({S.cnt1}, {S.cnt2}) = {min(S.cnt1, S.cnt2)}`，操作次数 `{S.numOps}` → ' + ('够，能变成交替串' if min(S.cnt1, S.cnt2) <= S.numOps else '不够，交替串做不到，转入二分（答案至少为 2）'),
        'return 1': '交替串能做到，最长相同段就是 1',
        'left = 2': '`mid = 1` 已经单独判过，二分从 `left = 2` 开始',
        'right = len': '长度 `len(s)` 一定够（不翻也满足）：`right = {right}`',
        'mid = ': '试答案 `mid = ({left} + {right}) // 2 = {mid}`：能否让最长相同段 ≤ {mid}？',
        'cnt = 0': '`cnt` 统计需要翻转的次数',
                'length = q - p': '相同段 `s[{p}:{q}]`，长度 `{length}`',
        'cnt += length': '长 `{length}` 的段按每 `{mid + 1}` 个切一组，每组翻 1 个：`{length} // {mid + 1}` = {length // (mid + 1)} 次 → `cnt` = =={cnt}==',
        'if cnt <= numOps': lambda S, B, r: (f'`cnt = {S.cnt} <= numOps = {S.numOps}`：{S.mid} 做得到，答案可能更小 → `right = mid`' if S.cnt <= S.numOps
                                              else f'`cnt = {S.cnt} > numOps = {S.numOps}`：{S.mid} 做不到 → `left = mid + 1`'),
        'right = mid': '`right` → {right}',
        'left = mid + 1': '`left` → {left}',
        'return left': '`left == right`，最小长度 `{left}`',
    },
    skip=['for index, char', 'if index % 2', 'cnt2 += ', 'while q < len(s)', 'p = q', 'q = p + 1', 'q += 1', 'p = 0', 'cnt = 0'],
    max_steps=90,
    cards=dict(
        one_liner='二分「最长相同段」的上限 mid，看翻转次数够不够',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['二进制串 `s`，最多翻转 `numOps` 个字符',
                 '让最长的「全相同」子串尽量短，返回这个最短长度',
                 '示例：`s = "000001"`，`numOps = 1` → `2`'],
        quote='对于这类最大化某个最小值，或者最小化某个最大值的问题，一种常见的处理方法是二分答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['答案越大越容易达到，满足单调性 → 二分 `mid`',
              '一段长 `length` 的相同段，按每 `mid+1` 个一组，每组翻 1 个，共 `length // (mid+1)` 次',
              '`mid = 1` 是特例：只能变成 `1010…` 或 `0101…`，先单独判断'],
        summary=['时间 `O(n log n)`，空间 `O(1)`',
                 '易错点：`mid = 1` 时「翻中间那个」会和邻居相同，所以要先单独处理，二分从 2 开始',
                 '一段长 `length` 翻 `length // (mid+1)` 次即可：余下的不足 mid+1 个，相同段不超过 mid',
                 '原文已是 Python 3 可运行的写法，未改动代码'],
    ),
)
