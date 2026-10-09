# `large-publication-architect` — GDKP v1.1.0 实施设计

> - 状态：v1.1.0 实施基线
> - 目标版本：GDKP v1.1.0
> - 工作名称：`large-publication-architect`
> - 本文范围：记录新增 Skill、现有 Skills 协作边界、持久化状态与验收要求

## 1. 本轮调整结论

上一版以 `TextbookBlueprint` 为中心的设计不再采用。

它把问题理解成“每个 Framework node 缺少更详细的写作合同”，因而继续增加 `KnowledgePointPlan`、`ChapterContract`、`ContinuityLedger` 和审计回执。这会强化当前已经存在的错误倾向：先把知识拆成大量节点，再要求每个节点分别拥有标题、段落和完成状态。

实际问题不是规范不足，而是**知识颗粒度与出版颗粒度被错误地一一对应**：

```text
Framework node ≠ 教学主题 ≠ 正文段落 ≠ 可见标题
```

一个 Framework node 只是内部覆盖与追踪单元，不必成为一个 Notion 小标题，更不必独占一段正文。多个相关节点应当先合并成一个有中心问题的教学主题，再由若干连续段落共同讲清。只有读者面对的主题真正发生变化时，才需要新的标题。

因此，新 Skill 的核心能力调整为：

> 将覆盖完整但过度切碎的 Framework，重新聚合为少量语义完整的教学主题，并指导 Notion Author 用连续正文讲清定义、机制、作用和知识联系。

## 2. 两张截图暴露的真实问题

### 2.1 大规模计算：并行原语被写成并列知识卡片

截图中的“map、reduce 与 scan”和“直方图、排序与冲突控制”在目录上是两个完整小节，覆盖内容也基本齐全，但正文之间没有形成教学关系。

它们并不一定是两个互不相关的主题。更自然的主线是：

```text
独立元素变换
  → 有依赖的聚合与前缀传播
  → 多个线程写入共享目标
  → 冲突、私有化与合并
  → 在流压缩、分桶或基数排序中继续使用这些原语
```

`map`、`reduce`、`scan` 说明数据依赖如何从“无跨元素依赖”逐步变成“需要同步的聚合”；直方图、流压缩、分桶和基数排序可以把这种依赖落实到共享写入、热点、冲突控制或前缀偏移。对于比较排序等不依赖这条机制的内容，则应重新判断它是否属于同一中心问题，不能为了追求连续而强行合并。

正确方向不是为两个标题分别补更多正文，而是先判断它们是否应被聚合到同一教学主题中，例如“从独立变换到共享状态冲突”。正文可以分成数个自然段，但这些段落必须沿同一个问题连续推进。

### 2.2 深度学习：一条机制链被编号标题切断

截图中的“图把对象与关系同时作为输入”和“消息传递先汇总邻居，再更新节点”本来是一条连续机制：

```text
图如何表示对象和关系
  → 节点编号不应改变语义
  → 网络需要置换等变或不变的计算
  → 聚合邻居并更新节点
```

如果把“图对象”“置换性质”“邻居聚合”“节点更新”分别变成编号小节，宏观目录看起来更丰富，但每个标题下只有少量实际内容。删除这些小标题后，真正的知识量并没有增加，反而暴露出正文只是把一条机制拆开陈列。

正确方向是把它们写成一个连续主题，例如“图表示如何导出消息传递”。只有进入表达能力、过平滑、几何等变性或图级读出等真正改变中心问题的内容时，才考虑新建小节。

### 2.3 根因

当前流程隐含采用了以下错误投影：

```text
一个 KnowledgeNode
  → 一个可见小标题
  → 一段独立正文
  → 一个已完成状态
```

这能让覆盖率、章节数和发布状态显得完整，却会产生三类副作用：

- 同一主题被拆成互不连接的短段落；
- 标题数量增长快于实际知识量；
- 作者不断重新介绍上下文，正文无法形成教材式的连续解释。

新增 Skill 必须打破这种一一映射，而不是进一步规范它。

### 2.4 流程级问题：出版与练习被混成同一条推进链

在“大规模计算”案例的早期，流程在形成第一阶段实践后，以“完成练习并交回复核，才进入下一实验”的方式结束，之后需要用户再次要求“练习先跳过，直接生成后面的所有章节”。在后续系统重构要求中，用户又进一步明确提出约 12 部、80–120 个实质知识节点，并再次声明“练习暂不作为推进条件”。

这不是单个练习设计错误，而是两个阶段没有彻底分离：

- **教材构建：**确定全书章节与知识点，完成证据、正文和一次发布；
- **学习验收：**通过练习、实验、问答或迁移任务验证读者是否掌握。

生成完整教材不等于读者已经掌握，但读者尚未完成练习也不能阻止剩余教材继续生成。除非用户明确选择“学完一章再解锁下一章”的交互式课程模式，否则练习必须位于完整出版之后，或作为不阻塞出版的独立支线。

该案例还说明，仅有“12 部、108 个节点均已发布”并不能证明用户给出的详细知识点真正进入了正文。标题和节点可能全部存在，但作者实际收到的仍是稀疏标题列表或通用写作模板。新增 Skill 必须先生成一份覆盖全书的“章节—知识点”内容总图，把同一份完整总图作为用户可查看的主要设计结果和 Author 的实际输入。

## 3. Skill 身份

### 3.1 名称

- Skill name：`large-publication-architect`
- UI display name：`GDKP-Large Publication Architect`
- 中文定位：大规模教材叙事架构师

### 3.2 实现 description

```yaml
description: Produce or revise a complete full-book chapter-to-knowledge map for very large textbooks and monographs, grouping related knowledge into coherent teaching topics without compressing local depth. Use for explicitly 100k+ publications, multi-unit books, broad weak-foundation learning goals, or user-requested revisions of drafts that are incomplete, shallow, or disconnected; do not audit written Notion prose, define domain coverage, admit evidence, publish content, or route the workflow.
```

这里的 `architect` 指教材的语义组织与讲解主线，不是为每个知识节点建立固定 schema。

## 4. 何时触发

本节判定已经通过，本轮保持原触发方向。

### 4.1 强触发条件

满足任意一项即可进入大规模教材架构流程：

- 用户明确要求约 10 万字以上的教材、专著或系统性学习材料；
- 全书无法在一次可靠的写作与审计过程中完成，必须拆成多个 publication units；
- 用户已经反馈成品“像知识点总结”“小主题不完整”或“章节串不起来”；
- 现有框架虽然通过覆盖审计，但仍需整体重建教学顺序或深度分配。

### 4.2 组合触发信号

没有明确字数时，可将以下信号组合判断，而不把任何单一数字当成绝对定义：

- 约 12 个以上章节；
- 约 60 个以上需要正文承载的 KnowledgeNodes；
- 预计拆分为 4 个以上写作或发布单元；
- 覆盖 broad field map 或 reference-comprehensive 范围；
- 学习者基础薄弱，但大量主题要求达到 understanding 或 mastery；
- 跨章节先修、符号、方法组合与回引关系明显密集。

这些数字只是路由信号，不是质量标准。一个 8 章但依赖关系极密集的理论专著可能需要本 Skill；一个 20 章但每章相互独立的参考手册则未必需要完整的连续叙事模式。

### 4.3 不触发场景

- 单一问题、短教程、局部章节或明确限定的小主题；
- 只要求概览而不要求形成可连续学习的教材；
- 章节天然独立、用户明确要求词条式参考手册；
- 仍未确认领域边界或尚未通过必要的 coverage audit。

普通场景继续使用 GDKP v1.1.0 的轻量路径，避免为小任务引入不必要的规划成本。

## 5. 五种颗粒度必须分离

| 层次 | 实际用途 | 是否直接成为 Notion 标题 |
|---|---|---|
| Framework node | 内部覆盖、来源、关系与追踪单元 | 否 |
| 教学主题 | 围绕一个中心问题组织的连续知识 | 通常对应一个章节或自然小节 |
| DraftPacket | 一次模型调用及其 checkpoint 对应的隐藏生成与恢复分片 | 否 |
| 正文段落 | 完成定义、解释、推导、例子、作用或过渡 | 否 |
| 可见标题 | 帮助读者识别真正的主题转换 | 仅在需要导航时使用 |

默认关系应是：

```text
多个相关 Framework nodes
  → 一个教学主题
  → 一个或多个隐藏 DraftPackets
  → 若干互相承接的正文段落
  → 按阅读需要决定是否设置标题
```

同时保留反向可能：一个高度复杂的 Framework node 也可以展开为多个教学主题或 DraftPackets。DraftPacket 的数量只随可靠生成、验收和恢复需要变化，不增加读者可见标题；关键不在数量，而在读者是否面对了新的问题、对象或推理阶段。

以下做法必须避免：

- 根据 node 数量决定章节或小标题数量；
- 为了让每个 node “有位置”而创建短小独立段落；
- 把关系写在内部 RelationRegistry 中，却不在正文中解释；
- 用编号标题代替段落之间的因果、递进、对比或应用联系；
- 把 publication-unit 的技术切分直接暴露成读者可见结构。
- 把 runtime compaction 后的对话摘要当作 DraftPacket checkpoint 或已验收正文。

## 6. 首要产物：全书“章节—知识点”总图

新增 Skill 的第一产物不是规则清单，而是用户和 Author 都能直接阅读的**全书章节—知识点总图**，工作名称为 `FullBookChapterKnowledgeMap`。

对于新教材，它必须在任何 Notion 正文开始前覆盖已经确认的全部章节与全部实质知识点；对于既有教材，则应先从全书快照重建完整版本，再开始成批修订。其格式可以是 Markdown、大纲或其他自然可读形式，不要求固定 schema；关键是读者能够一次看到“整本书准备讲什么”，Author 能够直接据此完成全部正文。

总图应当对用户可见，但默认不是新的逐章审批门。除非用户明确要求“先确认全书总图再写正文”，Architect 完成总图后应由 Orchestrator 自动继续来源和 Notion 流程。

### 6.1 什么才算实质知识点

知识点不能只是一个名词或标题。它应当表达作者究竟需要讲清什么，例如：

- 较弱：`scan`；
- 有效：`scan 为每个位置保留前缀聚合状态；需解释 inclusive/exclusive 语义、上扫与下扫依赖、work/span，并连接到流压缩、分桶和基数排序中的偏移计算。`

一个实质知识点通常会说明概念、机制或关系中的至少一项，并在必要时指出公式、推导、例子、适用边界或应用方向。它是内容承诺，不是新的可见小标题。

### 6.2 总图应当让用户和 Author 看见什么

每章至少要让人读懂：

- 这一章解决的中心问题；
- 本章实际包含哪些有内容的知识点，而不是多少个标题；
- 哪些知识点应当合并成连续主题，它们为什么相连；
- 它们按什么顺序展开，前后章如何承接；
- 合并后还缺少哪些机制、推导、例子、边界或应用联系。

这些不是要求逐项填写的表单字段。可以按部分、章节或主题簇自然书写，但不能只交付章节名称，也不能用 Framework node ID 替代自然语言知识点。

### 6.3 用户提出的详细知识点不得在下游消失

Architect 必须综合当前确认范围内的用户原话、需求重建结果、Framework、结构性来源与已识别缺口。每个用户明确要求的重要知识点都必须出现以下一种结果：

- 作为独立实质知识点保留；
- 与相邻知识合并，但其具体内容仍在合并后的知识点描述中可见；
- 因范围冲突或证据限制无法纳入，并明确返回原 owner 处理。

不能因为合并小标题、压缩目录、切换 publication unit 或使用通用写作模板而静默删除。内部可以保留来源锚点和 Framework refs 以便追踪，但用户和 Author 看到的总图应当是自然语言内容，而不是机器 ID 清单。

为了真正发现静默遗漏，实现层需要保留一条隐藏的最小追踪关系：

```text
knowledge_point_key
  → 用户原话或需求锚点
  → 总图中的章节与教学主题
  → DraftPacket 与预定 Notion 页面
  → 已调度、已完成或受治理的例外状态
```

该关系可以并入现有 `PublicationCoverageIndex`，不单独创建一套知识点合同。多个知识点可以进入同一段连续正文，一个知识点也可以跨数段展开；它不生成可见标题，也不要求用户填写或审批。该索引是写作前和调度中的轻量追踪，不要求在发布后重新读取 Notion 正文逐项制作内容见证。

### 6.4 “一次性输出全部”的含义

Architect 的一次任务以**完整全书总图**为原子交付物：

- 不得只生成第一章、第一部或一个示例后返回 `ready`；
- 不得要求用户回复“继续”才生成剩余章节；
- 不得在章节总图尚未完成时切换到练习或学习验收；
- 如果上下文容量要求内部分批，可以自行保存中间结果并继续，但对用户和 Author 的正式输出必须是合并后的完整全书版本；
- 只有真实的范围歧义、必要的来源授权、外部能力阻塞或用户明确要求暂停，才允许中止。

“一次性”描述的是用户可见的完整结果与自动连续执行，不要求底层模型在单个上下文窗口中完成所有推理。

### 6.5 大规模计算示意

一个合格章节不应只列出 `map`、`reduce`、`scan`、`直方图` 和 `排序`。它可以在同一章中形成以下知识点主线：

- map 的元素独立性如何允许无同步并行，以及内存访问如何决定实际吞吐；
- reduce 如何引入树形依赖，为什么总工作量与关键路径必须分开分析；
- scan 如何保留中间前缀状态，上扫/下扫和 inclusive/exclusive 的差异是什么；
- 直方图为何把独立读取变成共享目标写入，热点分布如何导致原子冲突；
- 私有化、分层合并和内存占用之间如何权衡；
- scan 如何继续服务流压缩、分桶和基数排序，而比较排序是否属于同一主线需要另行判断。

这些知识点可以被写成少量连续段落，不需要逐条变成标题。

### 6.6 图深度学习示意

同样，图深度学习章节的总图不应只列 `图对象` 和 `消息传递`，而应说明：

- 节点、边和全局属性如何构成模型输入，节点编号为什么不应成为语义；
- 置换等变与图级置换不变分别约束什么输出；
- 邻居消息、聚合与节点更新如何组成一层通用消息传递；
- 聚合算子的选择如何影响可区分的信息与数值行为；
- 多层传播如何扩大感受野，并自然导向过平滑、表达能力或几何约束等后续问题。

这里的知识点数量来自真实讲解内容，而不是通过增加编号小节制造。

## 7. 如何决定合并还是拆分

### 7.1 倾向合并

出现以下情况时，相关知识点通常属于同一个教学主题：

- 它们共同回答同一个中心问题；
- 后一个概念是前一个概念的机制、结果、约束或应用；
- 它们位于同一比较轴或同一方法谱系；
- 其中一个脱离另一个就难以解释“为什么”；
- 分开写会重复背景、定义或前提；
- 相邻标题删除后，只需增加自然过渡就能形成连续正文。

### 7.2 倾向拆分

只有出现真实的阅读边界时才拆分：

- 中心问题、研究对象或抽象层级发生明显变化；
- 后续内容需要一组新的先修知识；
- 内容足够深入，读者确实需要导航和回查入口；
- 后续是可以独立阅读的专题、分支或附录；
- 合并后会形成难以阅读的超长段落或混合多个不相干论证。

### 7.3 三个编辑测试

1. **删标题测试：**删除两个相邻标题后，如果正文可以通过一两句因果、递进或对比过渡自然连接，应优先合并。
2. **薄标题测试：**如果一个标题下只有定义、一个公式或一小段说明，它通常不是独立主题。
3. **合并后知识密度测试：**如果多个标题合并后只剩很少实际知识，不能靠恢复标题掩盖；应补充机制、解释、例子和联系，或诚实缩减目录。

这些是编辑判断，不是确定性 validator，也不产生固定的标题数量。

## 8. 正文的默认段落逻辑

对大多数解释性段落，Notion 正文应优先采用：

```text
定义 + 解释 + 作用/联系
```

- **定义：**当前语境中的概念是什么，与相近概念有何区别；
- **解释：**它为何成立、如何工作，必要时加入机制、公式或例子；
- **作用/联系：**它解决什么问题，怎样连接前文、后文或同主题中的其他知识点。

这三个部分是段落的逻辑，不是三个可见小标题，也不是必须各写一句的固定模板。它们可以出现在一个完整段落中，也可以形成两三个紧密相连的段落。

例如，不应只写：

> scan 输出所有前缀结果，并具有线性工作量和对数跨度。

更完整的写法应沿以下逻辑自然展开：

> scan 为序列中每个位置产生其前缀聚合结果，因此它保留了 reduce 会丢失的中间状态。并行实现需要在树形上扫与下扫阶段之间维持依赖，这解释了它为何能够保持线性总工作量，却仍需要对数级同步层次。也正因为 scan 暴露了所有前缀状态，它可以继续支撑流压缩、分桶和基数排序，而不只是作为一个孤立原语存在。

推导、例题、比较、实验、历史背景和过渡段可以采用适合自身目的的结构。要求是大多数核心解释不能停在“定义 + 结论”，也不能为了符合模板而重复相同的作用描述。

## 9. 一次完成全书设计，再自动完成全部正文

Architect 必须先把完整 `FullBookChapterKnowledgeMap` 返回 `knowledge-product-orchestrator`。Orchestrator 以该完整版本为 canonical 内容计划，自动调度全部 Notion Author 批次；Architect 不直接调用或调度下游 Skill。

超大主题的正文仍可因为上下文或 connector 限制而内部分批。`DraftPacket` 是一次模型调用能够可靠完成的隐藏生成与恢复分片，publication unit 是写作、Zotero 审计或 connector 层面的技术批次；两者都不直接决定读者可见的标题结构：

- 第一章或第一批写入成功后必须自动继续，不得增加内容回读门；
- 不得把“第一章成功”当作本轮完成，也不得要求用户回复“继续”；
- 完整总图必须持久化且不可截断；每个 DraftPacket 只加载全局叙事主线、当前局部知识义务、必要证据、相邻正文上下文，以及相关术语和符号，避免总图本身挤占正文推理空间；
- 一个批次可以同时消化多个 Framework nodes，不要求逐 node 交付正文；
- 全部章节的知识义务在写作前已经分配到完整 DraftPacket 队列；不得在调度或写作时静默删除；
- 用户反馈触发的补写只在事实表述变化时重新进入 DraftClaimSet 提取与 Zotero claim audit，然后直接发布一次；自然语言编辑仅在用户明确要求润色或反馈指向文风时运行。

大规模场景的全局一致性主要通过以下方式维持：

- 每章具有清晰的主问题，并可包含若干支持性子问题，但不把 node 列表当目录；
- 前一章的结论成为后一章的起点；
- 重复出现的概念承担深化或迁移作用，而不是重新定义；
- 跨批次写作时以完整总图为 canonical 状态，并传递当前切片、上一段实际正文和下一步意图，而不只传递标题列表；
- 在每个 DraftPacket 生成时处理相邻衔接，避免由生产批次产生人工边界；
- 全书队列未完成、知识义务仍待处理、Zotero claim audit 未通过或发布写入尚未成功时，流程不能转入学习验收。

### 9.1 两层上下文管理与恢复

大规模教材不能把“模型当前还记得什么”当作执行状态。最稳妥的上下文架构是两层并用：

1. **Runtime compaction：**管理持续变长的 Codex 对话，使控制线程在压缩历史后仍能继续推理和调度；
2. **DraftPacket + 外部 checkpoint：**主动隔离每个知识主题或论证阶段，并把已验收内容、状态和恢复信息持久化到模型上下文之外。

两层承担不同职责，不能互相替代：

```text
runtime context = 可替换的工作缓存
external checkpoint = canonical 恢复事实源
```

Runtime compaction 可以保存当前目标、主要决策和下一步摘要，但它不是正文仓库，也不能证明某个知识点已经写完。自动压缩、Agent 重启或上下文切换之后，Orchestrator 必须从外部 checkpoint 重新装载当前 canonical 总图版本、DraftPacket 队列、已验收正文和下一项工作，而不是依靠压缩摘要重新回忆或重写内容。

外部 checkpoint 应进入 Project Kernel 管理的持久化机器状态或其引用的版本化 artifact，而不是只存在于聊天摘要、临时提示词或某个 Agent 的局部上下文中；它不进入读者可见的 Notion 正文。

每个 DraftPacket 的最小 checkpoint 至少应保留：

- 所绑定的总图、需求和证据 revision；
- 当前 Packet 的知识义务、状态及下一 Packet 标识；
- 已接受正文的精确内容或稳定页面目的地与落地状态；
- 已完成的 Zotero claim audit 与发布操作状态；
- 为下一 Packet 提供的术语、符号、上一段结论和下一步意图等连续性信息。

恢复时必须遵守以下不变量：

- compaction 摘要不能把 `pending` 或 `drafting` 推进为 `accepted`；
- 已验收正文不能仅存在于对话历史或模型记忆中；
- checkpoint 或绑定 revision 不一致时，相关 Zotero 审计和发布状态立即失效，并从最后一个持久化 checkpoint 恢复；
- 上下文不足只触发保存 checkpoint、拆分 DraftPacket 或内部续跑，不能触发概览式压缩、静默省略或向用户询问“是否继续”；
- 已验收 Packet 在后续装配中按持久化正文恢复，不能由全书摘要重新生成。

因此，runtime compaction 解决“长对话还能继续”，DraftPacket 与外部 checkpoint 解决“知识内容不会依赖长对话而存在”。即使自动压缩发生，规模增长也只会增加 Packet 数量和恢复次数，不会降低已经冻结的局部知识深度。

### 9.2 练习默认不是出版门

大规模教材构建默认采用 `exercise_gate: false`：

- 不以“完成本章练习”解锁下一章；
- 不因读者尚未提交实验、问答或学习单而暂停剩余正文；
- 不在全书章节—知识点总图或 Notion 正文未完成时，把主流程交给 `outcome-orchestrator`；
- 教材全部发布后，可以继续生成练习并验证掌握度，但“教材完成”和“个人掌握”必须分别报告；
- 只有用户明确要求交互式课程、分章解锁或边学边写时，练习才可以影响后续发布顺序。

### 9.3 审计预算：保留三种非重复控制

大规模出版最昂贵的无效循环来自发布后重新加载整本 Notion、逐项做第二次语义判断，再读取 Obsidian 文件、链接和图谱设置进行第三次确认。该流程会重复消费大段正文上下文，却无法稳定替代用户对实际阅读表面的判断。v1.1.0 因此从架构层取消这些常规审计。

Matrix 教材回放也证明，完全取消独立语义判断会丢掉一部分真实收益：首轮检查发现了秩与最大非零子式的机制边界、对偶范数与优化界的联系、全局投影与局部 Fréchet 线性化的区别、谱隙稳定性和 vec–Kronecker 推导等实质缺口；但第二轮主要只是确认已知修订，没有持续发现新的问题类型。因此保留首轮价值，删除递归复审。

v1.1.0 只保留三种相互独立的控制：宽领域 Framework 的确定性 coverage audit；Zotero 的来源准入与最终事实声明审计；每个连贯大规模 publication unit 在最终 claim 提取前接受一次 Architect `DraftQualityReview`。第三类只读取本地 canonical draft 与分配给它的知识义务，检查缺失机制、推导、边界、应用和必讲关系。它可以触发一次局部修订或证据路由，但修订稿不再交给 Architect 复审。

引用出版不增加第四轮模型审计。参考 v1.0 的编号引用、完整 References 和可点击原始链接要求，v1.1.0 在 Zotero claim audit 之后增加本地确定性的 `CitationProjection` 编译门：把内部 Zotero/source 身份映射为连续编号，生成与正文闭合的 References，并在写入前拒绝内部 ID 泄露、缺失或孤立编号、来源映射漂移和缺少已声明链接。它只读取局部 canonical draft 与机器状态，不调用模型，也不回读 Notion。

通过上述流程后，Notion 只写入一次并记录原生页面 ID 或 URL；Obsidian 只按 GraphPlan 写入一次并记录操作结果。两者均不为审计目的重新读取内容。Connector 返回错误、目标身份缺失、受管理文件冲突或用户指出具体内容问题时，流程执行定向修订；若修订改变事实表述，则重新进入 Zotero claim audit；若仅改变编号、链接或参考文献排版，只重建 CitationProjection。

## 10. 与 Notion Author 的职责边界

v1.1.0 已按以下边界同步调整 `notion-node-author`；正文所有权仍不转移给 Architect。

| 职责 | `large-publication-architect` | `notion-node-author` |
|---|---|---|
| 全书章节—知识点总图 | 在写作前一次性生成完整版本，并保留用户明确要求的知识内容 | 绑定同一份 canonical 总图；每个 DraftPacket 接收局部完整知识义务和必要全局上下文 |
| Framework nodes 的覆盖追踪 | 使用现有映射，不改变领域范围 | 在写作前将知识义务分配到 DraftPacket 与预定页面 |
| 哪些知识点合并讲解 | 决定主题聚合与叙事顺序 | 按聚合结果写成连续正文 |
| 可见章节和小标题 | 提出保留、合并或删除建议 | 决定最终自然标题并写入 Notion |
| 定义、解释与作用/联系 | 指明哪些关系必须在正文中讲清 | 完成实际段落、公式、例子和过渡 |
| 知识义务调度与单轮检查 | 在总图中完整保留并聚合每项义务；对每个连贯本地 draft 检查一次实质落实，不参与发布后检查 | 按 PublicationCoverageIndex 完成全部 Packet；对发现项执行一次局部修订或路由；事实表述通过 Zotero claim audit 后发布一次 |
| 事实与引用 | 不新增事实，不准入来源 | 只使用已准入 EvidencePack，并维护 DraftClaimSet |
| Notion connector | 不直接调用 | 独占写入与发布；记录成功结果，不启动发布后内容回读审计 |

### 10.1 Notion Author 在 v1.1.0 中的行为

在大规模教材分支中，Notion Author 应当：

- 在第一章开始前绑定当前完整 `FullBookChapterKnowledgeMap`，并以完成全书为本轮目标；每个 DraftPacket 使用当前局部完整知识义务而不是截断版全书清单；
- 把 Framework refs 当作不可见的覆盖清单，不把它们逐一变成标题；
- 以总图中的教学主题和实质知识点为正文组织依据；
- 允许一个段落或一组连续段落同时完成多个相关知识点；
- 让大多数解释性段落遵循“定义 + 解释 + 作用/联系”；
- 用正文写出因果、递进、对比与应用关系，而不是依赖页面链接或相邻标题；
- 只有中心问题、推理阶段发生变化，或长内容确实需要导航时才创建新标题；
- 发布前执行薄标题检查与相邻小节合并检查；
- 如果合并后暴露出实际知识不足，应补写解释或缩减目录，不能恢复碎标题来维持数量；
- 技术上可以分批写入，但成功完成第一批后必须自动继续其余章节；
- 在写作前和每个 Packet 完成时更新隐藏追踪关系，确保总图中的每项知识义务均进入已完成 Packet 或受治理例外；
- 每个连贯大规模 publication unit 在最终 claim 提取前接受一次 DraftQualityReview；发现项只修订一次，不进入 Architect 复审循环；
- 提取最终 DraftClaimSet 并交给 Zotero 审计；通过后发布一次，记录页面身份和写入结果，不重新加载正文做第二轮审计。

这不意味着：

- 整章不得使用小标题；
- 所有内容必须合成一个超长段落；
- 不相关知识也要强行串联；
- 每段必须机械写成三句话；
- 为了流畅而遗漏 Framework 已确认的范围；
- Architect 可以越权改写或发布 Notion 正文。

### 10.2 与其他现有 Skills 的边界

- `knowledge-framework` 继续负责“领域中必须包含什么”，但其 node 边界不得被视为出版边界；
- `zotero-source-gate` 继续负责来源和事实正确性；
- `notion-natural-prose-editor` 继续处理自然表达，但不能代替主题聚合和章节重组；
- `knowledge-product-orchestrator` 继续作为唯一控制平面；
- `outcome-orchestrator` 继续负责练习和掌握度验证，但只能在完整出版之后接管主流程，除非用户明确选择交互式课程模式；
- Obsidian 精简方案保持独立，不属于本 Skill。

## 11. 两种使用方式

### 11.1 新教材：写作前聚合

读取当前确认范围中的完整用户要求、已经通过覆盖审查的 Framework 和结构性缺口，一次性形成全书 `FullBookChapterKnowledgeMap`。在正式交付前，Architect 自行完成所有章节、全局去重、前后关系和知识缺口检查；不能把第一章样例作为正式结果。

总图完成后，Architect 将其返回 Orchestrator，由 Orchestrator 自动调度 Notion Author 完成各个连贯 publication unit。每个 unit 在最终 claim 提取前，由 Architect 对本地 canonical draft 做一次 bounded DraftQualityReview，判断分配给它的机制、推导、例子、边界、应用和必讲关系是否出现实质缺口。Author 对发现项只执行一次局部修订；修订稿直接进入 Zotero claim audit，不再交给 Architect 复审。通过后发布并继续下一单元。

### 11.2 既有教材：碎片化修订

接收由 Notion Author 或 Orchestrator 提供的**全书**正文快照、原始用户要求及内部 Framework 映射，先反向建立完整章节—知识点对照，再识别：

- 可以合并的相邻标题；
- 被标题切断的机制链；
- 只有定义、没有解释或作用的薄段落；
- 多处重复背景但没有新增理解的内容；
- 需要补写关系后才能自然合并的知识点；
- 用户明确提出、总图已经包含，但正文中没有实际解释的知识点。

返回面向 Orchestrator 的 `NarrativeRevisionMemo`，说明应合并什么、缺少哪段联系、哪些内容需要真正扩写；由 Orchestrator 路由给相应 owner。该 memo 是编辑建议，不是新的审计回执。

如果问题来自领域漏项或事实证据不足，分别返回 Framework 或 Zotero owner；Architect 不在本地修补其他 Skill 的 artifact。

## 12. 本 Skill 不采用的设计

首版不引入以下内容：

- 每个 node 一份 `KnowledgePointPlan`；
- 每章固定字段的 `ChapterContract`；
- 要求逐项打勾的 `ContinuityLedger`；
- `BlueprintAuditReceipt` 或 `DraftCoherenceReceipt`；
- 用脚本判断段落是否“足够像教材”；
- 固定章节数、标题数、段落数或逐节点字数；
- 将“定义 + 解释 + 作用/联系”暴露为正文小标题；
- 只生成第一章或第一批后等待用户回复“继续”；
- 用读者练习、实验或掌握度验证阻塞剩余章节；
- 以“标题存在”代替知识点已经进入正文。
- 发布后重新加载整本 Notion 做语义、样式、公式、引用或层级审计；
- 写入 Obsidian 后重新读取笔记、链接、节点数、边数或图谱设置进行复审。

这些机制会让实现重新围绕合规状态优化，并重复消耗大段上下文，而不是围绕实际阅读体验优化。v1.1.0 依靠完整总图、不可丢失的 Packet 义务、单轮 DraftQualityReview、Zotero 来源审计、真实案例回放和用户对实际阅读表面的反馈。

这里不排斥并入现有 `PublicationCoverageIndex` 的最小知识点调度。该索引连接用户要求、总图、DraftPacket 和预定页面，并在发布前防止义务静默消失。它不规定可见结构或每个知识点的写法，也不要求发布后回读，因此不同于逐 node 合同和审计表单。

DraftPacket checkpoint 同样不是新的读者结构或逐知识点写作合同。它只保存恢复所需的 canonical revision、队列状态、已验收正文和连续性信息，防止 runtime compaction 把模型记忆误当成项目状态。

篇幅仍可作为异常信号：10 万字目标明显只生成数万字时，说明内容不足；但篇幅不能决定应该拆出多少标题，也不能证明解释已经完整。

## 13. 质量判断

整本大规模教材首先应当满足：

- 写作开始前已经生成完整的章节—知识点总图，而不是只有第一章；
- 用户明确提出的知识范围在总图中均有去向，不因合并标题而丢失；
- Author 始终绑定同一份 canonical 完整总图，并在每个 DraftPacket 接收当前局部完整知识义务和必要全局上下文；
- runtime compaction 只承担对话续航，已验收正文与执行状态均可从 DraftPacket checkpoint 精确恢复；
- 每个知识点和必讲关系均已分配到完成的 DraftPacket 或受治理例外；每个连贯 unit 已完成一次 DraftQualityReview 且发现项已修订一次或受治理；最终事实表述具有当前 Zotero claim audit，全部 publication units 均有成功写入结果；
- 练习完成状态不会改变教材剩余章节的生成与发布。

其中每一章还应当满足：

- 读者能够说出这一章持续解决的中心问题；
- 相邻知识点通过机制、因果、对比或应用关系连接，而不是并排陈列；
- 标题数量反映真实主题转换，而不是内部 node 数量；
- 删除小标题后，正文仍能形成自然的论述顺序；
- 合并小节不会暴露出“很多标题、很少知识”的空心结构；
- 大多数核心段落不只给定义，还解释其含义并说明作用或联系；
- 公式、例子和实现细节嵌入解释主线，而不是独立堆放；
- 覆盖映射仍可在内部追踪，但读者看不到机器结构。

不使用统一量化阈值替代这些判断。章节可以很长或很短，小标题也可以多或少，前提是每个边界都对阅读有真实价值。

## 14. v1.1.0 实现影响面

v1.1.0 已按轻量结构实现新增 Skill：

```text
.agents/
└── skills/
    └── large-publication-architect/
        ├── SKILL.md
        └── agents/openai.yaml
```

初版原本不增加 Skill 私有 reference、validator 或 schema；但真实重建失败已经证明，仅靠文字合同无法阻止“先生成正文，再从标题反推总图、Packet、审查和完成收据”。因此本轮增加一个共享的 `large-publication-state-contract.md` 和一个最小前向状态验证器。它们只验证顺序、hash、owner、execution separation、义务调度和完成状态，不用字数、标题或关键词判断正文质量。

本次已同步修改的协作面包括：

- `knowledge-framework/SKILL.md`：明确 Framework node 与可见章节不是一一关系；
- `intent-source-analysis` 与 `requirement-reconstruction`：保留用户明确给出的详细主题和知识要求，使其能进入全书总图；
- `notion-node-author/SKILL.md`：要求先绑定 canonical 完整总图、按 DraftPacket 接收局部完整知识义务，再自动完成全部 publication units，并增加 checkpoint、按教学主题聚合写作、默认段落逻辑、知识点对照和发布前合并检查；
- `notion-node-template.md`：明确多数解释段落采用“定义 + 解释 + 作用/联系”，但禁止机械栏目化；
- `knowledge-product-orchestrator/SKILL.md`：只在已确认的大规模分支插入 Architect；持久化 DraftPacket 队列与 checkpoint，在 runtime compaction 后从 canonical 状态恢复；全书总图与正文未完成前，不把主流程切换到练习；对技术批次自动续跑；
- `large-publication-state-contract.md` 与 `validate_large_publication_state.py`：把“总图先于正文、Packet 逐包 checkpoint、Author/Architect execution 分离、claim audit 先于发布、完整全书门禁”变成必须前向通过的状态转换；每个 prospective gate 先持久化不可变 state snapshot，再输出绑定 snapshot hash、Packet/unit selector 与前一 receipt hash 的链式收据，完成门会重新装载历史 snapshot 并复验，晚期状态不能重放早期 gate；
- `validate_claim_audit.py`：在传入 EvidencePack 时重算 canonical checksum，并校验 EvidenceUnit 的具体来源身份、结构化 passage/table/figure 等 locator、支持的精确 claim IDs、支持范围、内容 fingerprint、可访问与冲突状态以及逐 claim 的 `support_assessment`，拒绝通用章级 EvidenceUnit；
- `outcome-orchestrator/SKILL.md`：默认不得用练习结果作为后续教材内容的解锁条件；
- bundle manifest 与公开文档：升级到 v1.1.0 与 14 个核心 Skills。

`FullBookChapterKnowledgeMap` 与 `NarrativeRevisionMemo` 仍保持自然语言产物，不注册为复杂内容 schema。新增结构只约束执行状态，因为真实案例已经暴露出稳定的时序伪造风险：地图、checkpoint、审查和完成状态可以在正文之后一次性补造。该状态合同不规定教材标题、段落或固定字数。

## 15. 验收场景

### 场景 A：大规模计算

- 在任何 Notion 写入前，一次性生成覆盖全部 12 部的章节—知识点总图；
- 用户明确给出的计算机系统、OpenMP、CUDA、MPI、HPC 存储与调度、分布式一致性与事务、云网络/Kubernetes/数据工程，以及地理空间与遥感计算主题均有自然语言知识点落点；
- 不再把 map、reduce、scan、直方图、排序和冲突控制逐项投影成正文标题；
- 能识别“数据依赖如何改变同步与冲突”这一共同主线；
- 修订结果明确指出哪些标题应合并，以及中间缺少哪段机制联系；
- 合并后的正文实际增加理解深度，而不是只删除标题；
- 第一章或第一批写入成功后自动继续全部章节，练习状态不参与出版推进；
- 总图中的每一项实质知识义务均预先分配到 DraftPacket，不能以 108 个标题均存在代替完整内容调度。

### 场景 B：图深度学习

- 能识别“图表示 → 置换性质 → 邻居聚合 → 节点更新”是一条连续机制；
- 不用 22.1、22.2 等编号制造虚假的知识数量；
- 只有进入表达能力、过平滑、几何约束或其他新问题时才建议分节；
- 合并后的核心解释整体体现必要的定义、解释和作用/联系；推导、例题和过渡段仍按各自功能组织。

### 场景 C：普通小主题

- 不触发本 Skill；
- 不增加全书总图或修订步骤；
- 保持现有短路径。

### 场景 D：练习与出版分离

- 教材构建到第一章后生成练习，但剩余章节尚未完成：失败；
- 要求用户完成练习或回复“继续”才写下一章：失败；
- 内部分批完成所有章节并获得全部写入成功结果，然后将练习作为独立学习阶段启动：通过；
- 用户明确选择“学完一章再解锁下一章”的交互模式：允许按其选择执行。

### 场景 E：上下文压缩与恢复

- 长对话发生 runtime compaction 后，从外部 checkpoint 装载准确的总图 revision、DraftPacket 队列和已验收正文，并自动继续下一 Packet：通过；
- 只根据 compaction 摘要重新生成已经验收的正文：失败；
- 已验收正文只存在于模型记忆，没有持久化内容、位置或 hash：失败；
- checkpoint 与正文 revision 不一致却继续沿用旧完成状态：失败；
- 上下文不足时保存 checkpoint 并进一步拆分 Packet，而不是缩短知识内容：通过。

### 场景 F：审计裁剪与定向修订

- 连贯大规模 unit 的本地 canonical draft 在 claim 提取前接受一次 Architect 语义检查：必须；
- 该检查发现缺失机制或关系后，由 Author 修订一次并直接进入 Zotero；再次交给 Architect 复审：禁止；
- Zotero 对来源准入和最终事实声明完成精确审计：必须；
- Notion 成功写入后，为检查语义、公式、引用数量或层级而重新加载整页：禁止；
- Obsidian 成功写入后，为核对节点、边、Wikilink 或 Graph 设置而重新读取 Vault：禁止；
- Connector 返回写入错误、目标身份缺失或文件冲突：定向处理，不启动全量内容审计；
- 用户指出某段过浅、断裂或图谱含有无效节点：定向修订；若事实表述变化，重新执行 Zotero claim audit 后再写入。

### 场景 G：前向状态与反伪造门禁

- 在第一段正文之后从现有标题反推 `FullBookChapterKnowledgeMap`：失败；
- 一次 Author execution 生成多个 DraftPackets，随后批量补 checkpoint：失败；
- 上一依赖 Packet 尚未 checkpoint 和 accepted 就调度下一 Packet：失败；
- Author 与 Architect 使用相同 execution ID，或脚本用标题数、字符数、正则和固定空 findings 生成 `passed`：失败；
- ClaimAuditReceipt 只匹配 claim/evidence ID，但 EvidenceUnit 没有具体来源身份、locator、support scope 或 content fingerprint：失败；
- 修改 EvidencePack locator 或 support scope 后沿用旧 checksum：失败；
- 在 Packet 已 accepted 或 unit 已 published 后补跑早期 prospective gate：失败；
- receipt chain 形式正确但 `validated_state_sha256` 找不到匹配的历史 snapshot：失败；
- 全部前向 gate 已在相应调度前通过，所有最终 draft hash 均与 Zotero receipt 和 Notion publication operation 一致：通过。

## 16. Definition of Done

`large-publication-architect` 的首版完成标准是：

1. 能在一个不中途等待用户续写的架构阶段中，输出完整全书章节—知识点总图；
2. 用户明确提出的详细知识要求不会在 Framework、总图和 Notion Author 之间静默丢失；
3. 能稳定识别 Framework node、教学主题、段落和标题之间的颗粒度差异；
4. 能把同一机制链上的多个 nodes 聚合成有中心问题的教学主题；
5. 能解释为什么合并或拆分，而不是套用固定数量规则；
6. 能指导 Notion Author 写出“定义 + 解释 + 作用/联系”的连续正文，并把每项总图义务预先分配到 DraftPacket；
7. Notion 可以内部分批，但必须自动完成全部章节，第一章不是停止点；
8. runtime compaction 后可以从 DraftPacket checkpoint 恢复准确正文与执行状态，不依赖模型记忆重建；
9. 练习与掌握度验证默认不阻塞教材构建；
10. 最小内部追踪能够证明用户要求、总图知识点、必讲关系、DraftPacket 与预定页面之间没有调度断裂；
11. 宽领域覆盖审计、单轮大规模 draft 语义检查和 Zotero 来源审计各自只承担不同职责；Notion 和 Obsidian 成功写入后不启动内容回读复审；
12. 用户反馈触发的事实性补写会重新完成 Zotero claim audit 后发布；纯文风修订不触发无关审计；
13. 只新增最小前向状态合同，不新增字数配额、标题配额、逐 node 写作合同或 Notion/Obsidian 回读审计；
14. 两个真实案例回放能够给出符合本 README 的全书总图、合并和扩写建议；
15. 不越过 Framework、Zotero、Notion Author 和 Orchestrator 的所有权。

## 17. 推荐决策

- 保留 `large-publication-architect` 名称与已经通过的触发条件；
- 撤回 `TextbookBlueprint` 与 `TextbookNarrativePlan` 作为核心产物，改用自然可读的 `FullBookChapterKnowledgeMap`；
- 将“一次性输出完整全书章节—知识点”设为第一职责，将语义聚合作为组织这些知识点的方法；
- 允许多个 Framework nodes 合并为一个教学主题和一组连续段落；
- 把“定义 + 解释 + 作用/联系”设为大多数解释性段落的默认逻辑，而不是可见模板；
- Notion Author 负责实际正文、标题、引用和一次发布；它绑定 canonical 完整总图，按 DraftPacket 接收局部知识义务，并自动完成所有技术批次；
- runtime compaction 与 DraftPacket checkpoint 两层并用；对话摘要只用于续航，外部 checkpoint 才是恢复正文和执行状态的事实源；
- PublicationCoverageIndex 在写作前把每项知识义务映射到 DraftPacket 与预定页面，不要求 Architect 在发布后重新读取正文；
- 每个连贯大规模 unit 在发布前只接受一次 DraftQualityReview；发现项允许一次修订，不进行 Architect 二审；
- 默认 `exercise_gate: false`，完整出版与个人掌握分别推进和报告；
- v1.1.0 不开发用字数、标题或关键词判断连贯性的 validator；新增的前向状态 validator 只检查总图冻结、Packet 调度与 checkpoint 时序、Author/Architect execution 分离、单轮 DraftQualityReview 状态、locator-specific Zotero claim audit、draft hash 和写入结果；
- Notion 与 Obsidian 的常规发布后审计全部取消，用户反馈成为定向修订入口。
