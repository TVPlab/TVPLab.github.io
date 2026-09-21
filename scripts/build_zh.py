"""Regenerate the Chinese pages from the English HTML: python scripts/build_zh.py.
Official bibliography and personal names are deliberately preserved in English.
"""
from pathlib import Path
from html.parser import HTMLParser
from html import escape
import re
import json
ROOT=Path(__file__).resolve().parent.parent
EXACT={
'Research Associate':'研究人员',
'Research in adipose tissue biology at the TVPlab.':'在 TVPlab 开展脂肪组织生物学研究。',
'Skip to content':'跳转到正文','Menu':'菜单','About':'关于我们','Research':'研究方向','People':'团队成员','Publications':'研究论文','News & Events':'新闻与活动','Join Us':'加入我们','Contact':'联系我们',
'University of Cambridge · Institute of Metabolic Science':'剑桥大学 · 代谢科学研究所','The science of':'探索代谢科学，','metabolic health.':'守护生命健康。','TVPlab':'TVPlab','About TVPlab':'关于 TVPlab','Understanding how':'理解身体如何','the body uses energy.':'利用能量。','Meet our laboratory':'了解我们的实验室',
'Our research':'我们的研究','From adipose tissue':'从脂肪组织出发，','to metabolic disease.':'探索代谢疾病。','All research':'全部研究方向','Adipose tissue biology':'脂肪组织生物学','Explore this area':'了解研究方向','Lipotoxicity & organ health':'脂毒性与器官健康','Thermogenesis':'产热调控','Immunometabolism':'免疫代谢','From the laboratory':'实验室动态','News & events':'新闻与活动','All updates':'全部动态','Read update':'阅读动态',
'Institute of Metabolic Science':'代谢科学研究所','University of Cambridge':'剑桥大学','Addenbrooke’s Hospital, Cambridge CB2 0QQ':'英国剑桥 Addenbrooke’s 医院，CB2 0QQ','Contact the lab':'联系实验室','© 2026 TVPlab · University of Cambridge':'© 2026 TVPlab · 剑桥大学',
'Our People':'团队成员','Principal Investigator':'课题组负责人','Professor Antonio (Toni) Vidal-Puig':'Antonio（Toni）Vidal-Puig 教授','Professor Antonio Vidal-Puig':'Antonio Vidal-Puig 教授','View full profile →':'查看完整简介 →','Administration & Management':'行政与管理','Personal Assistant':'个人助理','Operations Scientific Management Lead':'实验室运营与科研管理负责人','Research Associates':'研究人员','Postdoctoral Research Associate':'博士后研究员','Assistant Research Professor':'助理研究教授','Research Assistants':'科研助理','Research Assistant':'科研助理','PhD Students':'博士研究生','PhD':'博士研究生','PhD · Lab Communication Director':'博士研究生 · 实验室传播负责人','Visiting Entrepreneur':'访问创业专家',
'Our Mission':'我们的使命','Understanding Energy Metabolism at the Molecular Level':'从分子层面理解能量代谢','Location & Facilities':'地点与科研设施','Institute of Metabolic Science, Cambridge':'剑桥大学代谢科学研究所','We are based at the':'我们的实验室隶属于','MRC Metabolic Diseases Unit':'英国医学研究理事会代谢疾病研究部（MRC MDU）',
'Find Us':'联系信息','Address':'地址','TVPlab':'TVPlab',"Addenbrooke's Hospital":"Addenbrooke’s 医院",'Hills Road':'Hills Road','Cambridge CB2 0QQ':'剑桥 CB2 0QQ','United Kingdom':'英国','Email':'电子邮箱','Phone':'电话','Open Positions':'招聘机会','Vacancies':'招聘信息','for current openings.':'页面了解现有职位。','Media Enquiries':'媒体咨询','Write to the lab':'给实验室写信','directly.':'直接联系。','Name':'姓名','Subject':'主题','Message':'留言','Open email draft':'打开邮件草稿',
'← Our People':'← 返回团队成员','Biography':'个人简介','Current Appointments':'现任职务','2009 – present':'2009年至今','Education & Qualifications':'教育背景与专业资格','Selected Awards & Honours':'部分奖项与荣誉','Google Scholar':'Google Scholar','Publications page':'研究论文页面','A full list of publications is available on the':'完整论文列表可见','and via':'，也可通过','and':'及','profile.':'页面。','h-index: 117 · Total citations: >48,500 (June 2025)':'h 指数：117 · 总引用次数：超过 48,500（截至2025年6月）',
'Our Research':'研究方向','Adipose Biology':'脂肪组织生物学','White fat · Energy storage · Obesity':'白色脂肪 · 能量储存 · 肥胖','White Adipose Tissue Expandability and Function':'白色脂肪组织的扩增能力与功能','Organ Dysfunction':'器官功能障碍','Liver · Heart · Beta cells':'肝脏 · 心脏 · 胰岛 β 细胞','Lipotoxicity in Peripheral Organs: Fatty Liver':'外周器官脂毒性与脂肪肝','Brown fat · Beige fat · UCP1':'棕色脂肪 · 米色脂肪 · UCP1','Brown Fat and Muscle Thermogenesis':'棕色脂肪与骨骼肌产热','Macrophages · Inflammation · Insulin resistance':'巨噬细胞 · 炎症 · 胰岛素抵抗','Macrophage Biology and Fibroinflammation':'巨噬细胞生物学与纤维炎症',
'Why Join TVPlab':'为什么加入我们','International Environment':'国际化科研环境','Cutting-Edge Science':'前沿科研平台','Career Development':'职业发展','Global Collaborations':'全球合作','Postdoctoral Positions':'博士后与研究岗位','Postdoctoral Research Associate — Brown Adipose Tissue Thermogenesis':'博士后研究员 — 棕色脂肪组织产热','Postdoctoral':'博士后','Full-time':'全职','3 Years':'3年','Open':'开放申请','Apply Now':'立即申请','Postdoctoral Research Associate — Adipose Tissue Immunology & Fibrosis':'博士后研究员 — 脂肪组织免疫与纤维化','2 Years':'2年','Senior Research Associate — Computational Metabolomics':'高级研究员 — 计算代谢组学','Senior Postdoctoral':'高级博士后','Closing Soon':'即将截止','PhD Opportunities':'博士招生','PhD Studentship — White Adipose Tissue Expandability and Lipotoxicity':'博士生项目 — 白色脂肪组织扩增能力与脂毒性','Fully Funded':'全额资助','4 Years':'4年','Enquire':'咨询项目','PhD Studentship — Single-Cell Genomics of Adipose Macrophages':'博士生项目 — 脂肪组织巨噬细胞的单细胞基因组学',
'New Paper Published in':'新论文发表于','Wellcome Trust Senior Investigator Award Renewed':'Wellcome Trust 高级研究员资助获续期','International Symposium on Adipose Biology — Cambridge':'脂肪生物学国际研讨会在剑桥举行',', revealing novel regulators of adipocyte plasticity.':'，揭示了调控脂肪细胞可塑性的新因子。','PhD Student Wins MRC Prize for Best Thesis':'博士生荣获 MRC 最佳博士论文奖','New Collaboration with Karolinska Institute Announced':'宣布与卡罗林斯卡医学院开展新合作','Prof. Vidal-Puig Delivers Keynote at EASD 2025':'Vidal-Puig 教授在 EASD 2025 作主旨报告',
'Professor of Molecular Nutrition & Metabolism · Fellow, Academy of Medical Sciences · MRC Investigator. Leads research at the MRC Metabolic Diseases Unit and Wellcome Sanger Institute, Cambridge.':'分子营养与代谢学教授 · 英国医学科学院院士 · MRC 研究员。在剑桥 MRC 代谢疾病研究部及 Wellcome Sanger 研究所领导科研工作。',
'Professor of Molecular Nutrition & Metabolism · Wellcome Trust Senior Investigator · Fellow, Academy of Medical Sciences':'分子营养与代谢学教授 · Wellcome Trust 高级研究员 · 英国医学科学院院士',
'Principal Investigator · Professor of Molecular Nutrition & Metabolism · Fellow, Academy of Medical Sciences':'课题组负责人 · 分子营养与代谢学教授 · 英国医学科学院院士',
'Professor of Molecular Nutrition and Metabolism, University of Cambridge':'剑桥大学分子营养与代谢学教授','Associate Director, MRC Metabolic Disease Unit (MDU)':'MRC 代谢疾病研究部副主任','MRC Investigator':'MRC 研究员','Lead, Cardiometabolic Medicine, Cambridge Heart and Lung Research Institute (HLRI)':'剑桥心肺研究所（HLRI）心脏代谢医学负责人',"Honorary Consultant in Metabolic Medicine, Addenbrooke's Hospital":'Addenbrooke’s 医院代谢医学荣誉顾问医师','Scientific Director, Cambridge Phenomics Centre':'剑桥表型组学中心科学主任','Principal Investigator, Principe Felipe Research Center (CIPF), Valencia':'瓦伦西亚菲利佩王子研究中心（CIPF）课题组负责人','Associate Research Scientist, Cambridge University Nanjing Centre of Technology and Innovation (CUNJC)':'剑桥大学南京科技创新中心（CUNJC）副研究员',
'M.D., Valencia University School of Medicine, Spain (Magna Cum Laude)':'西班牙瓦伦西亚大学医学院医学学位（优等荣誉）','Ph.D., Granada University School of Medicine, Spain':'西班牙格拉纳达大学医学院博士学位','Endocrinology, Metabolism & Nutrition Specialist, Spanish Ministry of Health':'西班牙卫生部内分泌、代谢与营养专科医师资格','Fellow, Royal College of Physicians (FRCP)':'英国皇家内科医师学会会士（FRCP）','Fellow, Academy of Medical Sciences (FMedSci)':'英国医学科学院院士（FMedSci）','Executive MBA, Judge Institute of Business School, University of Cambridge':'剑桥大学嘉治商学院高管工商管理硕士（EMBA）','Honorary Doctorate, Universidad Rey Juan Carlos, Madrid':'马德里胡安卡洛斯国王大学荣誉博士','Elected Member, Academia Europaea':'当选欧洲科学院院士','Paul Dudley White Fellowship Award, American Heart Association':'美国心脏协会 Paul Dudley White 研究员奖','Hippocrates International Award for Nutrition Research, Royal Academy of Medicine, Principado Asturias':'阿斯图里亚斯皇家医学院希波克拉底国际营养研究奖','ERC Advanced Grant':'欧洲研究理事会高级研究资助（ERC Advanced Grant）','Toh Chin Chye Visiting Professorship, National University of Singapore':'新加坡国立大学杜进才访问教授',
}
PREFIX={
'We are a biomedical research laboratory led':'我们是剑桥大学代谢科学研究所的生物医学实验室，由 Antonio Vidal-Puig 教授领导。',
'Our research explores the molecular mechanisms':'我们研究调控能量消耗和脂肪沉积的分子机制，探索机体如何在能量氧化利用与储存之间进行分配。',
'How fat tissue expands':'探索脂肪组织如何扩增并储存能量，以及超出其储存能力后发生的变化。',
'How excess lipids affect':'研究过量脂质如何影响肝脏、心脏等器官，以及肥胖与代谢疾病之间的联系。',
'The mechanisms controlling brown fat':'揭示棕色脂肪激活、骨骼肌产热及能量消耗的调控机制。',
'The role of macrophages, inflammation':'探索巨噬细胞、炎症和组织重塑在代谢健康中的作用。',
'Our laboratory brings together':'我们的团队汇聚分子生物学、生理学、生物信息学和临床医学研究者，共同探索代谢疾病的发生机制。',
'PA to Professor':'担任 Vidal-Puig 教授的个人助理，负责实验室行政事务与日程安排。',
'Oversees day-to-day':'负责实验室日常运营及科研协调工作。',
'Research focus: adipose tissue extracellular':'研究方向：脂肪组织细胞外基质重塑、纤维炎症及巨噬细胞生物学。',
'Research focus: brown adipose':'研究方向：棕色脂肪组织产热及线粒体解偶联机制。',
'Research focus: adipose tissue biology and metabolic':'研究方向：脂肪组织生物学与代谢调控。',
'Research focus: adipocyte metabolism':'研究方向：脂肪细胞代谢与全身能量稳态。',
'Research focus: computational':'研究方向：计算代谢组学及脂肪生物学项目中的多组学数据整合。',
'Research focus: adipose tissue immunology':'研究方向：脂肪组织免疫与代谢疾病。',
'Research focus: adipose tissue biology and molecular':'研究方向：脂肪组织生物学与肥胖的分子机制。',
'Laboratory research assistant supporting':'科研助理，支持脂肪生物学与代谢组学研究项目。',
'Laboratory research assistant.':'实验室科研助理。',
'PhD research in adipose tissue':'在 TVPlab开展脂肪组织生物学博士研究。',
'PhD research in metabolic disease':'在 TVPlab开展代谢疾病博士研究。',
'PhD research in adipose biology':'博士研究方向为脂肪生物学与免疫代谢。',
'PhD candidate at the TVPlab':'剑桥大学 TVPlab博士研究生，同时担任实验室全球传播负责人，协调国际科学传播与对外交流工作。',
'Dr Rodrigo Santos is':'Rodrigo Santos 博士担任 TVPlab访问创业专家，致力于发掘团队的商业化与科研转化机会。他在细胞生物学，以及面向生物技术和制药行业的创新细胞技术开发与应用方面拥有丰富经验。',
'Rodrigo is an Entrepreneur':'Rodrigo 是 Cambridge Innovation Capital（CIC）的驻点创业家。2026年加入 CIC 之前，他曾任 clock.bio 首席技术官，并曾在 Novo Holdings 担任驻点创业家、在 Mogrify 担任细胞技术总监、在 bit.bio 担任技术负责人，以及在 Horizon Discovery 担任首席科学家。',
'He actively contributes':'他参与多个科学顾问委员会和创业指导项目，积极支持科学共同体的发展。Rodrigo 于剑桥大学干细胞研究所获得博士学位。',
'The TVPlab investigates':'TVPlab位于剑桥大学代谢科学研究所，研究脂肪组织生物学、能量代谢及代谢疾病的分子与细胞机制。',
'Professor Antonio Vidal-Puig is':'Antonio Vidal-Puig 教授是剑桥大学分子营养与代谢学教授及 Wellcome Trust 高级研究员。他在剑桥 Addenbrooke’s 医院代谢科学研究所领导 TVPlab，并担任心肺研究所心脏代谢研究项目主任。',
'Professor Vidal-Puig received':'Vidal-Puig 教授在西班牙瓦伦西亚大学获得医学及博士学位，随后在哈佛医学院接受博士后训练。他于1999年加入剑桥大学，并建立了具有国际影响力的脂肪生物学与代谢疾病研究项目。',
'He has published more than':'他已发表300余篇同行评审论文，并获得多项荣誉，包括营养学 Rank Prize、表彰糖尿病与代谢研究贡献的 Novo Nordisk Prize，以及内分泌学会奖章。',
'The TVPlab is dedicated':'TVPlab致力于理解机体储存与消耗能量的基本分子和细胞机制。我们认为，深入认识脂肪组织生物学，是开发肥胖、2型糖尿病及相关心脏代谢疾病有效治疗方法的重要基础。',
'Our interdisciplinary team spans':'我们的跨学科团队包括分子生物学家、生理学家、生物信息学研究者和临床科学家，共同推动实验室发现向具有临床意义的认识转化。',
'We are proud to be part':'实验室隶属于剑桥大学代谢科学研究所。该研究所位于 Addenbrooke’s 医院，是欧洲重要的代谢疾病研究中心之一，依托英国 NHS 教学医院开展研究。',
'within the Institute of Metabolic Science':'，位于 Addenbrooke’s 医院内的代谢科学研究所。研究所汇聚临床与基础科研人员，推动对代谢及内分泌疾病的认识和治疗。',
'Our laboratory has access':'实验室可使用先进的成像、基因组学和代谢组学平台，并与 Wellcome Sanger 研究所、MRC 流行病学研究部及剑桥生物医学园区的临床科室保持密切联系。',
'We welcome enquiries from prospective collaborators':'欢迎有合作意向的研究人员、学生、博士后及媒体与我们联系。',
'We welcome enquiries from prospective PhD':'欢迎有意申请博士或博士后岗位的研究人员来信咨询，并附上个人简历及简要研究意向。请查看',
'For press and media enquiries':'媒体咨询请联系剑桥大学传播办公室。',
'Prepare your message below':'请在下方填写内容，然后在电子邮件应用中打开草稿，检查后自行发送。也可以通过邮箱',
'As Professor of Molecular Nutrition':'作为剑桥大学分子营养与代谢学教授，Vidal-Puig 教授在英国医学研究理事会代谢疾病研究部（MRC MDU）及 Wellcome Sanger 研究所领导科研工作。他还担任剑桥表型组学中心科学主任，专注于先进的小鼠代谢表型分析，并担任 Addenbrooke’s 医院代谢医学荣誉顾问医师。',
'The TVPlab explores':'TVPlab探索肥胖与胰岛素抵抗、糖尿病及心脏代谢并发症之间的分子联系，旨在发现新的治疗途径。Vidal-Puig 教授在西班牙瓦伦西亚接受医学教育，并在加入剑桥大学前于哈佛医学院开展博士后研究。',
'He is a Fellow of the Academy':'他是英国医学科学院院士（FMedSci）及英国皇家内科医师学会会士（FRCP），获得欧洲研究理事会高级研究资助，并曾获内分泌学会奖章及希波克拉底国际营养研究奖。2025年，他当选欧洲科学院院士。',
'Selected publications from the TVPlab (':'TVPlab部分研究论文（h 指数117，引用超过48,500次）。完整列表请参阅 Vidal-Puig 教授的',
'Our programme explores':'我们的研究探索调控能量消耗、脂肪沉积，以及能量在氧化利用和储存之间分配的分子机制。',
'How the expansion of adipose tissue':'我们研究脂肪组织扩增与代谢综合征发生之间的关系，探索决定白色脂肪组织（WAT）扩增能力的基因、信号通路及表观遗传调控机制，理解脂肪细胞如何安全地增大和增生，以及超出这一能力后为何会在肝脏、心脏和骨骼肌中出现异位脂质沉积。',
'Our central hypothesis is that adipose':'我们的核心假说是：推动肥胖相关心脏代谢并发症的关键在于脂肪组织功能失调，而不仅是脂肪量增加。理解扩增能力的限制因素及其恢复途径，是实验室的重要研究目标。',
'Whether lipotoxicity and/or':'我们探索脂毒性及脂肪因子分泌变化，是否会影响骨骼肌、心脏、肝脏、脑、胰岛 β 细胞和巨噬细胞等组织或细胞的胰岛素敏感性，重点研究脂质过载损伤肝脏（NAFLD／MASLD）、心脏（糖尿病性心肌病）及胰岛 β 细胞的分子机制。',
'We use mouse genetic models':'我们结合小鼠遗传模型、原代细胞培养及人类组织转化研究，解析从脂质过载到纤维化、细胞死亡和器官衰竭的脂毒性级联过程。',
'The molecular mechanisms that control':'我们研究控制能量消耗与棕色脂肪激活的分子机制。棕色脂肪组织（BAT）和米色脂肪可通过解偶联蛋白1（UCP1）等机制，将化学能以热量形式释放。相关研究还涉及骨骼肌中的钙离子与肌酸无效循环。',
'We explore the transcriptional':'我们探索产热过程的转录与翻译后调控、骨骼肌产热的贡献，以及激活棕色和米色脂肪作为肥胖与代谢综合征治疗策略的潜力。',
'Whether modifications in adipogenesis':'我们探索调节脂肪生成与脂肪组织重塑，能否改善肥胖相关的代谢异常。脂肪组织巨噬细胞（ATMs）是局部及全身代谢稳态的重要调控者。',
'During obesity, ATMs shift':'在肥胖状态下，脂肪组织巨噬细胞可由抗炎、组织重塑相关表型转向促炎状态，促进纤维化、细胞因子释放及全身胰岛素抵抗。我们结合单细胞基因组学、流式细胞术和小鼠体内模型，描绘其异质性，并寻找控制脂肪组织由代谢健康转向功能障碍的分子调控节点。',
'We are always interested':'我们欢迎积极投入科研的研究人员与我们交流。有意了解实验室机会，可发送咨询邮件至',
'Work alongside scientists from over':'与来自15个以上国家的科学家共同工作，融入多元、包容且拥有广泛国际合作的实验室。',
'Access state-of-the-art facilities':'使用代谢科学研究所、Wellcome Sanger 研究所及剑桥合作机构的先进科研设施。',
'Structured mentorship':'通过系统的导师指导和培训机会获得支持；实验室成员在学术界与产业界均有职业发展路径。',
'Opportunities for international exchange':'有机会与南京、瓦伦西亚、斯德哥尔摩等地的合作实验室开展国际交流访问。',
'We seek a highly motivated postdoctoral':'我们招聘积极投入科研的博士后，加入由欧洲研究理事会高级研究资助支持的产热研究项目。研究将结合小鼠模型、原代细胞培养及多组学方法，探索棕色脂肪与骨骼肌适应性产热的分子调控。申请者需具备脂肪生物学、代谢或细胞生物学背景；具有小鼠遗传学和转录组学经验者优先。',
'This position offers an exciting':'该岗位研究肥胖脂肪组织中由巨噬细胞驱动的纤维炎症。研究者将整合流式细胞术、单细胞测序及小鼠体内实验，解析慢性炎症、脂肪纤维化与全身胰岛素抵抗之间的联系。申请者需具备免疫学或细胞生物学经验。',
'A senior position for an experienced':'该高级岗位面向具备丰富计算分析经验的研究人员，负责脂肪生物学项目中的多组学数据整合。申请者需具备 R／Python、代谢组学及蛋白质组学分析流程的相关经验。',
'A fully-funded 4-year PhD':'该博士项目通过 MRC 代谢疾病研究部 DTP 培养计划提供四年全额资助，结合小鼠遗传学、脂肪细胞生物学及多组学方法，研究白色脂肪组织扩增的调控机制，以及扩增障碍引发外周器官脂毒性的后果。申请者须已获得或预计获得相关生物医学专业的一等或二等一级本科学位。',
'In collaboration with the Wellcome Sanger':'该博士项目与 Wellcome Sanger 研究所合作，利用单细胞与空间转录组学解析肥胖脂肪组织中巨噬细胞的异质性。学生将接受单细胞测序、生物信息学及小鼠体内模型训练。申请者宜对免疫学或计算生物学具有浓厚兴趣。',
'Latest updates from the TVPlab':'TVPlab最新动态：论文发表、奖项、合作及活动。',
'Our latest study on adipose tissue remodelling':'我们关于长期代谢应激下脂肪组织重塑的最新研究已被接收并发表于',
"The Wellcome Trust has renewed Professor":"Wellcome Trust 已续期支持 Vidal-Puig 教授的高级研究员资助，为未来五年的棕色脂肪组织产热及治疗策略研究提供支持。",
'The TVPlab co-hosted a two-day':'TVPlab在代谢科学研究所联合举办了为期两天的国际研讨会，邀请来自欧洲及亚洲的研究者共同交流。',
'Congratulations to Dr. Sophie':'祝贺 Sophie Clarke 博士！她关于肥胖脂肪组织中巨噬细胞极化的博士论文获得了 MRC 代谢科学最佳博士论文奖。',
'The TVPlab has announced':'TVPlab宣布与斯德哥尔摩卡罗林斯卡医学院开展新合作，利用 PET-CT 成像研究棕色脂肪在人类能量稳态中的作用。',
'Professor Vidal-Puig delivered':'Vidal-Puig 教授在欧洲糖尿病研究协会年度会议上作开幕主旨报告，探讨脂肪组织研究的未来方向。',
}
TITLES={'index':'TVPlab — 剑桥大学代谢科学研究','about':'关于我们 — TVPlab','research':'研究方向 — TVPlab','people':'团队成员 — TVPlab','publications':'研究论文 — TVPlab','news':'新闻与活动 — TVPlab','vacancies':'加入我们 — TVPlab','contact':'联系我们 — TVPlab','antonio-vidal-puig':'Antonio Vidal-Puig 教授 — TVPlab'}
ATTRS={'Main navigation':'主导航','TVPlab home':'TVPlab首页','Your name':'您的姓名','your@email.com':'您的电子邮箱','e.g. PhD enquiry, collaboration':'例如：博士项目咨询、科研合作','Your message…':'请输入您的留言……','The TVPlab team together in the laboratory':'TVPlab团队合照','Language':'语言'}
EXACT.update({
 'Swipe or use the arrows':'左右滑动，或点击箭头',
 'Adipocytes under the microscope':'显微镜下的脂肪细胞',
 'Through our lens':'镜头里的实验室','Life at TVPlab':'科研之外，同样精彩',
 'People, shared moments and a passion for discovery.':'记录相聚的时刻，也记录共同探索的热情。',
 'Our people':'我们的团队','Together in the laboratory':'相聚在实验室',
 'Beyond the bench':'实验之外','A moment together':'共享美好时光',
 'From our archive':'往日影像','The people behind the science':'科学背后的同行者',
 'View photograph':'查看照片','1 / 4':'1 / 4','1 / 3':'1 / 3','←':'←','→':'→'
})
ATTRS.update({
 'Previous slide':'上一项','Next slide':'下一项','Research areas':'研究方向',
 'Laboratory photo gallery':'实验室相册',
 'Fluorescence microscopy image of adipocytes':'脂肪细胞荧光显微图',
 'TVPlab members sharing a meal':'TVPlab成员聚餐',
 'Black-and-white team photograph from the TVPlab archive':'TVPlab早期团队黑白合照'
})
EXACT.update({'Meet our team':'认识我们的团队','View all':'全部成员','Administration':'行政管理','Researchers':'研究人员','Visitors':'访问成员','Read biography':'查看个人简介','Select a portrait to read more.':'点击人物照片，了解更多。','18 team members':'18 位团队成员'})
ATTRS.update({'Team directory':'团队成员名录','Filter by role':'按团队角色筛选'})
# Verified People summaries share one source with the English directory.
for person in json.loads((ROOT/'data/people-summaries.json').read_text()):
 for key in ['summary','bio']:
  if person[key]:EXACT[person[key]]=person[key+'_zh']
EXACT.update({'Close biography':'收起简介','View profile':'查看个人主页','Explore our research interests and backgrounds.':'了解团队的研究方向与专业背景。'})
ALLOWED={'TVP','lab','☰','↗','EN','中文','TVPlab','X / Twitter','Twitter / X','LinkedIn','Google Scholar','PubMed','Nature Metabolism','Hills Road','Katie Fisher','Mark Campbell','Martin Dale','Nazuk Gupta','Milidili Maimaiti','Ruoqi Du','Possawee Prasertsuk','Iman Mali','Cherub Kaida Wu','.'}
missing=set()
def translate(text):
 clean=' '.join(text.split())
 if not clean:return text
 if clean in EXACT:out=EXACT[clean]
 elif clean in TITLES.values():out=clean
 elif clean.startswith('Dr. '):out=clean[4:]+' 博士'
 elif re.match(r'^(January|February|March|July|September|November) \d{4}$',clean):
  m,y=clean.split();out=y+'年'+str({'January':1,'February':2,'March':3,'July':7,'September':9,'November':11}[m])+'月'
 else:
  out=next((v for k,v in PREFIX.items() if clean.startswith(k)),None)
  if out is None:
   out=clean
   if clean not in ALLOWED and not re.match(r'^[\d\s+():.,–-]+$',clean) and '@' not in clean:missing.add(clean)
 return (' ' if text[:1].isspace() else '')+out+(' ' if text[-1:].isspace() else '')
class Localize(HTMLParser):
 def __init__(self,name):super().__init__(convert_charrefs=True);self.name=name;self.out=[];self.pub_depth=0;self.title=False
 def tag(self,tag,attrs,closed=False):
  a=dict(attrs)
  if tag=='div' and 'pub-academic-entry' in a.get('class',''):self.pub_depth=1;a['lang']='en'
  elif tag=='div' and self.pub_depth:self.pub_depth+=1
  if tag=='html':a['lang']='zh-CN'
  if tag=='title':self.title=True
  for key in ['src','href']:
   val=a.get(key,'')
   if val.startswith(('images/','styles.css','refresh.css','site.js','people.css','people.js')):a[key]='../'+val
  if 'srcset' in a:a['srcset']=re.sub(r'(^|,\s*)images/',r'\1../images/',a['srcset'])
  if 'data-language' in a:
   a['href']=('../' if a['data-language']=='en' else '')+self.name
   if a['data-language']=='zh':a['aria-current']='true'
   else:a.pop('aria-current',None)
  if tag=='link' and a.get('rel')=='alternate':a['href']=('../' if a['hreflang']=='en' else '')+self.name
  for key in ['alt','aria-label','placeholder']:
   if a.get(key) in ATTRS:a[key]=ATTRS[a[key]]
   elif a.get(key,'').startswith('Institutional and funder logos'):a[key]='TVPlab原网站所列机构与资助方标志'
  if tag=='meta' and a.get('name')=='description':a['content']=TITLES[self.name[:-5]]+'。了解我们的研究、团队及实验室动态。'
  self.out.append('<'+tag+''.join(' '+k+('="'+escape(v,quote=True)+'"' if v is not None else '') for k,v in a.items())+(' />' if closed else '>'))
 def handle_starttag(self,t,a):self.tag(t,a)
 def handle_startendtag(self,t,a):self.tag(t,a,True)
 def handle_endtag(self,t):
  self.out.append('</'+t+'>')
  if t=='title':self.title=False
  if t=='div' and self.pub_depth:self.pub_depth-=1
 def handle_data(self,t):
  if self.title:out=TITLES[self.name[:-5]]
  elif self.pub_depth:out=t
  else:out=translate(t)
  self.out.append(escape(out,quote=False))
 def handle_comment(self,t):self.out.append('<!--'+t+'-->')
 def handle_decl(self,t):self.out.append('<!'+t+'>')
for p in sorted(ROOT.glob('*.html')):
 l=Localize(p.name);l.feed(p.read_text());s=''.join(l.out)
 if p.stem=='publications':s=s.replace('<div class="inner-wrap">','<div class="inner-wrap"><p class="bibliography-note">为便于准确检索，以下保留论文正式英文题名、作者姓名和期刊名称。</p>',1)
 (ROOT/'zh'/p.name).write_text(s)
if missing:
 print('UNTRANSLATED:',*sorted(missing),sep='\n');raise SystemExit(1)
print('Chinese pages generated: 9; all narrative text covered.')
