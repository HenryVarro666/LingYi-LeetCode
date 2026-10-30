def _top(S):
    if 't' not in S or 'i' not in S:
        return ''
    t, i, st = S['t'], S['i'], S.get('start')
    if S['_line'] in (11, 12, 13) and st is not None and st < i:
        return f"当前这一组：`t[{st}:{i}] = \"{t[st:i]}\"`"
    return f"处理 `t = \"{t}\"`，`i = {i}`"


CONFIG = dict(
    num=3926, title='有效单词计数', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='分组循环 · 哈希表计数',
    tags=['灵神题单·滑动窗口与双指针', '难度分 1608'],
    code='''
class Solution:
    def countWordOccurrences(self, chunks: list[str], queries: list[str]) -> list[int]:
        s = ''.join(chunks)
        cnt = defaultdict(int)

        for t in s.split():  # 不用 split 的写法见另一份代码
            n = len(t)
            i = 0
            while i < n:
                if t[i] == '-':
                    i += 1
                    continue
                start = i
                # 遇到 "--"（连续两个 '-'）就跳出循环
                while i < n and (t[i] != '-' or i < n - 1 and t[i + 1] != '-'):
                    i += 1
                cnt[t[start: i]] += 1

        return [cnt[q] for q in queries]
''',
    call='Solution().countWordOccurrences(["a-b wo", "rld --c-"], ["a-b", "c", "world", "b"])',
    expect=[1, 1, 1, 0],
    views=[
        dict(type='text', fn=lambda S: f"拼接后 `s = \"{S['s']}\"`" if 's' in S else '', size=26),
        dict(type='text', fn=_top, size=26),
        dict(type='string', var='t', label='当前单词块 t（蓝 = 当前组）', cell=70, pointers={'i': 'pink', 'start': 'blue'},
             color=lambda S, k, v: 'blue' if 'start' in S and 'i' in S and S['start'] <= k < S['i'] else None, h=200),
        dict(type='map', var='cnt', label='cnt：单词 → 出现次数', h=260),
    ],
    watch=[('i', 'i', 'pink'), ('start', 'start', 'blue'), ('n', 'n')],
    captions={
        "s = ''.join": '先把 chunks 拼成一个字符串 `s = "{s}"`',
        'cnt = defaultdict': '`cnt` 统计每个单词出现几次，后面直接查表回答询问',
        'for t in s.split()': '按空格切开，取下一块 `t = "{t}"`；空格一定是分隔符',
        'n = len(t)': '这一块长 `n = {n}`',
        'i = 0': '`i` 从块的开头开始，外层循环负责「找下一组的起点」',
        "if t[i] == '-'": lambda S, B, r: (f"`t[{S.i}] = '-'` → ==单词必须以字母开头==，这个连字符是多余的，跳过" if S.t[S.i] == '-'
                                           else f"`t[{S.i}] = '{S.t[S.i]}'` 是字母，一组从这里开始"),
        11: '跳过这个多余的 `-`：`i` → {i}',
        'continue': '回到外层循环，继续找字母作为起点',
        'start = i': '记录这一组的起点 `start = {start}`（分组循环的准备工作）',
        'while i < n and': lambda S, B, r: (
            f"内层：`t[{S.i}] = '{S.t[S.i]}'` 是字母，或是被字母夹住的 '-' → 组还没结束，继续扩" if S.i < len(S.t) and (S.t[S.i] != '-' or (S.i < len(S.t) - 1 and S.t[S.i + 1] != '-'))
            else (f"`i = {S.i}` 走到块尾 → 这一组结束" if S.i >= len(S.t)
                  else f"`t[{S.i}] = '-'` 后面是 `-` 或块尾 → 不是合法连字符，==这一组到此结束==")),
        16: '`i` 右移到 {i}，这一组继续变长',
        'cnt[t[start: i]]': '这一组 `t[{start}:{i}] = "{t[start:i]}"` 是一个有效单词，`cnt` 加一 → =={cnt[t[start:i]]}==',
        'return [cnt[q]': lambda S, B, r: f"每个询问直接查表：`{r}`；没出现的（如 `b`）defaultdict 给 0",
    },
    cards=dict(
        one_liner='分组循环：外层找起点，内层找终点，统计后扔进哈希表',
        complexity='时间 `O(C+Q)`，空间 `O(C)`',
        problem=['拼接 `chunks` 得到 `s`，单词 = 小写字母，中间的 `-` 必须两侧都是字母',
                 '其余字符（空格、多余的 `-`）都是分隔符，单词不能再被延长',
                 '示例：`["a-b wo","rld --c-"]` 查 `["a-b","c","world","b"]` → `[1,1,1,0]`'],
        quote='外层循环负责遍历组之前的准备工作（记录开始位置），和遍历组之后的统计工作。内层循环负责遍历组，找出这一组最远在哪结束。',
        quote_src='—— 灵茶山艾府题解',
        idea=['单词的第一个字符必须是字母，所以外层遇到 `-` 就跳过，遇到字母记下 `start`',
              '内层往右扩，遇到 `"--"` 或块尾的 `-` 就停，`t[start:i]` 就是一个单词',
              '哈希表计数，询问 `O(1)` 回答'],
        summary=['时间 `O(C+Q)`，空间 `O(C)`',
                 '分组循环不用特判最后一组：内层停在 `n`，统计放在内层之后',
                 '内层条件 `i < n - 1 and t[i+1] != "-"`：结尾的 `-` 不算单词的一部分',
                 '灵神还给了不用 `split` 的写法，把空格也放进内层的结束条件里'],
    ),
)
