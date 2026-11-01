def _txt(S):
    if 'level' not in S:
        return '每层节点数 `2^(k-1)`，前 k 层共 `cnt_list[k-1] = 2^k - 1` 个'
    lv, pos = S['level'], S.get('pos')
    if pos is None:
        return f"label 在第 {lv + 1} 层（下标 `level = {lv}`）"
    kind = '偶数下标 → 从左往右' if lv % 2 == 0 else '奇数下标 → 从右往左'
    return f"当前 `level = {lv}`（{kind}），距行首/行尾的偏移 `pos = {pos}`"


CONFIG = dict(
    num=1104, title='二叉树寻路', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='逐层累计节点数 · 由位置倒推',
    tags=['灵神题单·链表树与回溯', '难度分 1545'],
    code='''
class Solution(object):
    def pathInZigZagTree(self, label):
        cnt_list = [1]
        while cnt_list[-1] < label:
            cnt_list.append(cnt_list[-1] + cnt_list[-1] + 1)
        
        res = []
        level = len(cnt_list) - 1
        if level % 2 == 0:
            if level == 0:
                pos = 1
            else:
                pos = label - cnt_list[-2] - 1
        else:
            pos = cnt_list[-1] - label

        while level > 0:
            if level % 2 == 0:
                res.append(cnt_list[level - 1] + 1 + pos)
            else:
                res.append(cnt_list[level] - pos)
            level -= 1
            pos //= 2
        
        res.append(1)
        res.reverse()
        return res
''',
    call='Solution().pathInZigZagTree(14)',
    expect=[1, 3, 4, 14],
    views=[
        dict(type='text', fn=_txt, size=28),
        dict(type='array', var='cnt_list', label='cnt_list（前 k 层的节点总数）', pointers={'level': 'blue'}, h=170),
        dict(type='array', var='res', label='res（从叶往根收集）', h=150, color=lambda S, i, v: 'green' if i == len(S['res']) - 1 else None),
    ],
    watch=[('label', 'label', 'blue'), ('level', 'level', 'pink'), ('pos', 'pos', 'yellow')],
    captions={
        'cnt_list.append': '前 k 层共 `2^k - 1` 个，下一层 = `2×上一个 + 1`：`cnt_list = {cnt_list}`',
        'level = len': '`cnt_list` 刚好盖住 label，所以 `label` 位于下标 `level = {level}` 这一层（根为 0）',
        'pos = label - cnt_list[-2] - 1': '偶数下标层从左往右标号：`pos = label - 上一层总数 - 1 = {pos}`，即从行首数起的偏移',
        'pos = cnt_list[-1] - label': '奇数下标层从右往左标号：`pos = 本层最大标号 - label = {pos}`，即从行尾数起的偏移',
        'pos = 1': '`level = 0` 就是根，偏移随便给个值',
        'res.append(cnt_list[level - 1] + 1': '偶数层从行首数 `pos`：标号 = `上一层总数 + 1 + pos` = =={res[-1]}==',
        'res.append(cnt_list[level] - pos': '奇数层从行尾数 `pos`：标号 = `本层最大标号 - pos` = =={res[-1]}==',
        'level -= 1': '往上走一层：`level` → {level}',
        'pos //= 2': '父节点在上一层的位置 = `pos // 2`：`pos` → {pos}',
        'res.append(1)': '根节点标号一定是 1，补上',
        'res.reverse': '收集时是从叶到根，反转成从根到叶：`{res}`',
    },
    cards=dict(
        one_liner='先算 label 在哪一层第几个，再按位置倒推父亲',
        complexity='时间 `O(log label)`，空间 `O(log label)`',
        problem=['无限满二叉树，奇数行从左到右、偶数行从右到左标号',
                 '给 `label`，返回从根到它的路径上的标号',
                 '示例：`label = 14` → `[1,3,4,14]`'],
        quote='由于这颗二叉树是满的，那么每一层节点的数量都可以很快计算出来，具体来说就是第k层中一个有2^(k - 1)个节点。',
        quote_src='—— yiduobo 题解',
        idea=['先用累计数 `cnt_list` 判断 label 在哪一层，再算出它在该层的第几个',
              '第 l 层第 p 个节点的父亲是第 l-1 层第 `p // 2` 个，不管标号怎么排',
              '最后按层数奇偶决定这个位置对应哪个标号，一路倒推回根'],
        result='运行结束，返回 `[1, 3, 4, 14]`',
        summary=['原文为 Python 2 写法，`pos /= 2` 已改为 `pos //= 2`（整数除法）',
                 '时间 `O(log label)`：层数只有 `log` 级；空间 `O(log label)`',
                 '易错：偶数下标层的偏移从行首数，奇数下标层从行尾数，别混',
                 '对照灵神：他直接用公式 `sum - label/2` 求父节点，这里是先定位置再换算'],
    ),
)
