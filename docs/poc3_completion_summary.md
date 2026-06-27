# PoC 3 完了まとめ

# BIM / Construction AI Knowledge Assistant PoC

## 1. 概要

本PoCでは、PoC 1・PoC 2で作成したBIM／建設AI関連のナレッジを検索可能な形に整理し、質問に対して**根拠付きで回答するナレッジ検索アシスタント**のMVPを作成した。

このPoCは、LLMによる自由回答生成そのものを目的としたものではなく、以下のような構造を検証するためのものである。

```text
PoC 1：
BIMデータがAI活用に適しているかを評価する

PoC 2：
BIM・建設業務がどのAI/DX活用に適しているかを分類する

PoC 3：
PoC 1・PoC 2の成果物を検索し、根拠付きで説明する
```

全体として、以下の流れを実装した。

```text
データ品質評価
↓
業務ユースケース分類
↓
ナレッジ検索・根拠付き回答
```

---

## 2. GitHubリポジトリ

GitHubリポジトリ：

```text
https://github.com/takahashi-365/bim-construction-ai-knowledge-assistant
```

ローカルフォルダ：

```text
C:\Users\PLS-39\OneDrive - ペーパレススタジオジャパン株式会社\▶成果物\bim-construction-ai-knowledge-assistant
```

Git状態：

```text
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

---

## 3. PoC 1・PoC 2・PoC 3 の関係

| PoC   | テーマ                                        | 役割                           |
| ----- | ------------------------------------------ | ---------------------------- |
| PoC 1 | BIM Data Quality & AI Readiness Assessment | BIMデータ品質とAI活用準備度を評価する        |
| PoC 2 | BIM / Construction AI Use Case Mapper      | BIM・建設業務をAI/DX活用候補に分類する      |
| PoC 3 | BIM / Construction AI Knowledge Assistant  | PoC 1・PoC 2の知識を検索し、根拠付きで説明する |

PoC 3は、PoC 1・PoC 2を置き換えるものではない。
PoC 1・PoC 2で作成したルール、分類、方針、制約、ユースケースを、検索可能なナレッジとして再利用するためのPoCである。

---

## 4. 今回作成したもの

今回のPoC 3では、以下を作成した。

```text
docs/
input/
output/
src/
tests/
README.md
.gitignore
```

主な構成は以下の通り。

```text
bim-construction-ai-knowledge-assistant/
│  .gitignore
│  README.md
│
├─docs
│      answer_policy.md
│      bim_to_ai_workflow_blueprint.md
│      chunk_design.md
│      human_review_policy.md
│      limitations.md
│      metadata_design.md
│      mvp_scope.md
│
├─input
│      poc1_knowledge_samples.csv
│      poc2_knowledge_samples.csv
│      sample_questions_v001.csv
│
├─output
│      rag_documents_v001.jsonl
│      rag_index_v001.json
│      retrieval_results_v001.csv
│      sample_answers_v001.md
│
├─src
│      build_rag_documents.py
│      build_rag_index.py
│      generate_sample_answers.py
│      retrieve_documents.py
│
└─tests
       test_rag_documents.py
       test_rag_index.py
       test_retrieval_results.py
       test_sample_answers.py
```

---

## 5. docs で整理した設計資料

### `docs/mvp_scope.md`

PoC 3のMVP範囲を定義した資料。
今回の対象範囲と対象外を明確にした。

主な方針：

* ローカル環境で動くMVPとする
* Azure AI SearchやOpenAI APIは使わない
* 実案件データや顧客データは使わない
* Revitモデルの自動修正は行わない
* 人間レビュー前提のナレッジ検索とする

---

### `docs/bim_to_ai_workflow_blueprint.md`

PoC 1・PoC 2・PoC 3の関係を整理したブループリント。

整理した流れ：

```text
BIMデータ品質評価
↓
AI Readiness評価
↓
BIM・建設業務ユースケース分類
↓
ナレッジ検索・根拠付き回答
```

---

### `docs/chunk_design.md`

PoC 1・PoC 2のナレッジを、RAG-style documentとして分割する設計を整理した資料。

主なchunk単位：

* BIMデータ品質ルール
* AI Readiness関連情報
* Fix Guide方針
* 建設AI/DXユースケース
* Human Review方針
* Limitations

---

### `docs/metadata_design.md`

RAG-style documentに付与するmetadataを定義した資料。

主なmetadata：

* `category`
* `rule_id`
* `use_case_id`
* `severity`
* `recommended_approach`
* `human_review_required`
* `deep_dive_required`
* `source_file`

---

### `docs/answer_policy.md`

回答生成時の方針を整理した資料。

回答に含める項目：

* Question
* Answer
* Reasoning Summary
* Referenced Sources
* RuleId
* UseCaseId
* RecommendedApproach
* HumanReviewRequired
* DeepDiveRequired
* Caution

重要な注意書き：

```text
この回答は協議用の参考情報です。
設計判断、施工判断、法規判断、安全判断、契約判断は人間レビューが必要です。
AIは最終判断を行いません。
```

---

### `docs/human_review_policy.md`

AIが最終判断を行わない方針を整理した資料。

人間レビューが必要な領域：

* 設計判断
* 施工判断
* 法規判断
* 安全判断
* 契約判断
* コスト判断
* 工程判断
* 顧客向け提案
* Revitモデル変更
* BIMデータ修正方針

---

### `docs/limitations.md`

PoC 3の制約事項を整理した資料。

主な制約：

* キーワード検索のみ
* Embeddingなし
* ベクトルDBなし
* Azure AI Searchなし
* OpenAI APIなし
* Azure OpenAIなし
* LangChain / LlamaIndexなし
* 実案件データなし
* 顧客データなし
* Revitモデルの自動編集なし
* 設計・施工・法規・安全・契約に関する最終判断なし

---

## 6. input で作成したサンプルデータ

### `input/poc1_knowledge_samples.csv`

PoC 1由来のサンプルナレッジ。

含めた内容：

* Door Name Missing Rule
* Room Name Missing Rule
* AI Readiness Score
* RAG Design Policy
* Human Review Policy
* BIMデータ品質に関するルール

---

### `input/poc2_knowledge_samples.csv`

PoC 2由来のサンプルナレッジ。

含めた内容：

* 建設AI/DXユースケース
* Meeting Minutes AI
* Invoice Processing AI
* BIM Data Check
* Construction AI Use Case
* Human Review Policy

---

### `input/sample_questions_v001.csv`

検索・回答生成を確認するためのサンプル質問。

質問数：

```text
35問
```

質問例：

* Door Name Missing Rule は何を意味しますか
* Room Name Missing Rule は何を意味しますか
* AI Readiness Score は何を判断するためのものですか
* HumanReviewRequired=Falseなら人間確認は不要ですか
* GitHub公開時に注意すべき制約は何ですか

---

## 7. src で実装した処理

### `src/build_rag_documents.py`

PoC 1・PoC 2のCSVナレッジを読み込み、RAG-style document形式のJSONLに変換するスクリプト。

生成ファイル：

```text
output/rag_documents_v001.jsonl
```

実行結果：

```text
RAG-style documents generated successfully.
Total documents: 38
PoC1 documents: 16
PoC2 documents: 22
```

---

### `src/build_rag_index.py`

`rag_documents_v001.jsonl` から簡易キーワードインデックスを生成するスクリプト。

生成ファイル：

```text
output/rag_index_v001.json
```

実行結果：

```text
RAG-style keyword index generated successfully.
Total documents: 38
PoC1 documents: 16
PoC2 documents: 22
Unique tokens: 565
```

---

### `src/retrieve_documents.py`

`sample_questions_v001.csv` の質問に対して、関連documentを検索するスクリプト。

生成ファイル：

```text
output/retrieval_results_v001.csv
```

実行結果：

```text
Document retrieval completed successfully.
Questions: 35
Retrieval result rows: 105
No-result rows: 0
Top K: 3
```

---

### `src/generate_sample_answers.py`

検索結果をもとに、根拠付き回答Markdownを生成するスクリプト。

生成ファイル：

```text
output/sample_answers_v001.md
```

実行結果：

```text
Sample grounded answers generated successfully.
Questions: 35
No-result questions: 0
```

この回答生成はテンプレートベースであり、LLMによる自由生成ではない。

---

## 8. output で生成した成果物

### `output/rag_documents_v001.jsonl`

PoC 1・PoC 2のサンプルナレッジをRAG-style documentとして変換したJSONL。

件数：

```text
38 documents
```

内訳：

```text
PoC1 documents: 16
PoC2 documents: 22
```

---

### `output/rag_index_v001.json`

簡易キーワードインデックス。

特徴：

* `simple_keyword_index`
* Embeddingなし
* ベクトルDBなし
* ローカルMVP用の検索インデックス

---

### `output/retrieval_results_v001.csv`

35問に対する検索結果。

結果：

```text
Questions: 35
Retrieval result rows: 105
No-result rows: 0
Top K: 3
```

---

### `output/sample_answers_v001.md`

検索結果に基づく根拠付き回答Markdown。

含まれる項目：

* Question
* Answer
* Reasoning Summary
* Referenced Sources
* Metadata Summary
* HumanReviewRequired
* DeepDiveRequired
* Caution

---

## 9. pytestによる検証結果

最終的に、以下の4つのテストファイルを作成した。

```text
tests/test_rag_documents.py
tests/test_rag_index.py
tests/test_retrieval_results.py
tests/test_sample_answers.py
```

全テスト結果：

```text
collected 90 items

tests/test_rag_documents.py ...................
tests/test_rag_index.py ........................
tests/test_retrieval_results.py ......................
tests/test_sample_answers.py .........................

90 passed in 0.20s
```

合計：

```text
90 passed
```

---

## 10. テスト内容の概要

### `tests/test_rag_documents.py`

`output/rag_documents_v001.jsonl` を検証。

確認内容：

* ファイルが存在する
* documentが空ではない
* 必須フィールドが存在する
* metadataが存在する
* `document_id` が重複していない
* PoC 1 / PoC 2 のdocumentが含まれている
* RuleMaster / UseCaseMapping が含まれている
* HumanReviewRequired / DeepDiveRequired が含まれている
* Door / Room の代表ルールが含まれている
* UseCaseIdが含まれている
* 禁止表現が含まれていない

結果：

```text
19 passed
```

---

### `tests/test_rag_index.py`

`output/rag_index_v001.json` を検証。

確認内容：

* ファイルが存在する
* 必須フィールドが存在する
* `index_type` が `simple_keyword_index` である
* document数が一致している
* token数が一致している
* inverted index が存在する
* 重要な検索語が含まれている
* PoC 1 / PoC 2 のsourceが含まれている
* RuleMaster / UseCaseMapping が含まれている
* 禁止表現が含まれていない

結果：

```text
24 passed
```

---

### `tests/test_retrieval_results.py`

`output/retrieval_results_v001.csv` を検証。

確認内容：

* ファイルが存在する
* 35問が含まれている
* 全質問に検索結果がある
* No-result が0件である
* Rank / Score が入っている
* Top K が3件以内である
* Q001 が D-001 を取得できている
* Q004 が R-101 を取得できている
* Q013 が UC-001 を取得できている
* HumanReviewRequired / DeepDiveRequired が含まれている
* PoC 1 / PoC 2 のsourceが含まれている
* RuleMaster / UseCaseMapping が含まれている

結果：

```text
22 passed
```

---

### `tests/test_sample_answers.py`

`output/sample_answers_v001.md` を検証。

確認内容：

* ファイルが存在する
* 35問分の回答セクションがある
* Answer / Reasoning Summary / Referenced Sources がある
* Metadata Summary がある
* HumanReviewRequired / DeepDiveRequired / Caution がある
* 参照元が含まれている
* No-resultの回答が残っていない
* 人間レビューの注意書きが含まれている
* Revit自動修正を行わない制約が含まれている
* Door / Room / UseCase の代表例が含まれている
* 禁止表現が含まれていない

結果：

```text
25 passed
```

---

## 11. READMEの整備

READMEは当初英語が多い内容だったが、日本語メインに修正した。

修正方針：

* 日本語メイン
* 必要な技術語のみ英語
* PoC 1・PoC 2・PoC 3の関係を明確化
* 処理フローを可視化
* GitHub閲覧者が内容を理解しやすい構成

READMEにはMermaid図を追加した。

追加した図：

1. PoC全体の関係図
2. 処理フロー図
3. 回答生成の考え方

README更新コミット：

```text
Add Mermaid diagrams to Japanese README
```

---

## 12. GitHub公開整理

ローカルGitリポジトリを初期化し、GitHubにpushした。

実施内容：

```text
git init
git branch -M main
git add .
git commit -m "Initial commit: BIM Construction AI Knowledge Assistant PoC"
git remote add origin https://github.com/takahashi-365/bim-construction-ai-knowledge-assistant.git
git push -u origin main
```

初回コミット：

```text
Initial commit: BIM Construction AI Knowledge Assistant PoC
```

README日本語版・Mermaid図追加後のコミット：

```text
Add Mermaid diagrams to Japanese README
```

最終状態：

```text
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

---

## 13. 今回の技術的ポイント

今回のPoCで示せた技術的ポイントは以下である。

### 1. BIM・建設AIナレッジを検索可能な形に構造化した

PoC 1・PoC 2の成果物を、単なるMarkdownやCSVとしてではなく、RAG-style documentとして再構成した。

これにより、以下のようなmetadata付きナレッジとして扱えるようになった。

* source_poc
* source_type
* rule_id
* use_case_id
* recommended_approach
* human_review_required
* deep_dive_required
* source_file

---

### 2. RAGの前段階となるdocument設計を実装した

本番RAGではないが、将来的にAzure AI SearchやEmbedding検索に移行しやすいよう、JSONL形式でdocumentを作成した。

今回の設計は、以下に拡張しやすい。

* Azure AI Search
* Vector Search
* Embedding
* Azure OpenAI回答生成
* 社内ナレッジ検索
* BIMデータ品質説明アシスタント

---

### 3. 簡易キーワード検索でMVPを成立させた

外部AI APIやベクトルDBに依存せず、まずローカルで検索・参照・回答生成の流れを実装した。

これにより、以下を確認できた。

* どのmetadataが必要か
* どのchunk単位が扱いやすいか
* 質問とdocumentの対応が取れるか
* No-resultを検出できるか
* 参照元付き回答に必要な情報が揃っているか

---

### 4. Grounded Answerの形式を作成した

回答には、単なる回答文だけではなく、以下を含めるようにした。

* Reasoning Summary
* Referenced Sources
* Metadata Summary
* HumanReviewRequired
* DeepDiveRequired
* Caution

これにより、AI回答をそのまま信じるのではなく、参照元と判断条件を確認できる形式にした。

---

### 5. Human Review前提の安全な回答方針を組み込んだ

AIが設計判断、施工判断、法規判断、安全判断、契約判断を行わないことを明示した。

特に以下を重要方針とした。

```text
AIは最終判断を行いません。
```

また、`HumanReviewRequired=False` は「人間確認不要」という意味ではないことも明記した。

---

### 6. pytestで成果物の品質を検証した

生成物を作って終わりではなく、以下のファイルをpytestで検証した。

* RAG-style document
* simple keyword index
* retrieval results
* sample answers

最終結果として、90件のテストがすべて通った。

```text
90 passed
```

---

## 14. 今回の成果

今回のPoC 3で得られた成果は以下である。

### 成果1：PoC 1・PoC 2をつなぐ第3の成果物を作成できた

PoC 1はBIMデータ品質評価。
PoC 2は建設AI/DXユースケース分類。
PoC 3では、それらを検索・説明可能なナレッジとしてつなげることができた。

---

### 成果2：BIM×AIのポートフォリオにストーリーができた

単発のPython処理ではなく、以下の流れを説明できるようになった。

```text
BIMデータを評価する
↓
AI活用可能性を整理する
↓
蓄積した知識を検索・説明する
```

これは、BIM×AIコンサル、AI導入支援、建設AIエンジニア候補として説明しやすい構成である。

---

### 成果3：GitHubで見せられる状態まで整理できた

以下が完了している。

* README整備
* Mermaid図追加
* docs整理
* input/output整理
* src整理
* tests整理
* pytest 90 passed
* GitHub push完了

---

### 成果4：本番RAGに進む前の設計検証ができた

いきなりAzure AI SearchやOpenAI APIを使うのではなく、まずローカルで以下を検証できた。

* document設計
* metadata設計
* chunk設計
* 質問設計
* 回答フォーマット
* 参照元表示
* 人間レビュー方針
* 制約事項

---

## 15. 現時点の制約

このPoCはあくまでMVPであり、以下の制約がある。

* 検索はキーワードベース
* Embedding検索ではない
* ベクトルDBは使っていない
* Azure AI Searchは使っていない
* OpenAI API / Azure OpenAIは使っていない
* 回答生成はテンプレートベース
* 実案件データは使っていない
* 顧客データは使っていない
* Revitモデルの自動編集は行わない
* 本番利用を想定したセキュリティ設計は未実装

---

## 16. 今後の拡張候補

今後の拡張候補は以下。

### 技術面

* Embedding検索の追加
* Azure AI Search対応
* Azure OpenAIによる回答生成
* Streamlit UIの追加
* 参照元document表示機能
* confidence scoreの追加
* 回答比較機能
* feedback loopの追加

---

### BIMナレッジ面

* BIMルールカテゴリの追加
* Door / Room以外のカテゴリ追加
* COBie / FMナレッジの追加
* pyRevit metadata exportナレッジの追加
* BIM実行計画・BEP関連ナレッジの追加
* BIMモデル品質チェックルールの拡充

---

### 建設AIユースケース面

* 建設AIユースケースの追加
* 業務トリアージ結果との連携
* AI/DXサービス分類との連携
* 顧客向け提案テンプレートへの展開
* Operation: RECODEとの接続

---

### ポートフォリオ面

* PoC 1・PoC 2・PoC 3をまとめたPortfolio READMEの作成
* ビズリーチ記載内容への反映
* 職務経歴書への反映
* 面接説明用の1ページ要約作成
* 図解入りのポートフォリオPDF作成

---

## 17. ビズリーチ・職務経歴書に書ける要点

以下のように記載できる。

```text
BIMデータ品質評価PoC、建設AI/DXユースケース分類PoCの成果物をもとに、
BIM・建設AIナレッジを検索し、参照元付きで回答するローカルRAG-styleナレッジアシスタントを構築。

PythonでCSVナレッジをJSONL形式のRAG-style documentへ変換し、
metadata、RuleId、UseCaseId、HumanReviewRequired、DeepDiveRequiredを付与。
簡易キーワードインデックス、質問検索、根拠付き回答Markdown生成までを実装。

成果物はpytestで検証し、RAG document、index、retrieval results、sample answersに対して
90件のテストを作成・全件通過。
GitHub上にREADME、Mermaid図、設計docs、src、testsを整理して公開。
```

短く書く場合：

```text
BIMデータ品質評価・建設AIユースケース分類の知識を検索可能なRAG-style documentへ構造化し、
根拠付き回答を生成するローカルMVPをPythonで実装。
JSONL化、簡易キーワード検索、参照元付き回答生成、pytest検証までを行い、
90件のテストを全件通過させた。
```

---

## 18. 面接・説明時に使える要約

このPoCを説明する場合は、以下のように説明できる。

```text
PoC 1では、BIMデータがAI活用に適しているかを評価しました。
PoC 2では、BIM・建設業務がどのAI/DX活用に向いているかを分類しました。
PoC 3では、それらの成果物を検索できるナレッジとして整理し、
質問に対して参照元付きで回答するローカルRAG-styleアシスタントを作りました。

まだAzure AI SearchやOpenAI APIは使っていませんが、
RAGに進む前段階として、document設計、metadata設計、検索結果、回答フォーマット、
人間レビュー方針、制約事項を整理し、pytestで90件の検証を行いました。
```

---

## 19. 完了ステータス

PoC 3の完了ステータスは以下。

```text
Step 1：プロジェクトフォルダ作成　完了
Step 2：docs設計資料作成　完了
Step 3：inputサンプル作成　完了
Step 4：RAG-style document JSONL生成　完了
Step 5：簡易インデックス生成　完了
Step 6：検索処理実装　完了
Step 7：根拠付き回答生成　完了
Step 8：出力確認・サンプルレビュー　完了
Step 9：pytest作成・検証　完了
Step 10：README作成　完了
Step 11：GitHub公開整理　完了
Step 12：完了まとめ作成　完了
```

---

## 20. 最終結果

最終的に、PoC 3は以下の状態まで完了した。

```text
GitHub公開：完了
README日本語メイン化：完了
Mermaid図追加：完了
docs作成：完了
input作成：完了
output生成：完了
src実装：完了
tests作成：完了
pytest：90 passed
working tree clean：確認済み
```

このPoCにより、BIMデータ品質評価、建設AI/DXユースケース分類、ナレッジ検索・根拠付き回答生成という一連の流れを、GitHub上で説明できる状態に整理できた。
