CONFIG = dict(
    num=1189, title='“气球” 的最大数量', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='计数 · 取最小',
    code='''
class Solution:
    def maxNumberOfBalloons(self, text: str) -> int:
        cnt = Counter(text)
        return min(cnt['a'], cnt['b'], cnt['l'] // 2, cnt['n'], cnt['o'] // 2)
''',
    call='Solution().maxNumberOfBalloons("loonbalxballpoon")',
    expect=2,
    views=[
        dict(type='string', var='text', label='text', cell=60, h=170),
        dict(type='map', var='cnt', label='cnt（每个字母出现次数）', fmt=lambda k, v: f"'{k}': {v}", h=200, font=30),
        dict(type='text', h=130, size=30, fn=lambda S: (
            f"a:`{S['cnt']['a']}`  b:`{S['cnt']['b']}`  l:`{S['cnt']['l']}`÷2=`{S['cnt']['l']//2}`  n:`{S['cnt']['n']}`  o:`{S['cnt']['o']}`÷2=`{S['cnt']['o']//2}`"
            if 'cnt' in S else '')),
    ],
    watch=[],
    captions={
        'cnt = Counter': '统计 `text` 里每个字母的出现次数：`{dict(cnt)}`',
        'return min': 'a、b、n 各需 1 个，l、o 各需 2 个：`min({cnt["a"]}, {cnt["b"]}, {cnt["l"]}//2, {cnt["n"]}, {cnt["o"]}//2)` = ==`{ret}`==，最缺的字母决定个数',
    },
    cards=dict(
        one_liner='一个 balloon 要 1a 1b 2l 1n 2o，最缺的字母决定个数',
        complexity='时间 `O(n)`，空间 `O(|Σ|)`',
        problem=['用 `text` 里的字母拼尽可能多的 `"balloon"`，每个字母最多用一次',
                 '示例：`"loonbalxballpoon"` → `2`',
                 '`l`、`o` 在单词里各出现两次'],
        quote='1 个 balloon 需要消耗 2 个 o。所以如果有 5 个 o，则最多拼凑出 2 个 balloon。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每种字母单独算：能供出几个气球',
              'a、b、n 次数直接用；l、o 要 ==整除 2==',
              '木桶效应：五个数取最小值'],
        after=[dict(heading='举例：为什么取最小', lines=['`"loonbalxballpoon"`：a、b、n 各 2 个，l、o 各 4 个',
                    '按 1 个气球的需求：a 够 2 个，b 够 2 个，n 够 2 个',
                    'l 有 4 个，每个气球要 2 个 → 够 2 个；o 同理够 2 个',
                    '五个数都是 2，所以答案是 `2`；任何一个更小，答案就跟着变小'])],
        summary=['时间 `O(n)`，空间 `O(|Σ|)`',
                 '易错：`l`、`o` 要 `// 2`，别忘了向下取整',
                 'Counter 缺失的键返回 0，所以没出现的字母自然得到 0',
                 '与 2287 题相同，可推广到任意目标串'],
    ),
)
