CONFIG = dict(
    num=2434, title='使用机器人打印字典序最小的字符串', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='枚举目标字母 + 栈',
    tags=['栈', '字符串贪心', '难度分 1953'],
    code='''
class Solution(object):
    def robotWithString(self, s):

        stack = []
        char_cnt = {}
        for char in s:
            char_cnt[char] = char_cnt.get(char, 0) + 1

        target = 'a'
        p = 0
        n = len(s)
        res = []
        while p < n:
            while stack and stack[-1] <= target:
                res.append(stack[-1])
                stack.pop()
            
            while char_cnt.get(target, 0) > 0:
                if s[p] == target:
                    res.append(target)
                else:
                    stack.append(s[p])

                char_cnt[s[p]] -= 1
                p += 1
            
            target = chr(ord(target) + 1)
        
        while stack:
            res.append(stack[-1])
            stack.pop()
        
        return ''.join(res)
''',
    call='Solution().robotWithString("bcaba")',
    expect='aabcb',
    views=[
        dict(type='string', var='s', label='s（蓝 = 已经处理到的位置 p）', pointers={'p': 'blue'}, cell=90, h=180,
             dim=lambda S, i, v: 'p' in S and i < S['p']),
        dict(type='map', var='char_cnt', label='char_cnt（s[p:] 里每个字母还剩几个）', fmt=lambda k, v: f"'{k}': {v}", h=120, font=30),
        dict(type='stack', var='stack', label='stack（机器人手里的 t，栈顶在右）', h=120, font=34),
        dict(type='array', var='res', label='res（纸上已经写出的）', cell=80, h=130, color=lambda S, i, v: 'green'),
        dict(type='text', fn=lambda S: f"当前 target = ==`{S['target']}`==" if 'target' in S else '', size=30, h=70),
    ],
    watch=[('target', 'target', 'yellow'), ('p', 'p', 'blue'), ('stack', 'stack', 'cyan'), ('res', "''.join(res)", 'green')],
    captions={
        'char_cnt[char] = ': '统计 `{char}` 的个数：`char_cnt[{char!r}] = {char_cnt[char]}`',
        "target = 'a'": '`target` 是当前要打印的最小字母，从 `a` 开始',
        'while p < n': lambda S, B, r: (f'`p = {S.p} < {S.n}`，还有字符没处理' if S.p < S.n else f'`p = {S.p}` 走完 `s`，只剩栈里的字符'),
        'while stack and stack[-1] <= target': lambda S, B, r: (
            f"栈顶 `{S.stack[-1]}` ≤ target `{S.target}` → ==它不会比后面的更大，先写出来==" if S.stack and S.stack[-1] <= S.target
            else '栈空或栈顶比 target 大 → 不弹'),
        'res.append(stack[-1])': '栈顶写到纸上：`res = {"".join(res)}`',
        'stack.pop()': '把刚写出的字符弹掉：`stack = {stack}`',
        'while char_cnt.get': lambda S, B, r: (
            f"`{S.target}` 还剩 `{S.char_cnt.get(S.target, 0)}` 个没处理 → 继续往右扫" if S.char_cnt.get(S.target, 0) > 0
            else f"`{S.target}` 都处理完了 → 换下一个字母"),
        'if s[p] == target': lambda S, B, r: (
            f"`s[{S.p}] = {S.s[S.p]}` ==就是 target== → 直接写到纸上" if S.s[S.p] == S.target
            else f"`s[{S.p}] = {S.s[S.p]}` 不是 `{S.target}` → 它在 target 左边，先压进栈"),
        'res.append(target)': '写出 `{target}`：`res = {"".join(res)}`',
        'stack.append(s[p])': '压栈：`stack = {stack}`',
        'char_cnt[s[p]] -= 1': '`{B.s[B.p]}` 处理过了，剩余个数减一 → {char_cnt[B.s[B.p]]}',
        'p += 1': '`p` → {p}',
        'target = chr': '`{B.target}` 打印完 → 下一个 target 是 ==`{target}`==',
        'while stack:': lambda S, B, r: ('`s` 全部处理完，栈里还有 `' + str(S.stack) + '` → 倒出来' if S.stack else '栈空了'),
        'return': '纸上就是答案 `{ret}`',
    },
    cards=dict(
        one_liner='先打印最小字母，它左边的全压栈，再换下一个字母',
        complexity='时间 `O(26n)` 即 `O(n)`，空间 `O(n)`',
        problem=['机器人 `t` 是栈：`s` 首字符可入 `t`，`t` 末字符可写到纸上',
                 '求纸上能写出的==字典序最小==的字符串',
                 '本视频：`s = "bcaba"` → `"aabcb"`'],
        quote='设原始字符串中字典序最小的字符为target，那么在第一轮操作时就应该将最左侧target左边的所有字符压入栈中，然后将target加入到答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['按 `a`、`b`、`c`…… 的顺序依次当 target：把它们按出现顺序全部写出',
              '每个 target 左边的字符压栈；下一轮 target 变大时，栈顶 `<=` target 的要先弹出',
              '`s` 扫完后，栈里剩的倒出来接在答案后面'],
        summary=['时间 `O(n)`（字母表固定 26），空间 `O(n)`',
                 '易错：弹栈条件是 `<= target`，不是 `<`',
                 '易错：`s` 扫完后别忘了把栈里剩余字符倒出',
                 '原文已是 Python 3 可运行，未做修改',
                 '对比灵神：灵神预处理后缀最小值、边扫边弹；yiduobo 按字母表从小到大一轮轮处理'],
    ),
)
