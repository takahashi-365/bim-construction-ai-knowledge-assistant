# Metadata Design

## 1. このドキュメントの目的

このドキュメントは、PoC 3：BIM / Construction AI Knowledge Assistant において、RAG-style Knowledge Documents に付与するmetadataを定義するための設計資料である。

PoC 3では、PoC 1・PoC 2の成果物を検索対象ナレッジとして整理し、質問に対して関連するdocumentを検索し、根拠付き回答を生成する。

その際、単に本文を検索するだけではなく、以下を回答内で明示できる必要がある。

```text
どのPoC由来の情報か
どの種類の情報か
どのRuleIdまたはUseCaseIdに基づく情報か
Human Reviewが必要か
Deep Diveが必要か
どのファイル由来の情報か
どの推奨アプローチに基づく情報か
```

このため、各documentにはmetadataを付与する。

metadataは、検索、参照元表示、回答生成、pytest検証のすべてで使用する。

---

## 2. Metadataの役割

PoC 3におけるmetadataの役割は以下である。

* 検索結果の出所を明確にする
* 回答の根拠を明示する
* RuleIdやUseCaseIdを回答内に表示する
* HumanReviewRequiredを回答方針に反映する
* DeepDiveRequiredを追加確認事項に反映する
* SourcePoCやSourceTypeで情報の種類を区別する
* pytestで必須項目の存在を検証する
* 将来的なRAG / Azure AI Search拡張時の設計基盤にする

PoC 3のMVPでは、本格的なベクトル検索やクラウド検索は行わない。

ただし、将来的に検索基盤へ拡張できるように、metadataは最初から構造化しておく。

---

## 3. Metadata設計の基本方針

metadata設計では、以下の方針を守る。

* すべてのdocumentに共通metadataを持たせる
* Rule単位、Fix Guide単位、UseCase単位、Policy単位、Summary単位で必要なmetadataを分ける
* 回答時に参照元として表示できる項目を持たせる
* 検索処理でフィルタやスコアリングに使える項目を持たせる
* HumanReviewRequiredとDeepDiveRequiredを明示する
* 実案件データ、顧客データ、社内サービス詳細はmetadataにも含めない
* 値の表記ゆれをできるだけ抑える
* Python / pandas / JSONL / Markdown / pytest で扱いやすい形式にする

---

## 4. RAG-style documentの基本構造

PoC 3では、1つのchunkを原則として1つのRAG-style documentとして扱う。

JSONLの1行が1documentであり、基本構造は以下である。

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
    "use_case_id": "",
    "severity": "High",
    "recommended_approach": "",
    "human_review_required": true,
    "deep_dive_required": false,
    "source_file": "poc1_knowledge_samples.csv"
  },
  "keywords": ["door", "name", "missing", "quality", "rule", "human review"]
}
```

PoC 3では、上位項目とmetadata内項目を使い分ける。

---

## 5. 上位項目とmetadata内項目の考え方

RAG-style documentでは、以下を上位項目として持つ。

```text
document_id
source_poc
source_type
title
content
metadata
keywords
```

上位項目は、検索や表示で頻繁に使う基本項目である。

一方、metadata内には、RuleId、UseCaseId、Severity、HumanReviewRequiredなど、検索結果や回答生成で補足的に使う構造化情報を入れる。

整理すると以下である。

| 区分          | 項目例                   | 用途                                    |
| ----------- | --------------------- | ------------------------------------- |
| 上位項目        | document_id           | documentを一意に識別する                      |
| 上位項目        | source_poc            | PoC1 / PoC2 / PoC3 の由来を示す             |
| 上位項目        | source_type           | RuleMaster / UseCaseMapping など情報種別を示す |
| 上位項目        | title                 | 検索結果・回答で表示する見出し                       |
| 上位項目        | content               | 回答根拠として使う本文                           |
| 上位項目        | keywords              | 簡易検索で使うキーワード                          |
| metadata内項目 | rule_id               | Rule単位の根拠を示す                          |
| metadata内項目 | use_case_id           | UseCase単位の根拠を示す                       |
| metadata内項目 | human_review_required | 人間レビュー要否を示す                           |
| metadata内項目 | source_file           | 元ファイルを示す                              |

---

## 6. 共通metadata項目

すべてのdocumentに付与する共通項目は以下である。

```text
document_id
source_poc
source_type
title
content
metadata.category
metadata.rule_id
metadata.use_case_id
metadata.severity
metadata.recommended_approach
metadata.human_review_required
metadata.deep_dive_required
metadata.source_file
keywords
```

ただし、すべての項目に値が入るとは限らない。

例えば、Rule単位chunkではrule_idに値が入り、use_case_idは空でよい。

UseCase単位chunkではuse_case_idに値が入り、rule_idは空でよい。

Policy単位chunkやSummary単位chunkでは、rule_idとuse_case_idの両方が空でもよい。

---

## 7. 共通metadata項目の定義

### 7.1 document_id

document_idは、各documentを一意に識別するIDである。

例。

```text
P1-RULE-D001
P1-FIX-F001
P2-USECASE-UC001
P3-POLICY-HUMAN001
P3-SUMMARY-WORKFLOW001
```

命名ルール。

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

document_idは、検索結果CSV、回答Markdown、pytestで参照するため、重複させない。

---

### 7.2 source_poc

source_pocは、documentの由来となるPoCを示す。

使用する値は以下。

```text
PoC1
PoC2
PoC3
```

意味は以下。

| 値    | 意味                                           |
| ---- | -------------------------------------------- |
| PoC1 | BIM Data Quality & AI Readiness Assessment由来 |
| PoC2 | BIM / Construction AI Use Case Mapper由来      |
| PoC3 | Knowledge Assistant本体の方針・制約・概要由来             |

---

### 7.3 source_type

source_typeは、documentの情報種別を示す。

PoC 3では、以下の値を使用する。

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

意味は以下。

| source_type        | 意味                |
| ------------------ | ----------------- |
| RuleMaster         | 品質チェックルール         |
| QualityCheckResult | 品質チェック結果          |
| FixGuide           | 修正方針・確認方針         |
| AIContext          | AI向け構造化コンテキスト     |
| AIReadiness        | AI活用準備度に関する情報     |
| UseCaseMapping     | 業務ユースケース分類        |
| ClassificationRule | ユースケース分類ルール       |
| DiscussionReport   | 協議用レポート           |
| AnswerPolicy       | 回答方針              |
| HumanReviewPolicy  | 人間レビュー方針          |
| Limitations        | 制約事項              |
| WorkflowSummary    | PoC全体の関係・ワークフロー説明 |

source_typeは、検索結果や回答内で「どの種類の情報を参照しているか」を示すために使用する。

---

### 7.4 title

titleは、documentの見出しである。

検索結果CSVや回答Markdownで表示する。

例。

```text
Door Name Missing Rule
Room Number Missing Rule
Door Name Missing Fix Guide
BIM Issue Review Use Case
Human Review Required Policy
PoC 1 to PoC 3 Workflow Summary
```

titleは短く、内容が分かるものにする。

---

### 7.5 content

contentは、回答根拠として使う本文である。

contentには、以下を含める。

* documentの説明
* 何を意味する情報か
* どの判断や確認に使うか
* AI ReadinessやAI/DX活用への影響
* Human Reviewが必要な場合の理由
* 注意事項

contentは、検索に使うだけでなく、回答文の根拠にもなる。

そのため、単語だけでなく、文章として意味が通る内容にする。

---

### 7.6 metadata.category

categoryは、BIMカテゴリや業務カテゴリを示す。

PoC 1では主にBIMカテゴリを入れる。

例。

```text
Door
Room
Element
General
```

PoC 2では業務領域やユースケース分類を入れてもよい。

例。

```text
BIM Review
Construction Planning
Quality Management
AI/DX Planning
General
```

カテゴリが特定できない場合は、空欄またはGeneralを使用する。

---

### 7.7 metadata.rule_id

rule_idは、PoC 1由来の品質チェックRuleIdを示す。

例。

```text
D-001
D-002
R-101
R-102
```

Rule単位chunkやFix Guide単位chunkで使用する。

PoC 2由来のUseCase単位chunkでは空欄でよい。

---

### 7.8 metadata.use_case_id

use_case_idは、PoC 2由来の業務ユースケースIDを示す。

例。

```text
UC-001
UC-002
UC-003
```

UseCase単位chunkで使用する。

PoC 1由来のRule単位chunkでは空欄でよい。

---

### 7.9 metadata.severity

severityは、品質問題や確認事項の重要度を示す。

主にPoC 1由来のRule単位chunk、QualityCheckResult、FixGuideで使用する。

推奨値は以下。

```text
High
Medium
Low
Info
```

意味は以下。

| 値      | 意味                        |
| ------ | ------------------------- |
| High   | AI Readinessや後続処理への影響が大きい |
| Medium | 確認・修正した方がよい               |
| Low    | 影響は限定的だが確認対象になる           |
| Info   | 説明・参考情報                   |

severityは、検索結果や回答で優先度を説明するために使う。

---

### 7.10 metadata.recommended_approach

recommended_approachは、PoC 2由来のユースケースに対して推奨されるAI/DX活用方針を示す。

例。

```text
RAG Support
BI / Dashboard
Automation Support
Rule-based Check
Human Review
Deep Dive Required
RAG Support + Human Review
Automation Support + Human Review
BI + Human Review
```

recommended_approachは、UseCase単位chunkやDiscussionReportで使用する。

PoC 1由来のRule単位chunkでは空欄でよい。

---

### 7.11 metadata.human_review_required

human_review_requiredは、人間レビューが必要かどうかを示すboolean値である。

値は以下。

```text
true
false
```

trueにする例。

```text
設計判断が含まれる
施工判断が含まれる
法規判断が含まれる
安全判断が含まれる
契約判断が含まれる
顧客合意が必要である
自動修正や自動承認が不適切である
```

falseにできる例。

```text
単純な情報参照
補助的な分類
明確なルールに基づく表示
協議前の参考情報整理
```

ただし、falseであっても、AIが最終判断するという意味ではない。

PoC 3では、判断の性質に応じてHuman Review注意書きを表示する。

---

### 7.12 metadata.deep_dive_required

deep_dive_requiredは、追加確認や詳細調査が必要かどうかを示すboolean値である。

値は以下。

```text
true
false
```

trueにする例。

```text
入力情報が不足している
判断条件が曖昧である
業務内容が広すぎる
関係者確認が必要である
AI/DX適用方針を決めるには追加ヒアリングが必要である
```

DeepDiveRequired=Trueの場合、回答内で「追加確認が必要」と明示する。

---

### 7.13 metadata.source_file

source_fileは、documentの元になったファイル名を示す。

例。

```text
poc1_knowledge_samples.csv
poc2_knowledge_samples.csv
mvp_scope.md
bim_to_ai_workflow_blueprint.md
chunk_design.md
answer_policy.md
human_review_policy.md
limitations.md
```

source_fileは、回答のReferenced Sourcesに表示する。

実ファイルパスではなく、リポジトリ内で確認しやすい相対的なファイル名を使う。

---

### 7.14 keywords

keywordsは、簡易検索で使用するキーワードの配列である。

PoC 3のMVPではEmbedding検索を使わないため、keywordsは検索精度に大きく影響する。

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

```json
["door", "Door", "ドア", "扉", "name", "名称", "missing", "未入力", "D-001", "quality", "品質", "human review", "人間レビュー"]
```

日本語質問でも英語項目名でも検索できるように、可能な範囲で日英のキーワードを含める。

---

## 8. Chunk種別ごとのmetadata設計

PoC 3では、chunk種別ごとに必要なmetadataが異なる。

扱うchunk種別は以下。

```text
Rule単位
Fix Guide単位
UseCase単位
Policy単位
Summary単位
```

---

## 9. Rule単位metadata

Rule単位chunkでは、PoC 1由来の品質チェックルールを扱う。

### 9.1 必須項目

```text
document_id
source_poc
source_type
title
content
metadata.category
metadata.rule_id
metadata.severity
metadata.human_review_required
metadata.source_file
keywords
```

### 9.2 任意項目

```text
metadata.target_field
metadata.check_logic
metadata.ai_readiness_impact
metadata.fix_guide_id
metadata.deep_dive_required
```

### 9.3 例

```json
{
  "document_id": "P1-RULE-D001",
  "source_poc": "PoC1",
  "source_type": "RuleMaster",
  "title": "Door Name Missing Rule",
  "content": "このRuleは、DoorカテゴリのName項目が未入力または不明確な状態を検出するための品質チェックである。Nameが不足している場合、AI Context生成や検索対象ナレッジ化において、対象要素を識別しにくくなる可能性がある。",
  "metadata": {
    "category": "Door",
    "rule_id": "D-001",
    "use_case_id": "",
    "severity": "High",
    "target_field": "Name",
    "check_logic": "Name is missing or blank",
    "ai_readiness_impact": "Element identification becomes difficult for AI context generation.",
    "recommended_approach": "",
    "human_review_required": true,
    "deep_dive_required": false,
    "source_file": "poc1_knowledge_samples.csv"
  },
  "keywords": ["door", "ドア", "name", "名称", "missing", "未入力", "D-001", "quality", "AI readiness", "human review"]
}
```

---

## 10. Fix Guide単位metadata

Fix Guide単位chunkでは、PoC 1由来の修正方針や確認ポイントを扱う。

### 10.1 必須項目

```text
document_id
source_poc
source_type
title
content
metadata.category
metadata.rule_id
metadata.human_review_required
metadata.source_file
keywords
```

### 10.2 任意項目

```text
metadata.fix_guide_id
metadata.related_rule_id
metadata.issue_type
metadata.review_point
metadata.caution
metadata.deep_dive_required
```

### 10.3 例

```json
{
  "document_id": "P1-FIX-F001",
  "source_poc": "PoC1",
  "source_type": "FixGuide",
  "title": "Door Name Missing Fix Guide",
  "content": "このFix Guideは、DoorカテゴリのName項目が不足している場合の確認方針を示す。対象DoorのElementId、UniqueId、FamilyName、TypeNameを確認し、プロジェクトの命名ルールや設計意図に沿ってNameを設定する必要がある。AIによる自動修正は行わず、BIM担当者による確認を前提とする。",
  "metadata": {
    "category": "Door",
    "rule_id": "D-001",
    "use_case_id": "",
    "severity": "High",
    "fix_guide_id": "F001",
    "related_rule_id": "D-001",
    "recommended_approach": "",
    "human_review_required": true,
    "deep_dive_required": false,
    "source_file": "poc1_knowledge_samples.csv"
  },
  "keywords": ["door", "ドア", "fix guide", "修正方針", "name", "名称", "D-001", "human review"]
}
```

---

## 11. UseCase単位metadata

UseCase単位chunkでは、PoC 2由来のBIM・建設業務ユースケース分類を扱う。

### 11.1 必須項目

```text
document_id
source_poc
source_type
title
content
metadata.category
metadata.use_case_id
metadata.recommended_approach
metadata.human_review_required
metadata.deep_dive_required
metadata.source_file
keywords
```

### 11.2 任意項目

```text
metadata.business_area
metadata.rag_suitable
metadata.bi_suitable
metadata.automation_suitable
metadata.rule_based_check_suitable
metadata.discussion_point
```

### 11.3 例

```json
{
  "document_id": "P2-USECASE-UC001",
  "source_poc": "PoC2",
  "source_type": "UseCaseMapping",
  "title": "BIM Issue Report Review Use Case",
  "content": "このUseCaseは、BIMに関する指摘内容を確認し、過去のルール、Fix Guide、関連資料を参照しながら対応方針を整理する業務である。過去ナレッジ検索や類似事例の参照が有効なため、RAG-style検索との相性が高い。一方で、設計判断、施工判断、契約判断を含む場合はAIが最終判断を行うべきではない。",
  "metadata": {
    "category": "BIM Review",
    "rule_id": "",
    "use_case_id": "UC-001",
    "severity": "",
    "recommended_approach": "RAG Support + Human Review",
    "rag_suitable": true,
    "bi_suitable": false,
    "automation_suitable": false,
    "rule_based_check_suitable": true,
    "human_review_required": true,
    "deep_dive_required": false,
    "source_file": "poc2_knowledge_samples.csv"
  },
  "keywords": ["BIM", "issue", "指摘", "review", "RAG", "ナレッジ検索", "UC-001", "human review", "人間レビュー"]
}
```

---

## 12. Policy単位metadata

Policy単位chunkでは、PoC 3の回答方針、Human Review方針、制約事項を扱う。

### 12.1 必須項目

```text
document_id
source_poc
source_type
title
content
metadata.human_review_required
metadata.source_file
keywords
```

### 12.2 任意項目

```text
metadata.policy_id
metadata.policy_type
metadata.applicable_scope
metadata.caution_text
metadata.deep_dive_required
```

### 12.3 例

```json
{
  "document_id": "P3-POLICY-HUMAN001",
  "source_poc": "PoC3",
  "source_type": "HumanReviewPolicy",
  "title": "AI does not make final decisions",
  "content": "PoC 3の回答は、協議用の参考情報として扱う。設計判断、施工判断、法規判断、安全判断、契約判断はAIが最終判断してはならない。最終的な判断はBIM担当者、設計者、施工担当者、または関係者が行う必要がある。",
  "metadata": {
    "category": "Policy",
    "rule_id": "",
    "use_case_id": "",
    "severity": "High",
    "recommended_approach": "Human Review",
    "policy_id": "HUMAN001",
    "policy_type": "HumanReviewPolicy",
    "human_review_required": true,
    "deep_dive_required": false,
    "source_file": "human_review_policy.md"
  },
  "keywords": ["human review", "人間レビュー", "final decision", "最終判断", "設計判断", "施工判断", "法規判断", "安全判断", "契約判断"]
}
```

---

## 13. Summary単位metadata

Summary単位chunkでは、PoC全体の関係やワークフローを扱う。

### 13.1 必須項目

```text
document_id
source_poc
source_type
title
content
metadata.source_file
keywords
```

### 13.2 任意項目

```text
metadata.summary_id
metadata.summary_type
metadata.related_poc
metadata.related_docs
metadata.human_review_required
metadata.deep_dive_required
```

### 13.3 例

```json
{
  "document_id": "P3-SUMMARY-WORKFLOW001",
  "source_poc": "PoC3",
  "source_type": "WorkflowSummary",
  "title": "PoC 1 to PoC 3 Workflow Summary",
  "content": "PoC 1は、BIMデータがAI活用に適しているかを評価するPoCである。PoC 2は、BIM・建設業務がどのAI/DX活用に適しているかを分類するPoCである。PoC 3は、PoC 1・PoC 2の成果物を検索対象にし、根拠付きで説明するローカルRAG-style Knowledge Assistantである。",
  "metadata": {
    "category": "Workflow",
    "rule_id": "",
    "use_case_id": "",
    "severity": "Info",
    "recommended_approach": "",
    "summary_id": "WORKFLOW001",
    "summary_type": "PoCRelationship",
    "related_poc": ["PoC1", "PoC2", "PoC3"],
    "related_docs": ["mvp_scope.md", "bim_to_ai_workflow_blueprint.md"],
    "human_review_required": false,
    "deep_dive_required": false,
    "source_file": "bim_to_ai_workflow_blueprint.md"
  },
  "keywords": ["PoC1", "PoC2", "PoC3", "workflow", "ワークフロー", "AI readiness", "use case mapping", "knowledge assistant"]
}
```

---

## 14. 検索結果CSVで使用するmetadata

検索処理 `src/retrieve_context.py` では、検索結果CSVとして以下を出力する。

```text
QuestionId
Question
Rank
DocumentId
SourcePoC
SourceType
Title
MatchedKeywords
Score
RuleId
UseCaseId
HumanReviewRequired
DeepDiveRequired
SourceFile
```

各項目の対応関係は以下。

| 検索結果CSV項目           | 参照元                            |
| ------------------- | ------------------------------ |
| DocumentId          | document_id                    |
| SourcePoC           | source_poc                     |
| SourceType          | source_type                    |
| Title               | title                          |
| MatchedKeywords     | keywords                       |
| RuleId              | metadata.rule_id               |
| UseCaseId           | metadata.use_case_id           |
| HumanReviewRequired | metadata.human_review_required |
| DeepDiveRequired    | metadata.deep_dive_required    |
| SourceFile          | metadata.source_file           |

検索結果CSVは、回答生成だけでなく、ユーザーが「なぜこの回答になったか」を確認するための中間成果物として扱う。

---

## 15. 回答Markdownで使用するmetadata

回答生成 `src/generate_grounded_answer.py` では、metadataを使って回答に参照元を表示する。

回答に含める項目は以下。

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

各項目の対応関係は以下。

| 回答項目                | 参照元                                  |
| ------------------- | ------------------------------------ |
| Question            | sample_questions_v001.csv            |
| Answer              | content + metadata                   |
| Reasoning Summary   | content + source_type                |
| Referenced Sources  | document_id / source_file / title    |
| RuleId              | metadata.rule_id                     |
| UseCaseId           | metadata.use_case_id                 |
| RecommendedApproach | metadata.recommended_approach        |
| HumanReviewRequired | metadata.human_review_required       |
| DeepDiveRequired    | metadata.deep_dive_required          |
| Caution             | Policy chunk / human_review_required |

HumanReviewRequired=True のdocumentが検索結果に含まれる場合は、回答に必ず注意書きを含める。

DeepDiveRequired=True のdocumentが検索結果に含まれる場合は、追加確認が必要であることを明記する。

---

## 16. HumanReviewRequiredの扱い

PoC 3では、HumanReviewRequiredを特に重要なmetadataとして扱う。

HumanReviewRequired=Trueの場合、回答には以下の趣旨を含める。

```text
この回答は協議用の参考情報です。
設計判断、施工判断、法規判断、安全判断、契約判断は人間レビューが必要です。
AIは最終判断を行いません。
```

HumanReviewRequired=Falseの場合でも、AIが最終判断してよいという意味ではない。

Falseは、該当document単体では強い人間レビュー要否が設定されていないことを示すだけである。

PoC 3全体では、設計判断、施工判断、法規判断、安全判断、契約判断、契約判断、顧客合意が必要な判断については人間レビューを前提とする。

---

## 17. DeepDiveRequiredの扱い

DeepDiveRequired=Trueの場合、回答には以下の趣旨を含める。

```text
この内容は追加確認が必要です。
入力情報、判断条件、関係者確認、業務範囲などを確認したうえで、AI/DX活用方針を協議する必要があります。
```

DeepDiveRequiredは、特にPoC 2由来のUseCase単位chunkで重要である。

業務内容が広すぎる場合や、入力・出力・判断基準が曖昧な場合は、DeepDiveRequired=Trueとする。

---

## 18. metadata値の表記ルール

metadata値は、できるだけ表記ゆれを避ける。

### 18.1 boolean値

boolean値は、JSON上では以下を使う。

```text
true
false
```

CSV上では、必要に応じて以下を使ってもよい。

```text
True
False
```

Python処理時にbooleanへ変換する。

---

### 18.2 source_poc

source_pocは以下に統一する。

```text
PoC1
PoC2
PoC3
```

以下のような表記ゆれは避ける。

```text
POC1
poc1
PoC 1
Poc1
```

---

### 18.3 source_type

source_typeは以下のようなCamelCaseに統一する。

```text
RuleMaster
FixGuide
UseCaseMapping
HumanReviewPolicy
WorkflowSummary
```

以下のような表記ゆれは避ける。

```text
rule_master
rule master
Rule Master
RULEMASTER
```

---

### 18.4 severity

severityは以下に統一する。

```text
High
Medium
Low
Info
```

---

### 18.5 recommended_approach

recommended_approachは、読みやすさを優先して英語フレーズで統一する。

例。

```text
RAG Support
BI / Dashboard
Automation Support
Rule-based Check
Human Review
Deep Dive Required
RAG Support + Human Review
Automation Support + Human Review
BI + Human Review
```

---

## 19. metadataに含めない情報

PoC 3のmetadataには、以下を含めない。

* 実案件名
* 顧客名
* 顧客担当者名
* 社内サービスの詳細情報
* 契約情報
* 金額情報
* 非公開資料名
* 個人情報
* 実プロジェクト固有の判断内容
* Revitモデルの実データ
* 機密性のあるBIM属性
* 自動承認を示す情報
* AIによる最終判断を前提にする情報

PoC 3は個人開発ポートフォリオであるため、サンプルナレッジを使い、公開可能な内容に限定する。

---

## 20. pytestで確認するmetadata項目

PoC 3では、metadataの最低限の品質をpytestで確認する。

確認する内容は以下である。

```text
rag_documents_v001.jsonl が存在すること
各documentに document_id があること
各documentに source_poc があること
各documentに source_type があること
各documentに title があること
各documentに content があること
各documentに metadata があること
各documentに keywords があること
metadataに human_review_required があること
metadataに deep_dive_required があること
metadataに source_file があること
PoC 1由来のdocumentが存在すること
PoC 2由来のdocumentが存在すること
RuleIdを持つdocumentが存在すること
UseCaseIdを持つdocumentが存在すること
document_idが重複していないこと
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

## 21. 将来的な拡張時のmetadata候補

MVPでは使用しないが、将来的に本格RAGやAzure AI Searchへ拡張する場合、以下のmetadataを追加候補とする。

```text
created_at
updated_at
version
language
embedding_text
search_priority
access_level
source_repository
related_document_ids
related_rule_ids
related_use_case_ids
confidence_level
review_status
```

ただし、MVPでは過度にmetadataを増やさない。

まずは、検索、参照元表示、回答生成、pytest検証に必要な項目に絞る。

---

## 22. まとめ

PoC 3では、PoC 1・PoC 2の成果物をRAG-style Knowledge Documentsとして整理し、検索と根拠付き回答生成に利用する。

metadataは、その中で以下の役割を持つ。

```text
検索結果の出所を明確にする
回答の根拠を表示する
RuleIdやUseCaseIdを参照できるようにする
Human Review要否を回答に反映する
Deep Dive要否を回答に反映する
pytestで品質を確認する
将来的な検索基盤拡張に備える
```

PoC 3で特に重要なmetadataは以下である。

```text
document_id
source_poc
source_type
title
category
rule_id
use_case_id
severity
recommended_approach
human_review_required
deep_dive_required
source_file
keywords
```

このmetadata設計により、PoC 3は以下を実現する。

```text
PoC 1・PoC 2の成果物を構造化する
検索対象ナレッジの出所を明確にする
質問に対して関連documentを検索する
回答に参照元を含める
Human Reviewが必要な判断を明示する
Deep Diveが必要な業務を明示する
AIが最終判断しない設計を保つ
```
