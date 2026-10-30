CONFIG = dict(
    num=1255, title='得分最高的单词集合', difficulty='Hard', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='子集型回溯（选或不选）',
    tags=['灵神题单', '链表树与回溯', '难度分 1882'],
    setup='''
SC = [0] * 26
for ch, v in zip('abxz', (4, 4, 5, 10)):
    SC[ord(ch) - 97] = v
''',
    code='''
class Solution:
    def maxScoreWords(self, words: List[str], letters: List[str], score: List[int]) -> int:
        ans = 0
        left = Counter(letters)
        score = dict(zip(ascii_lowercase, score))  # 字母对应的分数

        def dfs(i: int, total: int) -> None:
            if i < 0:  # base case
                nonlocal ans
                ans = max(ans, total)
                return

            # 不选 words[i]
            dfs(i - 1, total)

            # 选 words[i]
            for j, c in enumerate(words[i]):
                if left[c] == 0:  # 剩余字母不足
                    for c in words[i][:j]:  # 撤销
                        left[c] += 1
                    return
                left[c] -= 1  # 减少剩余字母
                total += score[c]  # 累加得分

            dfs(i - 1, total)

            # 恢复现场
            for c in words[i]:
                left[c] += 1

        dfs(len(words) - 1, 0)
        return ans
''',
    call='Solution().maxScoreWords(["ax", "xxz"], ["z", "a", "x", "x"], SC)',
    expect=20,
    views=[
        dict(type='array', var='words', label='words（蓝 = 当前考虑的 words[i]）', cell=110, h=160, pointers={'i': 'blue'}),
        dict(type='map', var='left', label='left（剩余字母个数）', h=130, font=26),
        dict(type='calls', h=190, hide=('words',)),
        dict(type='text', h=60, fn=lambda S: f"当前得分 `total` = =={S['_inner'].get('total', 0)}==，历史最高 `ans` = =={S['ans']}==" if 'ans' in S else ''),
    ],
    watch=[('i', lambda S: S['_inner'].get('i'), 'blue'), ('total', lambda S: S['_inner'].get('total'), 'yellow'), ('ans', 'ans', 'green')],
    skip=['ans = 0', 'left = Counter', 'score = dict', 'def dfs', 'nonlocal ans', 'for j, c in enumerate', 'for c in words[i][:j]', 'for c in words[i]:'],
    max_steps=110,
    captions={
        'if i < 0': lambda S, B, ret: ('`i < 0` → ==所有单词都决定完了==，到达叶子，记录得分' if S['_inner'].get('i', 0) < 0
                                       else f"`i = {S['_inner'].get('i')}`：还剩 `words[0..{S['_inner'].get('i')}]` 要决定选或不选"),
        'ans = max(ans, total)': '叶子处更新答案：`ans = max({B.ans}, {total})` = =={ans}==',
        14: "先走「不选」分支：不选 `words[{B.i}]`，得分不变 `total = {B.total}`，进入下一层",
        25: "「选」分支：`words[{B.i}]` 的字母都扣完了，得分 `{B.total}`，进入下一层",
        'if left[c] == 0': '看字母 `{c}`：剩余 `{left[c]}` 个 → {"==不足，这个单词选不了==" if left[c] == 0 else "够用，继续"}',
        'left[c] -= 1': '用掉一个 `{c}`：`left[{c!r}]` = {left[c]}',
        'total += score[c]': '累加字母分：`total` = =={total}==',
        20: '字母不够，把本单词已经扣掉的字母加回去（撤销），这条「选」分支作废',
        11: '叶子处理完了 → 返回上一层',
        21: '「选」分支作废 → 返回上一层（不会再走下一层）',
        29: '恢复现场：把 `{c}` 还给 `left`，否则会误伤别的分支',
        'dfs(len(words) - 1, 0)': '从最后一个单词开始，得分 0',
        32: '搜完所有子集，最高得分 ==`{ret}`==',
    },
    cards=dict(
        one_liner='每个单词选或不选，选就扣字母，回来再还上',
        complexity='时间 `O(m+L·2^n)`，空间 `O(n+|Σ|)`',
        problem=['给单词表 `words`、字母表 `letters`、每个字母的得分 `score`',
                 '每个字母最多用一次，每个单词最多用一次，求能拼出的最高总分',
                 '本视频：`["ax","xxz"]`，字母 `z a x x`，a=4, x=5, z=10 → 20'],
        quote='枚举 words[i] ==选或不选==：如果不选，那么得分不变；如果选，那么统计 words[i] 中的每个字母对应的分数之和，累加到得分 total 中。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先数好 `letters` 里每个字母的个数 `left`',
              '回溯三问：当前操作 = 选或不选；状态 = `(i, total)`；下一步 = `dfs(i-1, ...)`',
              '选的时候逐个字母扣 `left`，字母不够就撤销；递归回来要恢复现场'],
        result='搜完 4 个子集，最高得分 20',
        summary=['时间 `O(m+L·2^n)`，空间 `O(n+|Σ|)`，n ≤ 14 所以 2^n 可接受',
                 '易错：选了单词，递归返回后必须把 `left` 还回去（恢复现场）',
                 '`total` 是局部变量，不需要恢复',
                 '字母不足时要撤销已扣的字母再 return',
                 '题解另一种写法：把 `left` 当参数复制传递，`total` 改成返回值，代码更短'],
    ),
)
