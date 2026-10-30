def _top(S):
    ln = S.get('_line', 0)
    if 'index' not in S or 'res' not in S:
        return ''
    if 's1' in S:
        return f"`str1[{S['index']}] = {S['s1']}`" + ('：这段必须等于 `str2`' if S['s1'] == 'T' else '：这段必须不等于 `str2`')
    return ''


def _pend(S, i, v):
    ci = S.get('change_index')
    return ci is not None and i in ci


CONFIG = dict(
    num=3474, title='字典序最小的生成字符串', difficulty='Hard', category='贪心与思维',
    author='yiduobo', technique='先填 T，其余填 a 再从后往前改',
    tags=['灵神题单·贪心与思维', '灵神题单·字符串', '难度分 2605'],
    code='''
class Solution(object):
    def generateString(self, str1, str2):
        
        n = len(str1)
        m = len(str2)
        list2 = list(str2)
        res = [None] * (n + m - 1)
        for index, s1 in enumerate(str1):
            if s1 == 'T':
                for offset, s2 in enumerate(str2):
                    res[index + offset] = s2
        
        for index, s1 in enumerate(str1):
            if s1 == 'T' and res[index: index + m] != list2:
                return ""
        
        change_index = set()
        for index in range(n + m - 1):
            if res[index] is None:
                change_index.add(index)
                res[index] = 'a'
        
        for index, s1 in enumerate(str1):
            if s1 == 'F' and res[index: index + m] == list2:
                p = index + m - 1
                while p >= index and p not in change_index:
                    p -= 1
                
                if p >= index:
                    res[p] = chr(ord(res[p]) + 1)
                else:
                    return ''
        
        return ''.join(res)
''',
    call='Solution().generateString("TFFT", "aa")',
    expect='aabaa',
    views=[
        dict(type='text', fn=_top, size=26),
        dict(type='string', var='str1', label='str1（T / F）', cell=84, h=190, pointers={'index': 'pink'},
             color=lambda S, k, v: 'green' if v == 'T' else 'orange'),
        dict(type='array', var='res', label='res（黄 = 没被 T 确定的位置，可以改）', cell=84, h=210,
             window=('index', 'index+m-1'),
             color=lambda S, k, v: 'yellow' if _pend(S, k, v) else None),
        dict(type='string', var='str2', label='str2', cell=84, h=130, color=lambda S, k, v: 'blue'),
    ],
    watch=['index', 'offset', 'p', ('change_index', 'sorted(change_index)', 'yellow')],
    captions={
        'n = len': '`n = {n}`，`m = {m}`：答案长度 `n + m - 1 = {n + m - 1}`',
        'list2 = list': '`list2`：把 `str2` 拆成列表，方便和 `res` 的切片比较',
        'res = [None]': '`res` 先全部设为 `None`（还没确定）',
        'res[index + offset] = s2': '`res[{index + offset}] = {s2}`',
        "s1 == 'T' and res[index": lambda S, B, r: (f"`str1[{S.index}] = {S.s1}`，不是 T，不用检查" if S.s1 != 'T'
                                                    else (f"`res[{S.index}:{S.index + S.m}] = {''.join(S.res[S.index:S.index + S.m])}` == `str2`，T 没有被别的 T 破坏" if S.res[S.index:S.index + S.m] == S.list2
                                                          else f"`res[{S.index}:{S.index + S.m}]` ≠ `str2`：两个 T 重叠矛盾 → ==返回空串==")),
        13: lambda S, B, r: (f'第二遍：检查每个 T 的子串有没有被别的 T 覆盖坏，现在看 `index = {S.index}`' if B.get('index') != S.index else '检查结束，T 之间没有矛盾'),
        18: lambda S, B, r: (f'找没被 T 确定的位置，现在看 `index = {S.index}`' if B.get('index') != S.index else '扫描结束，`change_index` 就是所有可改的位置'),
        23: lambda S, B, r: (f'处理 F：现在看 `index = {S.index}`' if B.get('index') != S.index else '所有 F 都处理完了'),
        'change_index = set()': '`change_index` 记录没被 T 确定的位置，只有这些位置能改',
        'if res[index] is None': lambda S, B, r: (f'`res[{S.index}]` 还是 None → 没被任何 T 覆盖' if S.res[S.index] is None else f'`res[{S.index}]` 已确定'),
        'change_index.add': '位置 `{index}` 记入 `change_index`',
        "res[index] = 'a'": '先填最小的字母 `a`',
        "s1 == 'F' and res[index": lambda S, B, r: (f"`str1[{S.index}] = {S.s1}`，不是 F，跳过" if S.s1 != 'F'
                                                     else (f"F 的子串 `{''.join(S.res[S.index:S.index + S.m])}` == `str2` → ==违规，必须改==" if S.res[S.index:S.index + S.m] == S.list2
                                                           else f"F 的子串 `{''.join(S.res[S.index:S.index + S.m])}` ≠ `str2` → 已满足")),
        'p = index + m - 1': '从子串最后一个位置 `p = {p}` 往前找可改的位置（贪心：改得越靠后字典序越小）',
        'while p >= index': lambda S, B, r: (f'`p = {S.p}` 在 change_index 里吗？' + ('不在 → 被 T 定死，继续往前' if S.p not in S.change_index else '在 → 可以改，停下')
                                             if S.p >= S.index else f'`p = {S.p} < index = {S.index}`：整段都被 T 定死 → 退出循环'),
        'p -= 1': '`p` → {p}',
        'if p >= index': lambda S, B, r: (f'`p = {S.p} ≥ index = {S.index}`：找到了可改的位置' if S.p >= S.index else '没找到可改的位置'),
        'res[p] = chr': '`res[{p}]` 从 `a` 改成下一个字母 `{res[p]}`，子串不再等于 `str2`',
        "return ''.join": '所有约束都满足，答案 `{ret}`',
    },
    cards=dict(
        one_liner='先填 T，空位全填 a，违规的 F 就改它最后一个空位',
        complexity='时间 `O(nm)`，空间 `O(n+m)`',
        problem=['`str1` 里 `T`：从该下标起长 `m` 的子串必须等于 `str2`；`F`：必须不等于',
                 '生成长 `n+m-1` 的字典序最小字符串，无法生成返回空串',
                 '本视频：`"TFFT"`、`"aa"` → `"aabaa"`'],
        quote='以贪心的思路来说，就应该从后往前，将当前子串中最后一个不是通过T确定下来的位置的字符修改为字母表中的下一个字符。',
        quote_src='—— yiduobo 题解原文',
        idea=['数据规模允许 `O(n·m)`：先按 T 填充，再检查所有 T 之间没有矛盾',
              '没被 T 覆盖的位置全填 `a`，这样字典序最小',
              'F 子串若等于 `str2`，从后往前找最后一个空位改成 `b`；作者没能构造出反例，并给出了直观证明'],
        summary=['时间 `O(nm)`，空间 `O(n+m)`',
                 '两个 `T` 重叠冲突时，第二遍检查会发现并返回空串',
                 '只有 `change_index` 里的位置可以改；整段都被 T 定死则无解',
                 '对比灵神：灵神在填 T 时顺带检查冲突，yiduobo 先全填再统一检查'],
    ),
)
