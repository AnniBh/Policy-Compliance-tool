# Policy Compliance Analysis Tool for Educational Institutions (AI + RAG)

**Carleton University | Jan 2025 - Apr 2025**

An end-to-end AI-powered pipeline that ingests PDFs, retrieves the right sections via vector search, performs clause-level gap analysis with an LLM, and produces audit-friendly summaries with priorities for educational institutions.

## 🎯 **Project Overview**

This system provides comprehensive policy compliance analysis for educational institutions by leveraging advanced AI and Retrieval-Augmented Generation (RAG) techniques. It automates the complex process of comparing institutional policies against regulatory requirements and generates actionable compliance reports.

## ✨ **Key Features**

- **📄 PDF Document Processing**: Ingests policy and regulatory PDFs with PyPDF/pypdf
- **🔍 Intelligent Vector Search**: Retrieves relevant sections via advanced vector search
- **🤖 LLM-Powered Analysis**: Performs clause-level gap analysis using Llama 3.2
- **📊 Audit-Friendly Reports**: Produces structured summaries with priorities and citations
- **🔄 Dual Collection System**: Separate ChromaDB collections for Regulatory and Institutional texts
- **📝 OCR Fallback**: Tesseract integration for handling scanned PDFs
- **🏷️ Version Control**: Automatic re-embedding when documents change
- **👥 Human-in-the-Loop**: Checkpoints for high-priority findings validation

## 🏗️ **Architecture & Pipeline**

### **Document Ingestion & Processing**
1. **PDF Processing**: Uses PyPDF/pypdf to extract text from policy documents
2. **Text Cleaning**: Cleans and splits documents into overlapping chunks
3. **Embedding Generation**: Converts chunks into embeddings using Llama 3.2
4. **Metadata Storage**: Stores embeddings with document/page metadata in ChromaDB

### **Dual Collection System**
- **Regulatory Collection**: Stores regulatory requirements and standards
- **Institutional Collection**: Stores institutional policies and procedures

### **Query & Analysis Process**
1. **Dual Retrieval**: LangChain orchestrates retrieval from both collections
2. **Context Grounding**: Feeds relevant clauses into structured compliance prompts
3. **LLM Analysis**: Llama 3.2 performs clause-level compliance analysis
4. **Structured Output**: Generates findings with status, discrepancies, and recommendations

### **Report Generation**
- **Executive Summary**: Tailored for stakeholders using ChatGPT-4
- **Action Plan**: Prioritized recommendations with traceable citations
- **Audit Trail**: Complete documentation for compliance verification

## 🔧 **Technology Stack**

### **Core Technologies**
- **Python**: Primary programming language
- **PyPDF/pypdf**: PDF document processing
- **LangChain**: Orchestration and retrieval framework
- **ChromaDB**: Vector database for embeddings storage
- **Ollama**: Local LLM deployment (Llama 3.2)

### **AI & ML Components**
- **Llama 3.2**: Embeddings generation and LLM analysis
- **ChatGPT-4**: Report design and executive summary generation
- **Vector Search**: Semantic similarity and retrieval

### **Data Processing**
- **Pandas**: Data manipulation and analysis
- **OCR (Tesseract)**: Text extraction from scanned documents

## 📋 **Compliance Analysis Features**

### **Status Classification**
- **Fully Compliant**: Policy meets all regulatory requirements
- **Partially Compliant**: Policy partially meets requirements
- **Non-Compliant**: Policy does not meet requirements
- **Policy Gap**: Missing policy or procedure

### **Output Structure**
- **Status Assessment**: Compliance level for each clause
- **Discrepancy Text**: Specific areas of non-compliance
- **Actionable Recommendations**: Specific steps for improvement
- **Priority Levels**: Risk-based prioritization
- **Citations**: Traceable references to source documents

## �� **Getting Started**

### **Prerequisites**
- Python 3.8+
- Ollama with Llama 3.2 model
- ChromaDB
- Tesseract OCR

### **Installation**
```bash
# Clone the repository
git clone https://github.com/AnniBh/Policy-Compliance-tool.git
cd Policy-Compliance-tool

# Install dependencies
pip install -r requirements.txt

# Set up Ollama with Llama 3.2
ollama pull llama3.2
```

### **Usage**
```python
# Example usage
from policy_compliance_tool import PolicyComplianceAnalyzer

# Initialize the analyzer
analyzer = PolicyComplianceAnalyzer()

# Ingest documents
analyzer.ingest_regulatory_docs("path/to/regulatory/pdfs")
analyzer.ingest_institutional_docs("path/to/institutional/pdfs")

# Perform compliance analysis
results = analyzer.analyze_compliance("compare Article X with Policy Y")

# Generate report
report = analyzer.generate_report(results)
```

## 📊 **Sample Output**

### **Compliance Finding**
```
Status: Partially Compliant
Clause: Student Data Protection Policy Section 3.2
Discrepancy: Missing encryption requirements for data at rest
Recommendation: Implement AES-256 encryption for all stored student data
Priority: High
Citation: Regulatory Document A, Section 4.1
```

## 🔒 **Security & Privacy**

- **Local Processing**: All analysis performed locally using Ollama
- **Data Privacy**: No sensitive policy data transmitted to external services
- **Audit Trail**: Complete logging of all analysis activities
- **Access Control**: Role-based access to compliance reports

## 🤝 **Contributing**

This project was developed as part of a 3rd Term project at Carleton University. For academic collaboration or research purposes, please contact the project team.

## 📄 **License**

This project is developed for educational and research purposes at Carleton University.

## 🏛️ **Institution**

**Carleton University**  
*Policy Compliance Analysis Tool for Educational Institutions*  
*Jan 2025 - Apr 2025*

---

**Keywords**: Compliance automation • RAG • Vector search • Prompt engineering • Document AI • Policy benchmarking • AI governance
