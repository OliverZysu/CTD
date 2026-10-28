# 期刊推荐与参考文献核验备忘录

核验日期：2026-10-06。用途：支持 CTD 化合物—疾病关联项目的英文期刊论文写作与投稿材料准备。本备忘录没有实施投稿，没有运行新的模型实验，也不把未来系统功能视为已完成成果。

## 1. 推荐结论

**首选 Journal of Cheminformatics，按 Research 类研究稿准备。** 建议把研究定位为化合物—疾病关联预测与证据审查，结合可复现的模型比较、数据语义分析和文献溯源。其官方范围明确包括化学信息系统、软件、数据库和数据挖掘。将研究对象从污染物扩展到一般化合物也更符合这一定位。

这一推荐是研究主题与读者群的匹配判断，不代表当前材料已经达到接收标准。现有工作主要采用已发表的图学习模型；不能包装成新的 GNN 架构。已有预测和系统原型可组织成完整研究初稿，但投稿前需要补齐数据版本、标签语义、独立评估和可公开复现材料。现阶段不宜把稿件定位为已验证的新致病关系发现，也不宜把规划中的基因异质图、Acemap 集成写成已经完成的系统贡献。

| 优先级 | 期刊 | 与本项目的匹配判断 | 成为有竞争力稿件所需的贡献 | 官方核验情况 |
|---|---|---|---|---|
| 1 | Journal of Cheminformatics | 化合物信息组织、图模型、关联预测与证据追溯匹配 | 可复现、具有化学信息学意义的研究；严格对照和明确新增认识。若改投 Software/Database，需真实可用且维护的公开资源 | 范围与通用投稿指南通过官方页面的第三方文本渲染读取；文章类型细则未成功获得 |
| 2 | Bioinformatics | 若后续强化方法学，或形成有广泛用途的软件工具，可作为备选 | 清楚的方法增量或工具价值，针对生物信息问题的严格验证 | 本次官方页面及其文本渲染均遇到 403/验证页面；下述投稿细则不能视为已核验 |
| 3 | PLOS Computational Biology | 更适合有实质生物学新认识的后续研究 | 计算结果带来显著生物学认识；基因解释须得到适当对照支持。其官方说明不把湿实验作为所有论文的强制条件 | 范围与作者指南直接读取成功 |
| 4 | Patterns | 在形成可推广的数据/方法/研究流程时再考虑 | 可被其他研究领域复用的实质性数据科学贡献，而不是单一数据集上的现成模型展示 | Cell/ScienceDirect 官方页面及渲染均受访问验证限制；具体篇幅、图数、材料要求未核验 |

上述顺序用于当前这份材料。若后续出现强生物学发现，PLOS Computational Biology 的优先级可提高；若出现有充分实验支持的新算法，Bioinformatics 的优先级可提高。不能依据期刊名称中的 AI/数据科学倾向推断接收可能性。

## 2. 已核验的官方要求与访问限制

### Journal of Cheminformatics

官方范围：https://link.springer.com/journal/13321/aims-and-scope

官方通用指南：https://jcheminf.biomedcentral.com/submission-guidelines

本次直接访问返回 JavaScript client challenge，通过 `https://r.jina.ai/` 文本渲染读取到官方来源内容。该途径可核验所读取的文字，但不能独立保证文本渲染缓存的新鲜度；最终提交前仍应由作者打开官方页面复核可变细则。

读取到的范围包含：

> chemical information systems, software and databases, and method development for molecular modelling
>
> computer and molecular graphics, computer-aided molecular design, expert systems, QSAR, and data mining techniques

通用指南明确要求或说明：

- 正文使用双倍行距，带行号和页码。
- 提供可编辑的 Word、RTF 或 TeX/LaTeX 文件；LaTeX 相关源文件需要一并提供。PDF 可用于审阅，但不能代替全部可编辑源文件。
- 每篇稿件包含 `Availability of data and materials`。支持结论的数据应以机器可读形式提供，或存入适当仓库；具体强制范围由文章类型说明和相关数据政策决定。
- 对软件，披露项目主页、存档版本 DOI/持久标识符、操作系统、语言、依赖、许可证和使用限制。
- 图表按文中顺序引用；图注放在稿件中；网络资源引用应包含完整 URL 和访问日期。
- 指南列出的文章类型包括 Research、Database、Methodology、Brief Report、Software、Data Note 等。

**未核验项：**Research 类型的两个路径均返回期刊首页，未获得该类型的完整格式说明，因此本备忘录不宣称其当前摘要字数限制或强制摘要结构。费用、税费、折扣、开放专刊截止日期均不作为本次决策依据，也不报价。应避免把其他 BMC 期刊的常见格式直接称为本刊当前要求。

### PLOS Computational Biology

官方范围：https://journals.plos.org/ploscompbiol/s/journal-information

官方投稿指南：https://journals.plos.org/ploscompbiol/s/submission-guidelines

以上两页直接读取成功。范围强调对生命系统的实质性新认识，包括 AI/机器学习应用；Methods/Software 稿件也要求重要的新能力与生物学价值。原文明确：

> Inclusion of experimental validation is not required for publication, but should be referenced where possible.

作者指南说明初投可用包含正文和图的单一 PDF；英文正文、双倍行距、单栏、连续行号和页码；摘要不超过 300 词，Research 文章另需 150–200 词非技术性 Author Summary；正文没有统一字数、图数上限。直接支持论文结论的作者代码须公开，除具体法律或伦理限制外不得设置访问限制，并在数据可用性声明中给出位置。期刊强烈建议持久归档与可引用的版本标识。

这些是 PLOS 的已核验要求，**不应套用为 Journal of Cheminformatics 的强制格式**。

### Bioinformatics 与 Patterns

Bioinformatics 官方范围入口：https://academic.oup.com/bioinformatics/pages/about

Bioinformatics 作者指南：https://academic.oup.com/bioinformatics/pages/general_instructions

Patterns 范围入口：https://www.sciencedirect.com/journal/patterns/about/aims-and-scope

Patterns 作者入口：https://www.cell.com/patterns/authors

本次直连返回 403，文本渲染也返回安全验证页面。已记录访问限制；未核验具体文章类型限制、摘要长度、费用或 STAR Methods 等要求。表中对两刊的建议是投稿定位判断，而不是对其当前政策的逐条认证。

## 3. 本项目投稿前的证据准备重点

以下为针对本项目的研究质量建议，与上面的已核验期刊要求分开列出。

1. **明确任务定义。** 区分化合物—疾病关联、治疗关联、标志物/机制关联、推断关联和暴露风险；CTD 中有记录不等于化合物在人体中致病。未收录配对通常是未知关系，不能自动当作经实验证明的真阴性。
2. **固定数据与标签。** 保存原始 CTD 数据版本/下载日期、文件摘要、预处理、ID 映射、排除准则、划分列表和随机种子。数据库更新论文的出版年不能替代实际使用的数据快照日期。
3. **完成可复现比较。** 在相同数据和划分下比较现有基线，检查消息传递图是否包含测试标签信息；给出多次运行的不确定性、PR 类指标和适当的简单对照。LAGCN/MRDDA 若未实际运行，只能做设计比较，不能宣称性能胜过它们。
4. **保存逐候选证据。** 错误预测表需明确真实标签、预测类别和分数所属类别。文献命中率应有确定的候选集合、检索日期、检索式、人工判读标准、匹配对照和去重逻辑；不能把检索到文献直接称为独立实验验证。
5. **避免循环验证。** 若某篇文献已用于构建 CTD 训练边，重新检索到该文献不能作为独立发现证据。基因路径也应有频度/度分布匹配的空模型，不能仅凭存在共同基因宣称机制成立。
6. **区分已完成与规划。** 扩大化合物数据库、Acemap 跳转、基因异质图、候选关系文献证据展示，应分别列明实施状态。现有材料中出现字段或界面需求不等于相关模块已部署、已评价。
7. **提供真实的可用性声明。** 本地共享盘路径不等于公开研究仓库；没有实际建立的 GitHub/Zenodo 地址或 DOI 不能填入稿件。对受许可约束的数据可提供获取步骤、版本标识、处理代码与允许再分发的派生结果。

## 4. 已核验参考文献及使用边界

文献元数据见 `verified_reference_metadata.json`。医学文献补充摘要见 `prior_work_europepmc.json`。Crossref 记录可将长标题拆成 title/subtitle，引用时已合并。年按正式会议或期刊卷期标注；预印本和在线优先年份可能更早。

| 建议键 | 可直接使用的书目信息与稳定入口 | 能支持的论述与限制 |
|---|---|---|
| Davis2025CTD | Davis AP, Wiegers TC, Sciaky D, et al. **Comparative Toxicogenomics Database's 20th anniversary: update 2025.** Nucleic Acids Research. 2025;53(D1):D1328–D1334. [doi:10.1093/nar/gkae883](https://doi.org/10.1093/nar/gkae883) | CTD 的文献人工整理、多种生物实体和环境健康用途；不能把该文的全库规模当成本项目训练集规模。存在更正 `10.1093/nar/gkae1185`；更正全文说明仅纠正标题大小写，不涉及数据/方法变化。不要误把更正当原始数据库论文。 |
| Davis2023CTD | Davis AP, Wiegers TC, Johnson RJ, Sciaky D, Wiegers J, Mattingly CJ. **Comparative Toxicogenomics Database (CTD): update 2023.** Nucleic Acids Research. 2023;51(D1):D1257–D1262. [doi:10.1093/nar/gkac833](https://doi.org/10.1093/nar/gkac833) | 支持 CTD 整合化合物、基因、表型、解剖、疾病和暴露内容，以及基于已整理知识产生可检验假说。CTD Tetramers 已提供化合物—基因—表型—疾病连接，因此“加入基因路径”本身不能表述为前所未有。 |
| Kuhn2016SIDER | Kuhn M, Letunic I, Jensen LJ, Bork P. **The SIDER database of drugs and side effects.** Nucleic Acids Research. 2016;44(D1):D1075–D1079. [doi:10.1093/nar/gkv1075](https://doi.org/10.1093/nar/gkv1075) | 支持药物不良反应数据库的来源和用途。SIDER 是药物/副作用资料，不能不加区分地作为环境污染致病风险金标准，也不能把不良反应等同治疗适应证。 |
| Hamilton2017GraphSAGE | Hamilton WL, Ying R, Leskovec J. **Inductive Representation Learning on Large Graphs.** Advances in Neural Information Processing Systems 30. 2017. [arXiv:1706.02216](https://arxiv.org/abs/1706.02216) | 支持 GraphSAGE 邻域采样与聚合。原论文支持基于节点特征的归纳学习，但本项目使用可训练节点 ID embedding 时，不能仅因使用 SAGEConv 就宣称验证了全新化合物/疾病的归纳泛化。 |
| Velickovic2018GAT | Veličković P, Cucurull G, Casanova A, Romero A, Liò P, Bengio Y. **Graph Attention Networks.** ICLR. 2018. [arXiv:1710.10903](https://arxiv.org/abs/1710.10903) | 支持 GAT 的邻域自注意力机制；注意力权重不是自动成立的生物机制解释。预印本发表于 2017 年。 |
| Kipf2017GCN | Kipf TN, Welling M. **Semi-Supervised Classification with Graph Convolutional Networks.** ICLR. 2017. [arXiv:1609.02907](https://arxiv.org/abs/1609.02907) | 支持 GCN 方法来源；原始任务主要为半监督节点分类，本项目的边解码器和关联预测设置需另外说明。预印本发表于 2016 年。 |
| He2020LightGCN | He X, Deng K, Wang X, Li Y, Zhang Y, Wang M. **LightGCN: Simplifying and Powering Graph Convolution Network for Recommendation.** SIGIR. 2020:639–648. [doi:10.1145/3397271.3401063](https://doi.org/10.1145/3397271.3401063); [arXiv:2002.02126](https://arxiv.org/abs/2002.02126) | 支持去除特征变换与非线性的简化邻域传播模型；原文是协同过滤，作为化合物—疾病模型时属于任务迁移/基线改写，不是原文已验证的毒理预测。 |
| Grover2016node2vec | Grover A, Leskovec J. **node2vec: Scalable Feature Learning for Networks.** KDD. 2016:855–864. [doi:10.1145/2939672.2939754](https://doi.org/10.1145/2939672.2939754); [arXiv:1607.00653](https://arxiv.org/abs/1607.00653) | 支持有偏随机游走和网络表示学习。边预测组合方式、分类器及训练图的构造仍是本项目设置。 |
| Tan2016AceMap | Tan Z, Liu C, Mao Y, Guo Y, Shen J, Wang X. **AceMap: A Novel Approach towards Displaying Relationship among Academic Literatures.** Proceedings of the 25th International Conference Companion on World Wide Web. 2016:437–442. [doi:10.1145/2872518.2890514](https://doi.org/10.1145/2872518.2890514) | 支持 AceMap 学术文献关系展示平台的来源；书目由 Crossref 核验。本次没有读取该论文全文，也没有核实当前 Acemap 的 API/单篇论文深链接契约；不能作为本项目已完成整合或准确召回证据的证明。 |
| Yu2021LAGCN | Yu Z, Huang F, Zhao X, Xiao W, Zhang W. **Predicting drug–disease associations through layer attention graph convolutional network.** Briefings in Bioinformatics. 2021;22(4):bbaa243. [doi:10.1093/bib/bbaa243](https://doi.org/10.1093/bib/bbaa243); [PMID:33078832](https://pubmed.ncbi.nlm.nih.gov/33078832/) | 已从 Crossref 与 Europe PMC 摘要核验：合并已知药物—疾病关联、药物相似度和疾病相似度，通过层间注意力整合 GCN 表征。是直接相关工作，可说明异质图与层注意力已有先例；不能跨数据集直接比较文中 AUROC/AUPRC。在线优先发表于 2020 年。 |
| Chen2025MRDDA | Chen C, Zhou Y, Li Y, Xu J, Li D, Wang L. **MRDDA: a multi-relational graph neural network for drug–disease association prediction.** Journal of Translational Medicine. 2025;23:753. [doi:10.1186/s12967-025-06783-x](https://doi.org/10.1186/s12967-025-06783-x); [PMID:40629423](https://pubmed.ncbi.nlm.nih.gov/40629423/); [PMC12235901](https://pmc.ncbi.nlm.nih.gov/articles/PMC12235901/) | 已从 Crossref 与 Europe PMC 摘要核验：多关系药物重定位，局部/全局图卷积、元路径和层注意力；摘要报告三个基准数据集及对接分析。支持相关方法比较，但对接并非疾病疗效或人群因果关系的实验证实。本次未复现其模型。 |

### 可供正文改写的相关工作句子

> Graph-based drug–disease association prediction has an established methodological foundation. LAGCN integrates known associations with drug and disease similarities and combines representations from different graph-convolution layers using attention. MRDDA extends this direction with multi-relational representations, meta-path information and layer-wise attention. These studies motivate comparison with disease-association methods beyond generic graph encoders. The present use of established graph-learning baselines should therefore be distinguished from the introduction of a new neural architecture.

若没有按同一数据与划分运行这两项方法，建议在讨论中直接承认缺少面向疾病关联任务的专用方法比较，并避免“state of the art”或“superior to existing approaches”。

## 5. Acemap、PubMed 与 DOI 跳转的可用性边界

当前 `https://acemap.info/` 可直接访问并显示 Acemap 学术检索平台。可以引用上述 2016 年原始平台论文，但当前服务的功能不能全部用该早期论文担保。

用于论文/系统准备的可行做法是保留 PMID 和 DOI，并提供标准 PubMed、DOI 跳转。Acemap 跳转应在确定其真实文献记录 ID 和可用链接后加入；本次没有验证可用的 Acemap 单篇论文 URL 模板，也没有把检索首页当作已匹配的目标论文。对每条候选关系应记录被引用文献、支持的具体命题、证据类型与检索时间，使“能跳转”与“文献支持该关系”分别可检查。

## 6. 可追溯证据文件

- `journal_guidance_retrieval.json`：官方 URL、直接/第三方读取方式、访问障碍和获取到的正文。注意其中两个 Research 路径是返回首页的失败尝试，不是有效文章类型细则。
- `verified_reference_metadata.json`：11 项原始文献的 Crossref/arXiv 元数据与核验 URL。
- `prior_work_crossref_search.json`：LAGCN、MRDDA、AceMap 的题名检索候选；只有与上述准确题名相符的记录被采用。
- `prior_work_europepmc.json`：LAGCN/MRDDA 摘要、PMID/PMCID 与 CTD 更正记录。
- `reference_additional_verification.json`：CTD 更正全文和图学习会议出处的补充核验（若某入口失败，保留具体错误）。

这些小型证明文件直接保存在个人 JuiceFS 共享目录；没有安装新环境、下载数据集或写入系统盘批量缓存。
