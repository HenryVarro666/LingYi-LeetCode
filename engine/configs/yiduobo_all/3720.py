CONFIG = dict(
    num=3720, title='大于目标字符串的最小字典序排列', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='先判无解 · 顶着 target 填 · 回溯变大',
    tags=['灵神题单', '贪心与思维', '难度分 1958'],
    code='''
class Solution(object):
    def lexGreaterPermutation(self, s, target):
        
        cnt = {}
        for c in s:
            cnt[c] = cnt.get(c, 0) + 1
        
        t = ""
        for index in range(25, -1, -1):
            c = chr(index + 97)
            t += c * cnt.get(c, 0)

        if t <= target:
            return ''
        
        res = []
        p = 0
        while p < len(target) - 1 and cnt.get(target[p], 0) > 0:
            cnt[target[p]] -= 1
            res.append(target[p])
            p += 1

        while True:
            c = chr(ord(target[p]) + 1)
            while c <= 'z' and cnt.get(c, 0) == 0:
                c = chr(ord(c) + 1)
            
            if c <= 'z':
                res.append(c)
                cnt[c] -= 1
                for index in range(26):
                    c = chr(index + 97)
                    res.append(c * cnt.get(c, 0))
                return ''.join(res)
            
            p -= 1
            res.pop()
            cnt[target[p]] += 1
''',
    call='Solution().lexGreaterPermutation("abc", "acb")',
    expect='bac',
    skip=['c = chr(ord(c) + 1)', 'while c <= \'z\' and', 'for index in range(25', 't += c', 'c = chr(index + 97)', 'for index in range(26)', 'res.append(c * cnt'],
    views=[
        dict(type='string', var='target', label='target（蓝 = 当前位置 p）', cell=100, h=170,
             pointers={'p': 'blue'}, color=lambda S, k, v: 'blue' if S.get('p') == k else None),
        dict(type='array', var='res', label='res（正在构造的答案，绿 = 刚填的）', cell=100, h=150,
             color=lambda S, k, v: 'green' if k == len(S['res']) - 1 else None),
        dict(type='map', var='cnt', label='cnt（剩余可用字母）', fmt=lambda k, v: f"'{k}': {v}", h=150, font=34),
        dict(type='text', fn=lambda S: (f"最大排列 `t = '{S['t']}'` 与 `target = '{S['target']}'` 比较" if 't' in S and 'res' not in S else
                                        f"当前尝试：`target[{S['p']}]` 之后找更大的字母" if 'p' in S and 'res' in S else ''), size=28, h=80),
    ],
    watch=[('p', 'p', 'blue'), ('c', 'c', 'orange'), ('t', 't', 'pink')],
    captions={
        'cnt = {}': '`cnt` 统计 s 中每个字母的次数',
        'cnt[c] = cnt.get': '`cnt = {cnt}`',
        't = ""': '先造 s 能排出的==最大==排列：字母从 z 到 a 排',
        'for index in range(25': '`{chr(index + 97)!r}` 的数量：`{cnt.get(chr(index + 97), 0)}`',
        't += c': '`t` → `{t!r}`',
        'if t <= target': lambda S, B, r: (f"最大排列 `{S.t}` <= `{S.target}`：连最大的都不够大 → 无解，返回空串" if S.t <= S.target
                                           else f"最大排列 `{S.t}` > `{S.target}`：==一定有解==，下面构造最小的"),
        'res = []': '`res` 是答案前缀，先顶着 target 填',
        'p = 0': '`p` 指向 target 当前位置',
        'while p < len(target) - 1': lambda S, B, r: (f"`target[{S.p}] = '{S.target[S.p]}'` 还有剩余 → 能照抄，再往后" if S.p < len(S.target) - 1 and S.cnt.get(S.target[S.p], 0) > 0
                                                      else f"`target[{S.p}] = '{S.target[S.p]}'` 没有剩余了或到末位 → 停止照抄"),
        'cnt[target[p]] -= 1': '用掉一个 `{target[p]}`，`cnt = {cnt}`',
        'res.append(target[p])': '`res` 追加 `{target[p]}` → `{"".join(res)}`',
        'p += 1': '`p` → {p}',
        'while True': '开始在位置 `p = {p}` 找“比 target 稍大”的字母',
        'c = chr(ord(target[p]) + 1)': '从 `target[{p}]` 的下一个字母 `{c!r}` 开始找',
        'if c <= \'z\'': lambda S, B, r: (f"找到了剩余的字母 `{S.c}`，比 `{S.target[S.p]}` 大 → 填上它" if S.c <= 'z'
                                          else f"位置 {S.p} 上没有比 `{S.target[S.p]}` 更大的剩余字母 → ==回溯==，改前一位"),
        'res.append(c)': '`res` 追加更大的字母 `{c}` → `{"".join(res)}`',
        'cnt[c] -= 1': '用掉一个 `{c}`',
        'for index in range(26)': '剩下的字母按从小到大填满',
        'c = chr(index + 97)': '`{c!r}` 还剩 `{cnt.get(c, 0)}` 个',
        'res.append(c *': '`res` → `{"".join(res)}`',
        'return \'\'.join(res)': '剩下的字母从小到大填满，答案 `{ret!r}`',
        'p -= 1': '回溯：`p` → {p}',
        'res.pop()': '弹出前一位填的字母，`res = {"".join(res)}`',
        'cnt[target[p]] += 1': '把 `{target[p]}` 还给 `cnt`，在这一位上找更大的字母',
        'return \'\'': '无解，返回空串',
    },
    max_steps=80,
    cards=dict(
        one_liner='先顶着 target 往下填，填不动就回溯，换成稍大的字母',
        complexity='时间 `O(n + |Σ|)`，空间 `O(|Σ|)`',
        problem=['把 `s` 重新排列，使字典序==严格大于== `target` 且最小，没有则返回 `""`',
                 '示例：`s = "abc"`，`target = "acb"` → `"bac"`',
                 '本视频用的就是这个例子，会演示回溯'],
        quote='最理想的情况就是得到的字符串的前缀都与target一样，仅有最后一个字符比target的最后一个字符更大。',
        quote_src='—— yiduobo 题解原文',
        idea=['先拼出 s 的最大排列，如果它也 `<= target` 就无解',
              '否则尽量照抄 target 的前缀，直到字母用完；然后填一个稍大的字母，剩余从小到大',
              '这一位没有更大的字母，就弹出前一位、还回字母，在前一位上继续找'],
        result='`ac` 之后没有更大的字母 → 退到 `a` 之前，把 `a` 换成 `b`，后面填 `a`、`c`：`bac` ✓',
        summary=['时间 `O(n + |Σ|)`，空间 `O(|Σ|)`',
                 '先判无解，之后回溯一定能找到合法位置',
                 '照抄前缀时循环条件是 `p < len(target) - 1`：最后一位要留给“变大”',
                 '与灵神对比：灵神用 neg 与 mx 判断能否变大；yiduobo 直接填并回溯',
                 '原文已是 Python 3 可运行的写法，未做修改'],
    ),
)
