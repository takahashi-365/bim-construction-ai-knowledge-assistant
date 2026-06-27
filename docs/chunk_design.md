# Chunk Design

## 1. このドキュメントの目的

このドキュメントは、PoC 3：BIM / Construction AI Knowledge Assistant において、検索対象となるナレッジをどの単位で分割するかを定義するための設計資料である。

PoC 3では、PoC 1・PoC 2の成果物をRAG-style Knowledge Documentsとして整理し、質問に応じて関連情報を検索し、根拠付き回答を生成する。

そのためには、検索対象となる情報を大きすぎず、小さすぎない単位に分割する必要がある。

この分割単位を、このPoCでは「chunk」と呼ぶ。

---

## 2. Chunkとは何か

PoC 3におけるchunkとは、検索対象となるナレッジの最小単位である。

1つのchunkは、1つの質問に対して、回答の根拠として参照できる程度のまとまった情報を持つ。

例えば、PoC 1由来のRule Masterであれば、1つのRuleIdを1つのchunkとして扱う。

PoC 2由来のUse Case Mappingであれば、1つのUseCaseIdを1つのchunkとして扱う。

PoC 3では、chunkをもとにRAG-style document JSONLを生成し、簡易検索インデックスを作成する。

---

## 3. Chunk設計の基本方針

PoC 3のchunk設計では、以下の方針を守る。

* 1つのchunkには、1つの主題を持たせる
* 1つのchunkに複数の論点を詰め込みすぎない
* 回答時に参照元として示しやすい単位にする
* RuleId、UseCaseId、Policyなどの識別子と結びつけやすくする
* HumanReviewRequiredやDeepDiveRequiredを判定・説明しやすい単位にする
* 実案件データ、顧客データ、社内サービス詳細は含めない
* AIが最終判断するような表現を含めない
* 検索結果として返されたときに、BIM担当者やAI/DX導入担当者が内容を確認しやすい形にする

PoC 3のMVPでは、本格的なEmbeddingやVector Searchを使わない。

そのため、chunkには検索しやすいtitle、content、metadata、keywordsを持たせる。

---

## 4. PoC 3で扱うchunk種別

PoC 3では、以下のchunk種別を扱う。

```text
Rule単位
Fix Guide単位
UseCase単位
Policy単位
Summary単位
```

それぞれの役割は以下である。

| Chunk種別     | 主な由来                  | 主な用途                        |
| ----------- | --------------------- | --------------------------- |
| Rule単位      | PoC 1                 | BIMデータ品質チェック内容を説明する         |
| Fix Guide単位 | PoC 1                 | 修正方針や確認ポイントを説明する            |
| UseCase単位   | PoC 2                 | 建設業務ユースケースのAI/DX適性を説明する     |
| Policy単位    | PoC 1 / PoC 2 / PoC 3 | 回答方針・Human Review方針・制約を説明する |
| Summary単位   | PoC 3                 | PoC全体の関係やワークフローを説明する        |

---

## 5. Rule単位chunk

## 5.1 目的

Rule単位chunkは、PoC 1で作成したRule Masterや品質チェック結果を、RuleIdごとに検索可能にするためのchunkである。

BIMデータのどの項目に問題があるのか、その問題がAI Readinessにどう影響するのか、人間レビューが必要かを説明するために使用する。

---

## 5.2 対象情報

Rule単位chunkで扱う情報は以下である。

```text
RuleId
RuleName
Category
TargetField
Severity
IssueDescription
CheckLogic
AIReadinessImpact
HumanReviewRequired
FixGuideSummary
SourceFile
```

---

## 5.3 想定質問

Rule単位chunkは、以下のような質問に対応する。

```text
このRuleIdの違反は何を意味しますか？
Doorカテゴリの品質チェック結果を教えてください。
RoomカテゴリでAI Readinessが低くなる原因は何ですか？
この品質チェックは何を確認していますか？
HumanReviewRequired=True の場合、何に注意すべきですか？
```

---

## 5.4 chunk作成方針

Rule単位chunkは、原則として1つのRuleIdにつき1chunkとする。

1つのchunkに複数のRuleIdをまとめない。

理由は、回答時に参照元としてRuleIdを明示しやすくするためである。

良い例。

```text
DocumentId: P1-RULE-D001
SourcePoC: PoC1
SourceType: RuleMaster
RuleId: D-001
Category: Door
Title: Door Name Missing Rule
```

避ける例。

```text
D-001、D-002、D-003を1つのchunkにまとめる
```

複数のRuleIdを1chunkにまとめると、質問に対してどのRuleIdを根拠に回答したかが分かりにくくなるため、MVPでは避ける。

---

## 5.5 contentに含める内容

Rule単位chunkのcontentには、以下を含める。

* 何をチェックするRuleか
* どのカテゴリに関係するか
* どの項目に不足・不整合があるか
* AI Readinessにどのように影響するか
* 修正または確認の方向性
* Human Reviewが必要か
* AIが自動判断・自動修正しないこと

content例。

```text
このRuleは、DoorカテゴリのName項目が未入力または不明確な状態を検出するための品質チェックである。
Nameが不足している場合、後続のAI Context生成や検索対象ナレッジ化において、対象要素を識別しにくくなる可能性がある。
修正方針としては、BIM担当者がRevitモデルまたは集計表を確認し、適切なDoor Nameを設定する。
ただし、名称の妥当性は設計意図やプロジェクトルールに関係するため、AIによる自動修正は行わず、人間レビューを前提とする。
```

---

## 6. Fix Guide単位chunk

## 6.1 目的

Fix Guide単位chunkは、PoC 1で作成したFix Guideの内容を、修正方針や確認ポイントごとに検索可能にするためのchunkである。

Rule単位chunkが「何が問題か」を説明するのに対し、Fix Guide単位chunkは「どのように確認・修正するか」を説明する。

---

## 6.2 対象情報

Fix Guide単位chunkで扱う情報は以下である。

```text
FixGuideId
RelatedRuleId
Category
IssueType
FixAction
ReviewPoint
Caution
HumanReviewRequired
SourceFile
```

---

## 6.3 想定質問

Fix Guide単位chunkは、以下のような質問に対応する。

```text
Fix Guideは何を示していますか？
この指摘はどのように確認すればよいですか？
この品質問題はRevitモデルを自動修正してよいですか？
Door Name Missing の修正方針を教えてください。
Room Number Missing の確認ポイントを教えてください。
```

---

## 6.4 chunk作成方針

Fix Guide単位chunkは、原則として1つの修正方針につき1chunkとする。

ただし、1つのFix Guideが複数のRuleIdに関連する場合は、RelatedRuleIdに複数のRuleIdを持たせてもよい。

例。

```text
DocumentId: P1-FIX-F001
SourcePoC: PoC1
SourceType: FixGuide
RelatedRuleId: D-001
Category: Door
Title: Door Name Missing Fix Guide
```

Fix Guideは、実際の自動修正手順ではなく、確認・協議・修正判断のための参考情報として扱う。

---

## 6.5 contentに含める内容

Fix Guide単位chunkのcontentには、以下を含める。

* 対象となる品質問題
* 関連するRuleId
* 推奨される確認方法
* 修正時に注意すべき点
* 自動修正しない理由
* Human Reviewが必要な理由

content例。

```text
このFix Guideは、DoorカテゴリのName項目が不足している場合の確認方針を示す。
まず、対象DoorのElementId、UniqueId、FamilyName、TypeNameを確認し、同一タイプや同一用途のDoorと比較する。
そのうえで、プロジェクトの命名ルールや設計意図に沿ってNameを設定する必要がある。
名称設定は設計情報や運用ルールに関係するため、AIが自動で確定するのではなく、BIM担当者による確認を前提とする。
```

---

## 7. UseCase単位chunk

## 7.1 目的

UseCase単位chunkは、PoC 2で作成したBIM・建設業務ユースケース分類を、UseCaseIdごとに検索可能にするためのchunkである。

このchunkは、特定の業務がRAG、BI、自動化、ルールベースチェック、人間レビュー、深掘り対象のどれに向いているかを説明するために使用する。

---

## 7.2 対象情報

UseCase単位chunkで扱う情報は以下である。

```text
UseCaseId
UseCaseName
BusinessArea
InputData
Process
Output
RecommendedApproach
RAGSuitable
BISuitable
AutomationSuitable
RuleBasedCheckSuitable
HumanReviewRequired
DeepDiveRequired
DiscussionPoint
SourceFile
```

---

## 7.3 想定質問

UseCase単位chunkは、以下のような質問に対応する。

```text
このユースケースはRAGに向いていますか？
この業務はAIで自動化してよいですか？
PoC 2のRecommendedApproachは何を意味しますか？
HumanReviewRequired=True になる理由は何ですか？
DeepDiveRequired の業務では何を追加確認すべきですか？
この業務はBI向きですか？
この業務はルールベースチェック向きですか？
```

---

## 7.4 chunk作成方針

UseCase単位chunkは、原則として1つのUseCaseIdにつき1chunkとする。

1つのchunkに複数のUseCaseIdをまとめない。

理由は、回答時にどの業務ユースケースを根拠にしたかを明確にするためである。

良い例。

```text
DocumentId: P2-USECASE-UC001
SourcePoC: PoC2
SourceType: UseCaseMapping
UseCaseId: UC-001
Title: BIM Issue Report Review Use Case
```

避ける例。

```text
複数の業務ユースケースを1つのsummary chunkにまとめ、個別UseCaseIdを持たせない
```

Summary chunkは別途作成してよいが、個別業務の判断根拠にはUseCase単位chunkを使う。

---

## 7.5 contentに含める内容

UseCase単位chunkのcontentには、以下を含める。

* 業務ユースケースの概要
* 入力情報
* 処理内容
* 出力情報
* 推奨されるAI/DX活用方針
* RAG、BI、自動化、ルールベースチェックとの相性
* Human Reviewが必要な理由
* Deep Diveが必要な場合の追加確認事項

content例。

```text
このUseCaseは、BIMに関する指摘内容を確認し、過去のルール、Fix Guide、関連資料を参照しながら対応方針を整理する業務である。
過去のナレッジ検索や類似事例の参照が有効なため、RAG-style検索との相性が高い。
一方で、設計判断、施工判断、契約判断を含む場合はAIが最終判断を行うべきではない。
そのため、RecommendedApproachはRAG Support + Human Reviewとし、回答は協議用の参考情報として扱う。
```

---

## 8. Policy単位chunk

## 8.1 目的

Policy単位chunkは、PoC 3の回答方針、Human Review方針、制約事項を検索可能にするためのchunkである。

PoC 3では、回答が断定的になりすぎたり、AIが最終判断するように見えたりしないように、Policy単位chunkを参照できるようにする。

---

## 8.2 対象情報

Policy単位chunkで扱う情報は以下である。

```text
PolicyId
PolicyType
PolicyTitle
PolicyDescription
ApplicableScope
CautionText
SourceFile
```

PolicyTypeの例。

```text
AnswerPolicy
HumanReviewPolicy
Limitations
DataPrivacyPolicy
NoAutoModificationPolicy
```

---

## 8.3 想定質問

Policy単位chunkは、以下のような質問に対応する。

```text
この回答は最終判断として使えますか？
Human Reviewが必要なのはなぜですか？
PoC 3で使ってはいけないデータは何ですか？
AIがRevitモデルを自動修正しない理由は何ですか？
このPoCの制約事項は何ですか？
```

---

## 8.4 chunk作成方針

Policy単位chunkは、1つの方針につき1chunkとする。

Answer Policy、Human Review Policy、Limitationsなどを大きな1chunkにまとめすぎない。

特に、以下の方針は個別chunkとして扱う。

```text
AIは最終判断を行わない
回答は協議用の参考情報とする
設計判断・施工判断・法規判断・安全判断・契約判断は人間レビュー必須
実案件データ、顧客データ、社内サービス詳細は使用しない
Revitモデルの自動修正は行わない
RAG-styleであり、本格RAGとは表現しない
```

---

## 8.5 contentに含める内容

Policy単位chunkのcontentには、以下を含める。

* 方針の内容
* なぜその方針が必要か
* どの回答・処理に適用されるか
* 注意書きとして回答に含めるべき文言

content例。

```text
PoC 3の回答は、協議用の参考情報として扱う。
設計判断、施工判断、法規判断、安全判断、契約判断は、AIが最終判断してはならない。
検索結果に関連情報が含まれている場合でも、最終的な判断はBIM担当者、設計者、施工担当者、または関係者が行う必要がある。
回答には、必要に応じてHuman Reviewが必要であることを明記する。
```

---

## 9. Summary単位chunk

## 9.1 目的

Summary単位chunkは、PoC 1・PoC 2・PoC 3の関係や、全体ワークフローを説明するためのchunkである。

個別のRuleIdやUseCaseIdではなく、PoC全体の位置づけや考え方を説明するために使用する。

---

## 9.2 対象情報

Summary単位chunkで扱う情報は以下である。

```text
SummaryId
SummaryType
Title
SummaryContent
RelatedPoC
RelatedDocs
SourceFile
```

SummaryTypeの例。

```text
PoCRelationship
WorkflowOverview
MVPOverview
KnowledgeAssistantOverview
HumanReviewOverview
```

---

## 9.3 想定質問

Summary単位chunkは、以下のような質問に対応する。

```text
PoC 1とPoC 2はどうつながりますか？
PoC 3は何をするPoCですか？
PoC 3の全体フローを教えてください。
なぜPoC 3でRAG-style Knowledge Assistantを作るのですか？
PoC 3のMVPでは何を作りますか？
```

---

## 9.4 chunk作成方針

Summary単位chunkは、1つの説明テーマにつき1chunkとする。

ただし、Summary chunkは個別のRuleIdやUseCaseIdの代わりに使うものではない。

個別の品質チェックや業務ユースケースについて回答する場合は、Rule単位chunkまたはUseCase単位chunkを優先する。

Summary chunkは、PoC全体の説明やREADME的な説明の補助として扱う。

---

## 9.5 contentに含める内容

Summary単位chunkのcontentには、以下を含める。

* PoC全体の位置づけ
* PoC間の関係
* ワークフロー
* MVPの範囲
* このPoCで示したい価値

content例。

```text
PoC 1は、BIMデータがAI活用に適しているかを評価するPoCである。
PoC 2は、BIM・建設業務がどのAI/DX活用に適しているかを分類するPoCである。
PoC 3は、PoC 1・PoC 2の成果物を検索対象にし、根拠付きで説明するローカルRAG-style Knowledge Assistantである。
この3つにより、BIMデータ品質、建設業務ユースケース分類、RAG-styleナレッジ検索、Human Review設計を一連の流れとして示す。
```

---

## 10. chunkとRAG-style document JSONLの関係

PoC 3では、1つのchunkを原則として1つのRAG-style documentとしてJSONL化する。

JSONLの1行が1documentであり、1documentが1chunkに対応する。

基本構造は以下である。

```json
{
  "document_id": "P1-RULE-D001",
  "source_poc": "PoC1",
  "source_type": "RuleMaster",
  "title": "Door Name Missing Rule",
  "content": "このRuleは、DoorカテゴリのName項目が未入力または不明確な状態を検出するための品質チェックである。",
  "metadata": {
    "category": "Door",
    "rule_id": "D-001",
    "severity": "High",
    "human_review_required": true,
    "source_file": "poc1_knowledge_samples.csv"
  },
  "keywords": ["door", "name", "missing", "quality", "rule", "human review"]
}
```

PoC 3のMVPでは、このJSONLを検索対象の中間成果物として扱う。

---

## 11. document_idの命名ルール

document_idは、SourcePoC、chunk種別、連番またはIDを組み合わせて作成する。

推奨する命名ルールは以下である。

```text
PoC 1 Rule:
P1-RULE-{RuleId}

PoC 1 Fix Guide:
P1-FIX-{FixGuideId}

PoC 2 UseCase:
P2-USECASE-{UseCaseId}

PoC 3 Policy:
P3-POLICY-{PolicyId}

PoC 3 Summary:
P3-SUMMARY-{SummaryId}
```

例。

```text
P1-RULE-D001
P1-RULE-R101
P1-FIX-F001
P2-USECASE-UC001
P3-POLICY-ANSWER001
P3-POLICY-HUMAN001
P3-SUMMARY-WORKFLOW001
```

document_idは、検索結果CSV、回答Markdown、pytestで参照されるため、重複しないようにする。

---

## 12. chunkに付与する共通項目

すべてのchunkには、以下の共通項目を付与する。

```text
document_id
source_poc
source_type
title
content
metadata
keywords
```

各項目の意味は以下である。

| 項目          | 説明                                                  |
| ----------- | --------------------------------------------------- |
| document_id | chunkを一意に識別するID                                     |
| source_poc  | PoC1、PoC2、PoC3などの由来                                 |
| source_type | RuleMaster、FixGuide、UseCaseMapping、Policy、Summaryなど |
| title       | 検索結果や回答で表示するタイトル                                    |
| content     | 回答根拠として使う本文                                         |
| metadata    | RuleId、UseCaseId、HumanReviewRequiredなどの構造化情報        |
| keywords    | 簡易検索で使用するキーワード                                      |

---

## 13. source_typeの定義

source_typeは、chunkの種類を示す分類である。

PoC 3では、以下のsource_typeを使用する。

```text
RuleMaster
QualityCheckResult
FixGuide
AIContext
AIReadiness
UseCaseMapping
ClassificationRule
DiscussionReport
AnswerPolicy
HumanReviewPolicy
Limitations
WorkflowSummary
```

source_typeは、検索結果や回答時に、参照した情報の性質を説明するために使用する。

例。

```text
SourceType: RuleMaster
→ BIMデータ品質チェックのルールを参照している

SourceType: UseCaseMapping
→ BIM・建設業務ユースケース分類を参照している

SourceType: HumanReviewPolicy
→ 人間レビュー方針を参照している
```

---

## 14. keywordsの設計方針

PoC 3のMVPでは、本格的なEmbedding検索を使わない。

そのため、keywordsは簡易検索の精度を上げるために重要である。

keywordsには、以下を含める。

* 日本語キーワード
* 英語キーワード
* RuleId
* UseCaseId
* Category
* SourceType
* RecommendedApproach
* HumanReviewRequiredに関係する語
* DeepDiveRequiredに関係する語

例。

```text
["door", "Door", "ドア", "扉", "name", "名称", "missing", "未入力", "D-001", "quality", "品質", "human review", "人間レビュー"]
```

PoC 3では、日本語質問でも英語項目名でも検索できるように、可能な範囲で日英のキーワードを含める。

---

## 15. chunkサイズの目安

PoC 3のMVPでは、1chunkのcontentは短すぎず、長すぎない範囲にする。

目安は以下である。

```text
最小：
2〜3文程度

標準：
5〜10文程度

最大：
1つのテーマを説明する範囲まで
```

避けるべき状態。

```text
1文だけで説明不足
複数テーマを詰め込みすぎている
RuleIdやUseCaseIdが複数混在している
回答時にどこを根拠にしたか分からない
```

MVPでは、精密なトークン数管理は行わない。

ただし、将来的に本格RAGへ拡張する場合は、chunkサイズ、token数、overlap、embedding対象範囲を再設計する。

---

## 16. 検索時の優先順位

検索時は、質問の種類に応じて優先するchunk種別を変える。

| 質問の種類              | 優先するchunk                            |
| ------------------ | ------------------------------------ |
| RuleIdに関する質問       | Rule単位chunk                          |
| 品質問題の意味に関する質問      | Rule単位chunk                          |
| 修正方針に関する質問         | Fix Guide単位chunk                     |
| 業務ユースケースに関する質問     | UseCase単位chunk                       |
| Human Reviewに関する質問 | Policy単位chunk + Rule / UseCase chunk |
| PoC全体の関係に関する質問     | Summary単位chunk                       |
| 制約事項に関する質問         | Policy単位chunk                        |

検索結果には、可能であれば複数のchunkを含める。

例えば、「この業務はAIで自動化してよいですか？」という質問では、UseCase単位chunkだけでなく、Human Review Policyのchunkも合わせて参照する。

---

## 17. 回答生成時のchunk利用方針

PoC 3では、検索されたchunkをもとに根拠付き回答を生成する。

回答生成時の基本方針は以下である。

* 最も関連性の高いchunkを主根拠にする
* HumanReviewRequired=True のchunkが含まれる場合は、回答に人間レビュー注意書きを入れる
* DeepDiveRequired=True のchunkが含まれる場合は、追加確認が必要であることを明記する
* RuleIdがある場合はRuleIdを表示する
* UseCaseIdがある場合はUseCaseIdを表示する
* SourceFileをReferenced Sourcesに表示する
* Policy chunkが検索された場合は、Cautionに反映する
* AIが最終判断する表現は使わない

回答に含める項目は以下である。

```text
Question
Answer
Reasoning Summary
Referenced Sources
RuleId
UseCaseId
RecommendedApproach
HumanReviewRequired
DeepDiveRequired
Caution
```

---

## 18. chunk設計で避けること

PoC 3のchunk設計では、以下を避ける。

* 実案件データを含める
* 顧客名や社内サービス詳細を含める
* 複数のRuleIdを無理に1chunkへまとめる
* 複数のUseCaseIdを無理に1chunkへまとめる
* 参照元が分からないchunkを作る
* AIが最終判断するようなcontentを書く
* Revitモデルを自動修正する前提で書く
* 本格RAGとして誇張する
* 検索結果として返されても意味が分からない短すぎるchunkを作る
* 1つのchunkに複数テーマを詰め込みすぎる

---

## 19. pytestで確認する観点

chunk設計は、最終的にpytestでも最低限確認する。

確認観点は以下である。

```text
rag_documents_v001.jsonl が存在すること
各documentに document_id があること
各documentに source_poc があること
各documentに source_type があること
各documentに title があること
各documentに content があること
各documentに metadata があること
各documentに keywords があること
PoC 1由来のdocumentが存在すること
PoC 2由来のdocumentが存在すること
RuleIdまたはUseCaseIdを持つdocumentが存在すること
HumanReviewRequiredを持つdocumentが存在すること
禁止表現を含まないこと
```

禁止表現の例。

```text
AIが最終判断します
自動で承認します
Revitモデルを自動修正します
人間確認は不要です
```

---

## 20. まとめ

PoC 3では、PoC 1・PoC 2の成果物を検索可能なRAG-style Knowledge Documentsとして整理する。

そのために、以下のchunk単位を使用する。

```text
Rule単位
Fix Guide単位
UseCase単位
Policy単位
Summary単位
```

Rule単位chunkは、BIMデータ品質チェックの内容を説明する。

Fix Guide単位chunkは、修正方針や確認ポイントを説明する。

UseCase単位chunkは、BIM・建設業務ユースケースのAI/DX適性を説明する。

Policy単位chunkは、回答方針、Human Review方針、制約事項を説明する。

Summary単位chunkは、PoC全体の関係やワークフローを説明する。

PoC 3のMVPでは、1chunkを原則として1つのJSONL documentとして扱い、簡易検索と根拠付き回答生成に利用する。

このchunk設計により、PoC 3は以下を実現する。

```text
PoC 1・PoC 2の成果物を再利用する
検索対象ナレッジを構造化する
質問に対して関連情報を検索する
回答に参照元を含める
Human Reviewが必要な判断を明示する
AIが最終判断しない設計を保つ
```
