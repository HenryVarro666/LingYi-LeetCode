CONFIG = dict(
    num=2434, title='使用机器人打印字典序最小的字符串', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='栈 + 后缀最小值',
    tags=['栈', '字符串贪心', '难度分 1953'],
    code='''
class Solution:
    def robotWithString(self, s: str) -> str:
      n = len(s)
      # 计算后缀最小值
      suf_min = ['z'] * (n + 1)
      for i in range(n - 1, -1, -1):
          suf_min[i] = min(suf_min[i + 1], s[i])

      ans = []
      st = []
      for i, ch in enumerate(s):
          st.append(ch)
          while st and st[-1] <= suf_min[i + 1]:
              ans.append(st.pop())
      return ''.join(ans)
''',
    call='Solution().robotWithString("bcabad")',
    expect='aabcbd',
    views=[
        dict(type='string', var='s', label='s（蓝 = 当前入栈的字符）', pointers={'i': 'blue'}, cell=90, h=180,
             dim=lambda S, i, v: 'i' in S and S['_line'] >= 11 and i < S['i'],
             color=lambda S, i, v: 'blue' if 'i' in S and S['_line'] >= 11 and i == S['i'] else None),
        dict(type='array', var='suf_min', label='suf_min[i]：s[i:] 里最小的字母', cell=90, h=180,
             pointers={'i': 'cyan'}, index=True),
        dict(type='stack', var='st', label='st（机器人手里的 t，栈顶在右）', h=120, font=34),
        dict(type='array', var='ans', label='ans（纸上已经写出的）', cell=80, h=130, color=lambda S, i, v: 'green'),
    ],
    watch=[('i', 'i', 'blue'), ('ch', 'ch', 'blue'), ('suf_min[i+1]', 'suf_min[i+1]', 'cyan'), ('st', 'st', 'yellow')],
    captions={
        'suf_min[i] = min': '`suf_min[{i}] = min({suf_min[i+1]}, {s[i]})` = =={suf_min[i]}==：`s[{i}:]` 里最小的字母',
        'st.append(ch)': '`{ch}` 先入栈，现在栈 `{st}`；能不能立刻写到纸上，要看后面还有没有更小的',
        'while st and': lambda S, B, r: (
            f"栈顶 `{S.st[-1]}` ≤ 后面最小 `{S.suf_min[S.i+1]}` → ==后面不会有更小的了，立刻出栈==" if S.st and S.st[-1] <= S.suf_min[S.i+1]
            else (f"栈顶 `{S.st[-1]}` > 后面最小 `{S.suf_min[S.i+1]}` → ==先不出栈==，等更小的字母出现" if S.st else '栈空了，处理下一个字母')),
        'ans.append(st.pop())': '栈顶 `{ans[-1]}` 写到纸上：`ans = {"".join(ans)}`',
        'return': '全部处理完，纸上写的就是答案 `{ret}`',
    },
    cards=dict(
        one_liner='栈顶不大于后面所有字母，就立刻写到纸上',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['机器人有空串 `t`：可把 `s` 的首字符放进 `t` 尾部，或把 `t` 的末字符写到纸上',
                 '求纸上能写出的==字典序最小==的字符串',
                 '示例：`s = "bac"` → `"abc"`；本视频：`"bcabad"` → `"aabcbd"`'],
        quote='根据题意，t 中字符是先进后出的，是一个栈。……如果栈顶 ≤ 剩余字母（后缀 s[i+1:]）中的最小值，就立刻出栈。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`t` 就是栈：问题变成「遍历 `s`，用一个辅助栈，让输出字典序最小」',
              '后面还有更小字母 → 栈顶先别写；没有了 → 立刻写，越早写小字母越好',
              '先预处理后缀最小值 `suf_min`，每步 O(1) 判断；相等也要出栈，免得更大的字母插到中间'],
        summary=['时间 `O(n)`，空间 `O(n)`：每个字母入栈、出栈各一次',
                 '易错：条件是 ==`<=`== 不是 `<`，`caba` 里相同的 a 必须及时写出，否则得到 `abac`',
                 '出栈用 `while`：写完一个后，下面的栈顶可能也满足条件',
                 '末尾 `suf_min[n] = "z"` 作哨兵，最后一个字母一定会出栈'],
    ),
)
