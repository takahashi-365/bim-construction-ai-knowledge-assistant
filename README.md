# BIM / Construction AI Knowledge Assistant PoC

## Overview

This repository is a local MVP PoC for a **RAG-style knowledge assistant** that searches BIM data quality knowledge and construction AI/DX use case knowledge, then generates grounded sample answers with referenced sources.

The purpose of this PoC is to connect the results of previous BIM / Construction AI portfolio projects into a searchable knowledge assistant.

```text
PoC 1:
BIMデータがAI活用に適しているかを評価する

PoC 2:
BIM・建設業務がどのAI/DX活用に適しているかを分類する

PoC 3:
PoC 1・PoC 2の成果物を検索し、根拠付きで説明する
```

Overall flow:

```text
データ品質評価
↓
業務ユースケース分類
↓
ナレッジ検索・根拠付き回答
```

This PoC is designed as a small, local, explainable MVP.
It does not use cloud AI services, vector databases, embeddings, or real project data.

---

## Project Goal

The goal of this PoC is to demonstrate a basic knowledge assistant workflow for BIM and construction AI use cases.

It answers questions such as:

* What does a BIM data quality rule mean?
* Which BIM quality issues require human review?
* Which construction AI/DX use case is related to a given task?
* What limitations should be considered when publishing or using this PoC?
* Which source document was used as the basis of an answer?

The key point is not free text generation.
The key point is **grounded answer generation with traceable sources**.

---

## Positioning in Portfolio

This repository is PoC 3 in the BIM / Construction AI portfolio sequence.

| PoC   | Theme                                      | Role                                                            |
| ----- | ------------------------------------------ | --------------------------------------------------------------- |
| PoC 1 | BIM Data Quality & AI Readiness Assessment | Evaluates BIM data quality and AI readiness                     |
| PoC 2 | BIM / Construction AI Use Case Mapper      | Maps BIM/construction work to AI/DX use cases                   |
| PoC 3 | BIM / Construction AI Knowledge Assistant  | Searches PoC 1 / PoC 2 knowledge and generates grounded answers |

PoC 3 does not replace PoC 1 or PoC 2.
Instead, it uses their outputs as searchable knowledge.

---

## What This PoC Does

This PoC performs the following steps:

1. Reads sample knowledge from CSV files
2. Converts PoC 1 / PoC 2 knowledge into RAG-style JSONL documents
3. Builds a simple keyword-based index
4. Retrieves related documents for sample questions
5. Generates grounded sample answers in Markdown
6. Validates outputs with pytest

---

## What This PoC Does Not Do

This MVP intentionally does not include the following:

* Azure AI Search implementation
* Azure OpenAI / OpenAI API calls
* LangChain / LlamaIndex
* Embeddings
* Vector database
* FAISS / Chroma
* Production RAG pipeline
* Real customer data
* Real project data
* Revit model modification
* Automatic BIM correction
* Legal, safety, design, construction, or contract decision-making

This is a local MVP to demonstrate the structure and logic of a grounded BIM / Construction AI knowledge assistant.

---

## Repository Structure

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

## Main Inputs

### `input/poc1_knowledge_samples.csv`

Sample knowledge from PoC 1.

This includes BIM data quality rules, AI readiness concepts, RAG design policies, and human review policies.

Examples:

* Door Name Missing Rule
* Room Name Missing Rule
* AI Readiness Score
* RAG Design Policy
* Human Review Policy

### `input/poc2_knowledge_samples.csv`

Sample knowledge from PoC 2.

This includes construction AI/DX use case mapping knowledge.

Examples:

* Meeting Minutes AI
* Invoice Processing AI
* BIM Data Check
* Human Review Policy
* Construction AI use case categories

### `input/sample_questions_v001.csv`

Sample questions used to test the retrieval and answer generation flow.

This file contains 35 questions.

Examples:

* Door Name Missing Rule は何を意味しますか
* Room Name Missing Rule は何を意味しますか
* AI Readiness Score は何を判断するためのものですか
* HumanReviewRequired=Falseなら人間確認は不要ですか
* GitHub公開時に注意すべき制約は何ですか

---

## Main Outputs

### `output/rag_documents_v001.jsonl`

RAG-style document file generated from the PoC 1 / PoC 2 sample knowledge.

Each line is one JSON document.

Main fields:

* `document_id`
* `source_poc`
* `source_type`
* `title`
* `content`
* `metadata`
* `keywords`

Example document structure:

```json
{
  "document_id": "P1-RULE-D001",
  "source_poc": "PoC1",
  "source_type": "RuleMaster",
  "title": "Door Name Missing Rule",
  "content": "...",
  "metadata": {
    "category": "Door",
    "rule_id": "D-001",
    "use_case_id": "",
    "severity": "Medium",
    "recommended_approach": "Human Review",
    "human_review_required": true,
    "deep_dive_required": false,
    "source_file": "poc1_knowledge_samples.csv"
  },
  "keywords": [
    "Door",
    "Name",
    "Missing",
    "Rule"
  ]
}
```

### `output/rag_index_v001.json`

Simple keyword index generated from `rag_documents_v001.jsonl`.

This is not a vector index.
It is not an embedding index.
It is a local keyword-based MVP index.

Main fields:

* `index_version`
* `index_type`
* `description`
* `document_count`
* `token_count`
* `documents`
* `inverted_index`

### `output/retrieval_results_v001.csv`

Search result file generated from `sample_questions_v001.csv`.

Each question retrieves up to Top 3 related documents.

Main fields:

* `QuestionId`
* `Question`
* `Rank`
* `DocumentId`
* `SourcePoC`
* `SourceType`
* `Title`
* `MatchedKeywords`
* `Score`
* `RuleId`
* `UseCaseId`
* `RecommendedApproach`
* `HumanReviewRequired`
* `DeepDiveRequired`
* `SourceFile`

### `output/sample_answers_v001.md`

Grounded sample answers generated from retrieval results.

Each answer includes:

* Question
* Answer
* Reasoning Summary
* Referenced Sources
* Metadata Summary
* HumanReviewRequired
* DeepDiveRequired
* Caution

This output is template-based.
It is not LLM-based free generation.

---

## Workflow

### Step 1: Build RAG-style documents

```powershell
python src/build_rag_documents.py
```

Expected output:

```text
RAG-style documents generated successfully.
Total documents: 38
PoC1 documents: 16
PoC2 documents: 22
```

Generated file:

```text
output/rag_documents_v001.jsonl
```

---

### Step 2: Build simple keyword index

```powershell
python src/build_rag_index.py
```

Expected output:

```text
RAG-style keyword index generated successfully.
Total documents: 38
PoC1 documents: 16
PoC2 documents: 22
Unique tokens: 565
```

Generated file:

```text
output/rag_index_v001.json
```

---

### Step 3: Retrieve documents for sample questions

```powershell
python src/retrieve_documents.py
```

Expected output:

```text
Document retrieval completed successfully.
Questions: 35
Retrieval result rows: 105
No-result rows: 0
Top K: 3
```

Generated file:

```text
output/retrieval_results_v001.csv
```

---

### Step 4: Generate grounded sample answers

```powershell
python src/generate_sample_answers.py
```

Expected output:

```text
Sample grounded answers generated successfully.
Questions: 35
No-result questions: 0
```

Generated file:

```text
output/sample_answers_v001.md
```

---

## Test

Run all tests:

```powershell
pytest
```

Current result:

```text
collected 90 items

tests/test_rag_documents.py ...................
tests/test_rag_index.py ........................
tests/test_retrieval_results.py ......................
tests/test_sample_answers.py .........................

90 passed in 0.20s
```

---

## Test Coverage

### `tests/test_rag_documents.py`

Validates:

* `rag_documents_v001.jsonl` exists
* Documents are not empty
* Required fields exist
* Metadata fields exist
* `document_id` values are unique
* PoC 1 and PoC 2 documents exist
* RuleMaster and UseCaseMapping documents exist
* HumanReviewRequired / DeepDiveRequired values exist
* Door / Room rule documents exist
* UseCaseId documents exist
* Prohibited final-decision phrases are not included

### `tests/test_rag_index.py`

Validates:

* `rag_index_v001.json` exists
* Index has required fields
* Index type is `simple_keyword_index`
* Document count matches
* Token count matches
* Inverted index exists
* Expected terms exist
* PoC 1 and PoC 2 sources exist
* RuleMaster and UseCaseMapping sources exist
* Prohibited final-decision phrases are not included

### `tests/test_retrieval_results.py`

Validates:

* `retrieval_results_v001.csv` exists
* 35 questions exist
* All questions have retrieval results
* No-result rows are zero
* Rank and Score exist
* Top K is limited to 3
* Q001 retrieves D-001
* Q004 retrieves R-101
* Q013 retrieves UC-001
* HumanReviewRequired / DeepDiveRequired are included
* PoC 1 and PoC 2 sources are included
* RuleMaster and UseCaseMapping sources are included

### `tests/test_sample_answers.py`

Validates:

* `sample_answers_v001.md` exists
* 35 answer sections exist
* Answer / Reasoning Summary / Referenced Sources sections exist
* Metadata Summary exists
* HumanReviewRequired / DeepDiveRequired / Caution sections exist
* Referenced sources are included
* No missing referenced source remains
* Human review caution is included
* Revit auto-modification limitation is included
* Door / Room / UseCase examples are included
* Prohibited final-decision phrases are not included outside question headings

---

## Answer Policy

This PoC follows a grounded answer policy.

Answers should include:

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

Important policy:

```text
この回答は協議用の参考情報です。
設計判断、施工判断、法規判断、安全判断、契約判断は人間レビューが必要です。
AIは最終判断を行いません。
```

---

## Human Review Policy

AI does not make final decisions.

Human review is required for:

* Design decisions
* Construction decisions
* Legal decisions
* Safety decisions
* Contract decisions
* Cost decisions
* Schedule decisions
* Client-facing recommendations
* Revit model changes
* BIM data correction policies

`HumanReviewRequired=False` does not mean that human confirmation is unnecessary.
It only means that the retrieved knowledge item is not flagged as requiring special human review in this MVP metadata.

---

## Limitations

This is a local MVP.

Current limitations:

* Keyword-based search only
* No embeddings
* No vector database
* No Azure AI Search implementation
* No OpenAI API call
* No Azure OpenAI call
* No LangChain / LlamaIndex
* No production security design
* No real customer data
* No real project data
* No confidential internal data
* No automatic Revit model editing
* No legal, safety, design, construction, or contract final decision

---

## Public Repository Policy

This repository is intended for portfolio and learning purposes.

When publishing to GitHub:

* Use only sample data
* Do not include customer data
* Do not include project-specific confidential data
* Do not include real building model data
* Do not include internal company documents
* Do not include credentials, API keys, or tokens
* Clearly state MVP limitations
* Clearly state that AI does not make final decisions
* Clearly state that Revit models are not automatically modified

---

## Why This PoC Matters

In BIM and construction AI projects, a common problem is that knowledge exists across many files and project outputs, but it is difficult to search, explain, and reuse.

This PoC demonstrates a small but important workflow:

```text
BIM data quality rules
+
Construction AI/DX use case mapping
+
RAG-style document design
+
Grounded retrieval
+
Referenced answer generation
+
pytest validation
```

This provides a foundation for future expansion into:

* Azure AI Search
* Vector search
* Embedding-based retrieval
* Azure OpenAI grounded answer generation
* Internal BIM knowledge assistant
* Construction AI proposal assistant
* BIM data quality explanation assistant
* AI readiness review assistant

---

## Future Improvements

Possible future improvements include:

* Add real embedding-based search
* Add Azure AI Search
* Add Azure OpenAI answer generation
* Add Streamlit UI
* Add source document viewer
* Add confidence score
* Add answer comparison
* Add feedback loop
* Add more BIM rule categories
* Add more construction AI use cases
* Add COBie / FM knowledge
* Add pyRevit metadata export knowledge
* Add BIM execution planning knowledge
* Add user-facing Japanese answer templates

---

## Current Status

Current MVP status:

```text
Step 1: Project folder created
Step 2: Design documents created
Step 3: Input samples created
Step 4: RAG-style document JSONL generated
Step 5: Simple keyword index generated
Step 6: Retrieval results generated
Step 7: Grounded sample answers generated
Step 8: Output review completed
Step 9: pytest validation completed
Step 10: README created
```

Current test result:

```text
90 passed
```

---

## Tech Stack

* Python
* CSV
* JSON / JSONL
* Markdown
* pytest

No external AI API is required for this MVP.

---

## License / Usage

This repository is a personal portfolio PoC for BIM / Construction AI learning and demonstration.

The sample data is created for demonstration purposes only.
It should not be treated as production data, legal advice, design advice, construction advice, or safety advice.
