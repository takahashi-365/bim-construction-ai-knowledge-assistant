# Limitations

## 1. このドキュメントの目的

このドキュメントは、PoC 3：BIM / Construction AI Knowledge Assistant の制約事項、対象外、注意点を定義するための設計資料である。

PoC 3は、PoC 1・PoC 2の成果物を検索対象ナレッジとして整理し、質問に対して関連documentを検索し、根拠付き回答を生成するローカルRAG-styleナレッジアシスタントMVPである。

ただし、このPoCは本格的なRAGシステム、クラウドAIサービス、業務システム、Revit自動修正ツールではない。

このドキュメントでは、以下を明確にする。

```text
MVPでできること
MVPでできないこと
本格RAGとの違い
検索精度の制約
回答生成の制約
Human Review上の制約
データ利用上の制約
GitHub公開時の注意
将来的な拡張候補
```

---

## 2. PoC 3の前提

PoC 3は、個人開発ポートフォリオとして作成する。

目的は、BIMデータ品質評価、AI Readiness評価、建設業務ユースケース分類、RAG-styleナレッジ検索、Human Review設計を一連の流れとして説明できるようにすることである。

PoC 3の目的は、AIが最終判断を行うことではない。

PoC 3の回答は、BIM担当者、設計者、施工担当者、AI/DX導入担当者、関係者が確認・協議するための参考情報として扱う。

---

## 3. MVPでできること

PoC 3のMVPでできることは以下である。

```text
PoC 1由来のサンプルナレッジを扱う
PoC 2由来のサンプルナレッジを扱う
サンプル質問を扱う
RAG-style document JSONLを生成する
簡易検索インデックスを生成する
キーワードベースで関連documentを検索する
検索結果CSVを生成する
根拠付き回答Markdownを生成する
回答に参照元を含める
HumanReviewRequiredを回答に反映する
DeepDiveRequiredを回答に反映する
pytestで主要な出力と方針を検証する
```

MVPでは、ローカル環境で再現可能な最小構成を優先する。

---

## 4. MVPでできないこと

PoC 3のMVPでは、以下はできない。

```text
本格的なベクトル検索
Embeddingによる意味検索
Azure AI Searchの本実装
Azure OpenAI API連携
OpenAI API連携
LangChain / LlamaIndexの本格利用
FAISS / Chromaの本格利用
自然言語生成AIによる自由回答生成
Revitモデルの自動修正
Revit API / pyRevit v2の新規開発
COBie Checkerの実装
FixPriority分類モデルの実装
Construction AI PoC Planning Toolkit完全版
実案件データの処理
顧客データの処理
社内サービス詳細の公開
業務判断の自動化
設計・施工・法規・安全・契約判断の代替
```

このPoCは、あくまでRAG-style Knowledge Assistantの基本構造を示すMVPである。

---

## 5. 本格RAGではなくRAG-styleである

PoC 3は、本格RAGではなくRAG-style構成である。

ここでいうRAG-styleとは、以下の意味である。

```text
検索対象ナレッジをdocument化する
documentにmetadataを付与する
質問に対して関連documentを検索する
検索結果に基づいて回答案を生成する
回答に参照元を含める
```

一方で、MVPでは以下を行わない。

```text
Embedding生成
ベクトル検索
類似度検索の高度化
LLMによる自由生成
クラウド検索基盤の利用
RAG評価指標の本格運用
プロンプトチェーンの設計
```

READMEやポートフォリオでは、PoC 3を「RAG-style Knowledge Assistant」と表現する。

「本格RAGを実装した」とは表現しない。

---

## 6. 検索精度の制約

PoC 3のMVPでは、簡易キーワード検索を前提とする。

そのため、検索精度には以下の制約がある。

```text
意味的に近いがキーワードが一致しない質問に弱い
表記ゆれに弱い
日本語・英語の混在に影響を受ける
類義語や専門用語の揺れを十分に吸収できない
長い質問の意図理解には限界がある
検索順位は簡易スコアに依存する
関連性の低いdocumentが検索される可能性がある
関連するdocumentが検索されない可能性がある
```

この制約に対応するため、MVPではkeywordsに日本語・英語の両方を入れる。

ただし、それでも本格的な意味検索と同等の精度は期待しない。

---

## 7. 回答生成の制約

PoC 3のMVPでは、回答は検索結果をもとにしたテンプレート生成を基本とする。

そのため、回答生成には以下の制約がある。

```text
LLMのような自然な自由回答は行わない
検索結果にない情報は回答できない
複雑な文脈理解は行わない
複数document間の高度な推論は行わない
回答品質は入力ナレッジと検索結果に依存する
回答は協議用の参考情報であり、最終判断ではない
```

PoC 3の回答では、以下を重視する。

```text
参照元が分かること
RuleIdまたはUseCaseIdが確認できること
HumanReviewRequiredが確認できること
DeepDiveRequiredが確認できること
Cautionが含まれること
AIが最終判断しないこと
```

---

## 8. Human Review上の制約

PoC 3では、AIが最終判断を行わない。

以下の判断は、必ず人間レビューを前提とする。

```text
設計判断
施工判断
法規判断
安全判断
契約判断
コスト判断
工程判断
品質保証上の判断
顧客合意が必要な判断
BIMモデルの正式修正判断
社内外への正式提出判断
```

PoC 3は、これらの判断に必要な情報を整理するための支援ツールである。

判断そのものを代替するものではない。

---

## 9. Revitモデル修正の制約

PoC 3では、Revitモデルの自動修正は行わない。

品質チェックやFix Guideで修正候補が示された場合でも、AIがRevitモデルを直接変更することはしない。

PoC 3で行うことは以下である。

```text
品質問題の意味を説明する
関連するRuleIdを示す
関連するFix Guideを示す
確認ポイントを示す
Human Reviewが必要な理由を示す
```

PoC 3で行わないことは以下である。

```text
Revitモデルを自動修正する
正しいパラメータ値を自動確定する
BIMモデルを自動承認する
人間確認なしでモデル更新する
pyRevit v2を新規開発する
```

---

## 10. AI/DX自動化の制約

PoC 3では、PoC 2由来のAI/DXユースケース分類を検索対象として扱う。

ただし、ある業務が自動化候補に分類されていても、それは完全自動化を意味しない。

AutomationSuitable=True や Automation Support は、以下の意味で扱う。

```text
自動化支援の候補である
作業補助や候補提示に使える可能性がある
最終判断は人間が行う
HumanReviewRequired=Trueの場合は人間レビュー必須
DeepDiveRequired=Trueの場合は追加確認が必要
```

PoC 3では、AI/DX活用方針を確定するのではなく、協議のための材料を提示する。

---

## 11. Deep Diveに関する制約

DeepDiveRequired=True の場合、PoC 3は追加確認が必要であることを示す。

ただし、PoC 3自体が追加ヒアリングや業務分析を完了するわけではない。

Deep Diveが必要な場合、確認すべき内容の例は以下である。

```text
入力情報
出力情報
判断条件
業務範囲
関係者
成果物の利用目的
AI/DX適用範囲
自動化してよい範囲
人間確認が必要な範囲
```

PoC 3では、Deep Diveが必要な論点を示すことはできる。

しかし、実際の業務ヒアリングや関係者合意までは行わない。

---

## 12. データ利用上の制約

PoC 3では、実案件データ、顧客データ、社内サービス詳細は使用しない。

使用するデータは、ポートフォリオ用のサンプルナレッジに限定する。

使用しない情報は以下である。

```text
実案件名
顧客名
顧客担当者名
顧客固有のBIMデータ
社内サービスの詳細情報
契約情報
金額情報
非公開資料名
個人情報
実プロジェクト固有の判断内容
Revitモデルの実データ
機密性のあるBIM属性
```

GitHub公開を前提とするため、公開可能なサンプルデータのみを使用する。

---

## 13. 入力データの制約

PoC 3のMVPでは、PoC 1・PoC 2の実ファイルを大量に取り込むのではなく、サンプルナレッジCSVを作成して扱う。

入力データは以下を想定する。

```text
input/poc1_knowledge_samples.csv
input/poc2_knowledge_samples.csv
input/sample_questions_v001.csv
```

これらは、PoCの考え方を説明するためのサンプルである。

実案件の完全なナレッジベースではない。

---

## 14. 出力データの制約

PoC 3のMVPで生成する出力は以下である。

```text
output/rag_documents_v001.jsonl
output/rag_index_v001.json
output/retrieval_results_v001.csv
output/sample_answers_v001.md
```

これらの出力は、PoC 3の処理結果を説明するための成果物である。

実運用の正式な判断資料ではない。

回答Markdownも、協議用の参考情報として扱う。

---

## 15. pytestの制約

PoC 3では、pytestで主要な出力と方針を確認する。

ただし、pytestで確認できるのは、主に以下である。

```text
ファイルが存在すること
必須項目が存在すること
PoC 1由来のdocumentが存在すること
PoC 2由来のdocumentが存在すること
回答に参照元が含まれること
Human Review注意書きが含まれること
禁止表現が含まれていないこと
```

pytestでは、以下を完全には保証できない。

```text
検索結果の意味的な正しさ
回答内容の専門的妥当性
設計・施工・法規・安全・契約判断の正しさ
実案件への適用可否
利用者が誤用しないこと
```

pytestは、PoCとしての再現性と最低限の品質確認を目的とする。

---

## 16. GitHub公開時の注意

PoC 3はGitHub公開を前提とするため、以下に注意する。

```text
実案件データを含めない
顧客データを含めない
社内サービス詳細を含めない
非公開資料を含めない
個人情報を含めない
APIキーを含めない
クラウド接続情報を含めない
Revitモデル実データを含めない
誤解を招く表現を避ける
本格RAGとして誇張しない
AIが最終判断するように見える表現を避ける
```

READMEでは、PoC 3が個人開発ポートフォリオであり、ローカルRAG-style MVPであることを明記する。

---

## 17. 誇張しない表現

PoC 3では、以下のような表現は避ける。

```text
本格RAGを実装した
建設業務をAIで自動判断できる
BIMデータをAIが自動修正できる
設計判断をAIで代替できる
施工判断をAIで代替できる
法規判断をAIで代替できる
実案件にそのまま適用できる
高精度な意味検索を実装した
AIが正しい回答を保証する
```

代わりに、以下の表現を使う。

```text
RAG-style Knowledge Assistant
ローカルで再現可能なMVP
簡易キーワード検索
根拠付き回答サンプル
協議用の参考情報
Human Reviewを前提とした回答設計
PoC 1・PoC 2成果物の再利用
将来的なRAG拡張を見据えた基礎設計
```

---

## 18. 禁止表現

PoC 3では、以下の表現を回答、docs、README、sample outputに含めない。

```text
AIが最終判断します
AIが自動で承認します
AIが設計判断します
AIが施工判断します
AIが法規判断します
AIが安全判断します
AIが契約判断します
Revitモデルを自動修正します
人間確認は不要です
確認なしで実行できます
この判断は確定です
必ず正しいです
```

これらは、pytestでも禁止表現として検出対象にする。

---

## 19. 推奨表現

PoC 3では、以下の表現を推奨する。

```text
検索結果に基づく回答案です
協議用の参考情報です
人間レビューが必要です
追加確認が必要です
可能性があります
参照元では以下のように整理されています
このPoCでは自動修正は行いません
最終判断は関係者が行う必要があります
AIは最終判断を行いません
RAG-style構成です
ローカルMVPです
```

これらの表現により、PoC 3の責任範囲を明確にする。

---

## 20. 将来的な拡張候補

PoC 3のMVP完了後、将来的に以下を検討できる。

```text
TF-IDF検索
scikit-learnによる簡易類似度検索
FAISSの試験利用
Chromaの試験利用
Embedding生成
Azure AI Search設計
Azure OpenAI API連携設計
OpenAI API連携設計
Streamlit UI
回答評価用のサンプル質問追加
検索スコア改善
metadataフィルタ検索
PoC 1・PoC 2成果物の取り込み拡張
```

ただし、これらはMVP対象外である。

PoC 3では、まずPython / pandas / JSONL / Markdown / pytest で完結するローカルMVPを優先する。

---

## 21. 将来的な拡張時にも維持する方針

将来的に本格RAGやクラウド連携へ拡張する場合でも、以下の方針は維持する。

```text
AIは最終判断しない
回答には参照元を含める
Human Reviewが必要な判断を明示する
Deep Diveが必要な場合は追加確認を促す
Revitモデルの自動修正を前提にしない
実案件データや顧客データを無断で使わない
本格実装とMVPを明確に区別する
```

実装が高度になっても、PoC 3の責任範囲は「判断支援」であり、「最終判断」ではない。

---

## 22. 制約を明記する理由

PoC 3で制約を明記する理由は以下である。

```text
GitHub閲覧者に誤解を与えないため
本格RAG実装と誤認されないため
AIが設計・施工判断を代替すると誤解されないため
実案件データを使っていると誤解されないため
ポートフォリオとしての責任範囲を明確にするため
Human Review方針を一貫させるため
```

制約を明記することは、PoCの価値を下げるためではない。

むしろ、AI/DX導入における責任範囲、データ利用、Human Reviewの重要性を理解していることを示すために必要である。

---

## 23. READMEへの反映方針

READMEでは、limitations.mdの内容を短く要約して掲載する。

READMEに記載するべき制約は以下である。

```text
This is a local RAG-style MVP, not a production RAG system.
No customer data, project data, or confidential service data is used.
No Revit model is automatically modified.
Answers are discussion references, not final decisions.
Human review is required for design, construction, legal, safety, and contractual decisions.
```

日本語で記載する場合は以下。

```text
このPoCは、本格RAGではなくローカルRAG-style MVPです。
実案件データ、顧客データ、社内サービス詳細は使用していません。
Revitモデルの自動修正は行いません。
回答は最終判断ではなく、協議用の参考情報です。
設計判断、施工判断、法規判断、安全判断、契約判断には人間レビューが必要です。
```

---

## 24. まとめ

PoC 3：BIM / Construction AI Knowledge Assistant は、PoC 1・PoC 2の成果物を検索対象にし、根拠付きで説明するローカルRAG-styleナレッジアシスタントMVPである。

ただし、以下の制約がある。

```text
本格RAGではない
クラウドAIサービスとは連携しない
EmbeddingやVector DBは使わない
LLMによる自由生成は行わない
実案件データや顧客データは使わない
Revitモデルの自動修正は行わない
AIが最終判断しない
検索精度や回答品質にはMVPとしての限界がある
```

PoC 3の価値は、これらの制約を理解したうえで、以下を示すことである。

```text
BIMデータ品質
AI Readiness
建設業務ユースケース分類
RAG-styleナレッジ検索
根拠付き回答生成
Human Review設計
```

このlimitations.mdにより、PoC 3の責任範囲、対象外、公開時の注意点を明確にし、個人開発ポートフォリオとして誤解なく説明できる状態にする。
