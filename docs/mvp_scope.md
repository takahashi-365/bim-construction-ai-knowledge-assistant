# MVPスコープ定義

## 1. 目的

PoC 3：BIM / Construction AI Knowledge Assistant は、PoC 1 と PoC 2 で作成した成果物を検索対象にし、BIM担当者やAI/DX導入担当者が、根拠付きで確認できるローカルRAG-styleナレッジアシスタントを作成するための個人開発PoCである。

このPoCの目的は、AIが最終判断を行うことではない。

PoC 1・PoC 2で整理したBIMデータ品質情報、AI Readiness情報、Fix Guide、Human Review方針、BIM・建設業務ユースケース分類情報を検索可能なナレッジとして整理し、質問に応じて関連情報を抽出し、関係者が確認・協議するための回答案と参照情報を提示することである。

---

## 2. PoC 1・PoC 2との関係

PoC 1 は、BIMデータ品質とAI Readiness評価を扱った成果物である。

PoC 1で扱った主な内容は以下。

* Revit集計表TXTの読み込み
* Room Schedule TXTの処理
* pyRevit Metadata CSV
* BIMデータクレンジング
* RuleIdベース品質チェック
* AI Readiness Score
* AI Context
* Fix Guide
* HumanReviewRequired設計
* RAG構成検討

PoC 2 は、BIM・建設業務ユースケースのAI/DX分類を扱った成果物である。

PoC 2で扱った主な内容は以下。

* BIM・建設業務ユースケースCSV
* RAG候補
* BI候補
* 自動化候補
* ルールベースチェック候補
* HumanReviewRequired
* DeepDiveRequired
* RecommendedApproach
* DXサービス候補
* 協議用レポート

PoC 3 は、PoC 1・PoC 2の成果物を検索対象として再利用し、根拠付きで説明するためのナレッジ検索アシスタントとして位置づける。

整理すると以下の関係になる。

```text
PoC 1：
BIMデータがAI活用に適しているかを評価する

PoC 2：
BIM・建設業務がどのAI/DX活用に適しているかを分類する

PoC 3：
PoC 1・PoC 2の成果物を検索し、根拠付きで説明する
```

---

## 3. MVPで実現すること

PoC 3のMVPでは、本格的なクラウドRAGやベクトルDB実装ではなく、ローカルで動作する簡易RAG-style構成を作成する。

MVPで実現することは以下。

* PoC 1由来のサンプルナレッジを作成する
* PoC 2由来のサンプルナレッジを作成する
* サンプル質問CSVを作成する
* PoC 1・PoC 2のナレッジをRAG-style document JSONLに変換する
* 各ナレッジにmetadataを付与する
* 簡易検索用インデックスを作成する
* 質問に対して関連ナレッジを検索する
* 検索結果をもとに、根拠付き回答サンプルをMarkdownで生成する
* 回答に参照元、RuleId、UseCaseId、HumanReviewRequired、DeepDiveRequiredなどを含める
* AIが最終判断しないことを回答ポリシーとして明記する
* pytestで、ドキュメント生成、検索、回答方針が機能していることを検証する

---

## 4. MVPで扱う検索対象

MVPでは、PoC 1・PoC 2の実ファイルを大量に取り込むのではなく、ポートフォリオ用のサンプルナレッジとして整理して扱う。

### 4.1 PoC 1由来の検索対象

PoC 1からは、以下の情報をサンプル化して扱う。

* Rule Master
* AI Context
* Fix Guide
* 品質チェック結果
* AI Readiness Score
* HumanReviewRequired
* pyRevit Metadata
* RAG設計方針

想定する質問例は以下。

* このRuleIdの違反は何を意味しますか？
* Doorカテゴリの品質チェック結果を教えてください。
* RoomカテゴリでAI Readinessが低くなる原因は何ですか？
* Fix Guideは何を示していますか？
* この指摘はRevitモデルを自動修正してよいですか？
* HumanReviewRequired=True の場合、何に注意すべきですか？

### 4.2 PoC 2由来の検索対象

PoC 2からは、以下の情報をサンプル化して扱う。

* AI Use Case Mapping
* RecommendedApproach
* RAG候補
* BI候補
* 自動化候補
* RuleBasedCheck候補
* HumanReviewRequired
* DeepDiveRequired
* DX Service Candidates
* Discussion Reference Report
* Classification Rules
* Human Review Policy

想定する質問例は以下。

* このユースケースはRAGに向いていますか？
* この業務はAIで自動化してよいですか？
* HumanReviewRequired=True になる理由は何ですか？
* DeepDiveRequired の業務では何を追加確認すべきですか？
* PoC 2のRecommendedApproachは何を意味しますか？
* PoC 1とPoC 2はどうつながりますか？

---

## 5. MVPで作成する成果物

MVPで作成する主な成果物は以下。

### 5.1 input

* PoC 1由来のサンプルナレッジCSV
* PoC 2由来のサンプルナレッジCSV
* サンプル質問CSV

### 5.2 output

* RAG-style document JSONL
* 簡易検索インデックス
* 質問ごとの検索結果CSV
* 根拠付き回答サンプルMarkdown

### 5.3 src

* ナレッジ文書生成スクリプト
* 簡易インデックス生成スクリプト
* 検索処理スクリプト
* 根拠付き回答生成スクリプト

### 5.4 docs

* MVPスコープ定義
* BIM Data to AI Workflow Blueprint
* Chunk設計
* Metadata設計
* Answer Policy
* Human Review Policy
* Limitations

### 5.5 tests

* RAG-style documentの必須項目チェック
* 検索結果が空でないことのチェック
* 回答に参照元が含まれることのチェック
* Human Review注意書きが含まれることのチェック
* AIが最終判断する表現を含まないことのチェック

---

## 6. MVPで作らないもの

PoC 3のMVPでは、以下は対象外とする。

* Azure AI Search の本実装
* Azure OpenAI API 連携
* OpenAI API 連携
* LangChain / LlamaIndex の本格実装
* ベクトルDB本格実装
* FAISS / Chroma の本格利用
* Embedding生成
* Revitモデルの自動修正
* Revit API / pyRevit v2 の新規開発
* COBie Checker の実装
* FixPriority分類モデルの実装
* Construction AI PoC Planning Toolkit 完全版
* 実案件データの利用
* 顧客データの利用
* 社内サービス詳細の利用

MVPでは、RAGの仕組みを大きく作り込むのではなく、RAG-style knowledge assistant の基本構造を理解し、ポートフォリオとして説明できる形にすることを優先する。

---

## 7. 回答形式

MVPの回答は、LLMによる自由生成ではなく、検索結果をもとにしたテンプレート生成を基本とする。

回答には、以下を含める。

* Question
* Answer
* Reasoning Summary
* Referenced Sources
* RuleId
* UseCaseId
* SourceType
* RecommendedApproach
* HumanReviewRequired
* DeepDiveRequired
* Caution

回答例の構造は以下。

```text
Question:
この業務はAIで自動化してよいですか？

Answer:
この業務は一部自動化候補として扱えますが、設計判断・施工判断・法規判断を含む場合はAIによる最終判断は行わず、人間レビューが必要です。

Referenced Sources:
- UseCaseId: UC-XXX
- SourceType: PoC2_UseCaseMapping
- RecommendedApproach: Automation Support + Human Review

HumanReviewRequired:
True

Caution:
この回答は協議用の参考情報です。最終判断はBIM担当者、設計者、施工担当者、または関係者が行う必要があります。
```

---

## 8. 必ず守る方針

PoC 3では、以下の方針を必ず守る。

* AIは最終判断を行わない
* 回答は協議材料として扱う
* 設計判断、施工判断、法規判断、安全判断、契約判断は人間レビュー必須とする
* 実案件データ、顧客データ、社内サービス詳細は使用しない
* 検索結果には参照元を明示する
* 回答には注意書きを含める
* 自動修正や自動承認を前提にしない
* RAG-style として実装し、本格RAGであると誇張しない

---

## 9. 技術スタック

MVPで使用する技術は以下。

* Python
* pandas
* JSON / JSONL
* Markdown
* pytest

必要に応じて後で追加する候補は以下。

* Streamlit
* TF-IDF
* scikit-learn
* FAISS
* Chroma
* Azure AI Search 設計資料
* Azure OpenAI 設計資料

MVPでは、まず Python / pandas / JSONL / Markdown / pytest で完結させる。

---

## 10. MVP完了条件

PoC 3のMVP完了条件は以下。

* READMEで目的、PoC 1・PoC 2との関係、実行方法、出力ファイルが説明されている
* docsに設計方針、回答方針、Human Review方針、制約が整理されている
* PoC 1由来のサンプルナレッジがある
* PoC 2由来のサンプルナレッジがある
* サンプル質問CSVがある
* RAG-style document JSONLが生成される
* 簡易インデックスが生成される
* 質問ごとの検索結果CSVが生成される
* 根拠付き回答サンプルMarkdownが生成される
* 回答に参照元が含まれている
* 回答にHuman Review注意書きが含まれている
* pytestが通る
* GitHubで公開できる状態になっている

---

## 11. 最終スコープ判断

PoC 3のMVPは、以下の範囲で進める。

```text
やること：
PoC 1・PoC 2の成果物をもとに、BIM・建設AIナレッジをJSONL化し、簡易検索と根拠付き回答生成を行う。

やらないこと：
本格RAG、クラウド連携、ベクトルDB、Revit自動修正、COBie Checker、FixPriority ML分類、pyRevit v2開発は行わない。

完了目標：
Python / pandas / JSONL / Markdown / pytest により、ローカルで再現可能なRAG-style Knowledge AssistantのMVPをGitHub公開できる状態にする。
```
