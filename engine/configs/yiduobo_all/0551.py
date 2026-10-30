CONFIG = dict(
    num=551, title='学生出勤记录 I', difficulty='Easy', category='字符串',
    author='yiduobo', technique='一趟遍历计数',
    tags=[],
    code='''
class Solution(object):
    def checkRecord(self, s):

        absent = 0
        late = 0
        for char in s:
            if char == 'A':
                absent += 1
                if absent > 1:
                    return False
                late = 0
            elif char == 'L':
                late += 1
                if late > 2:
                    return False
            else:
                late = 0

        return True
''',
    call='Solution().checkRecord("PLLALLP")',
    expect=True,
    views=[
        dict(type='string', var='s', h=200, pointers={'i': 'blue'},
             color=lambda S, i, v: ('blue' if S.get('char') is not None and i == S.get('i') else None)),
        dict(type='text', size=30,
             fn=lambda S: f"缺勤 `absent` = =={S.get('absent', 0)}==（>1 就失败），连续迟到 `late` = =={S.get('late', 0)}==（>2 就失败）"),
    ],
    watch=[('char', 'char', 'blue'), ('absent', 'absent', 'pink'), ('late', 'late', 'orange')],
    captions={
        'for char in s': '看下一天：`char = {char!r}`',
        "if char == 'A'": '`char = {char!r}`，是缺勤吗？→ {char == "A"}',
        'absent += 1': '又缺勤一天：`absent` = =={absent}==',
        'if absent > 1': '缺勤 `{absent}` 天，超过 1 天了吗？{absent > 1}；超过就拿不到奖励',
        "elif char == 'L'": '不是 A，是迟到吗？→ {char == "L"}',
        'late += 1': '连续迟到一天：`late` = =={late}==',
        'if late > 2': '连续迟到 `{late}` 天，超过 2 天了吗？{late > 2}；连续 3 天就失败',
        11: '遇到缺勤也打断了连续迟到：`late = 0`，别漏了这一行',
        17: '这天是 P，不是迟到 → 连续迟到 ==清零==：`late = 0`',
        'return False': '条件被破坏，直接返回 ==False==',
        'return True': '整个记录扫完都没破坏条件 → 返回 ==True==',
    },
    cards=dict(
        one_liner='一趟遍历：数 A，同时数「连续」的 L',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['字符串 `s` 的每个字符：`A` 缺勤、`L` 迟到、`P` 到场',
                 '拿奖要求：==缺勤严格少于 2 天==，且==没有连续 3 天迟到==',
                 '返回能不能拿奖，示例 `"PPALLP"` → `true`'],
        quote='比较基础的题目，直接一趟遍历，统计A和连续出现的L的个数即可。',
        quote_src='—— yiduobo 题解',
        idea=['`absent` 记总缺勤数，到第 2 个 A 立刻返回 False',
              '`late` 记当前连续迟到数：遇到 L 加一，遇到 A 或 P ==清零==',
              '`late` 一旦超过 2，说明出现了 LLL，返回 False'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：L 要「连续」，所以遇到 A 或 P 必须把 `late` 清零',
                 '遇到 A 也要清零 `late`，别只在 else 里清',
                 '对比：灵神用 `count` 和子串判断一行搞定，这里是手写计数'],
    ),
)
