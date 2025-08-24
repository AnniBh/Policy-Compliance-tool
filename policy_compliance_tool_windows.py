import os
import pandas as pd
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
from typing import List, Dict

class PolicyComplianceAnalysisTool:
    def __init__(self, policy_documents_folder: str, regulatory_documents_folder: str):
        """
        Initialize the Policy Compliance Analysis Tool with separate folders for policy and regulatory documents
        
        :param policy_documents_folder: Path to the folder containing institutional policy documents
        :param regulatory_documents_folder: Path to the folder containing regulatory documents
        """
        self.policy_documents_folder = policy_documents_folder
        self.regulatory_documents_folder = regulatory_documents_folder
        
        # Separate document collections
        self.policy_documents = []
        self.regulatory_documents = []
        
        # Vector stores for different document types
        self.policy_vector_store = None
        self.regulatory_vector_store = None
        
        # Use Ollama embeddings with Llama 3.2
        try:
            self.embeddings = OllamaEmbeddings(model='llama3.2')
            print("✓ Ollama embeddings initialized successfully")
        except Exception as e:
            print(f"⚠ Warning: Could not initialize Ollama embeddings: {e}")
            print("Please install Ollama from https://ollama.ai and run: ollama pull llama3.2")
            self.embeddings = None
    
    def load_documents(self, document_type: str) -> int:
        """
        Load PDF documents from specified folder
        
        :param document_type: 'policy' or 'regulatory'
        :return: Number of documents loaded
        """
        # Select the appropriate folder and document list based on type
        if document_type == 'policy':
            documents_folder = self.policy_documents_folder
            document_list = self.policy_documents
        elif document_type == 'regulatory':
            documents_folder = self.regulatory_documents_folder
            document_list = self.regulatory_documents
        else:
            raise ValueError("Document type must be 'policy' or 'regulatory'")
        
        # Reset the document list
        document_list.clear()
        
        # Check if folder exists
        if not os.path.exists(documents_folder):
            print(f"⚠ Warning: Folder {documents_folder} does not exist. Creating it...")
            os.makedirs(documents_folder, exist_ok=True)
            print(f"✓ Created folder: {documents_folder}")
            print(f"Please add your {document_type} PDF documents to this folder.")
            return 0
        
        # Load PDF documents
        pdf_count = 0
        for filename in os.listdir(documents_folder):
            file_path = os.path.join(documents_folder, filename)
            
            # Process only PDF files
            if os.path.isfile(file_path) and filename.lower().endswith('.pdf'):
                try:
                    print(f"Loading {filename}...")
                    loader = PyPDFLoader(file_path)
                    docs = loader.load()
                    document_list.extend(docs)
                    pdf_count += 1
                    print(f"✓ Successfully loaded {filename}")
                except Exception as e:
                    print(f"✗ Error processing {filename}: {e}")
        
        return pdf_count
    
    def split_documents(self, document_type: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List:
        """
        Split documents into manageable chunks
        
        :param document_type: 'policy' or 'regulatory'
        :param chunk_size: Size of text chunks
        :param chunk_overlap: Overlap between chunks
        :return: List of document chunks
        """
        # Select the appropriate document list based on type
        if document_type == 'policy':
            documents = self.policy_documents
        elif document_type == 'regulatory':
            documents = self.regulatory_documents
        else:
            raise ValueError("Document type must be 'policy' or 'regulatory'")
        
        if not documents:
            print(f"⚠ No {document_type} documents loaded. Please add PDF files to the {document_type} folder.")
            return []
        
        # Split documents
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, 
            chunk_overlap=chunk_overlap
        )
        chunks = text_splitter.split_documents(documents)
        print(f"✓ Split {len(documents)} {document_type} documents into {len(chunks)} chunks")
        return chunks
    
    def create_vector_store(self, document_type: str, chunks: List = None):
        """
        Create vector embeddings and store in Chroma
        
        :param document_type: 'policy' or 'regulatory'
        :param chunks: Optional pre-split document chunks
        :return: Chroma vector store
        """
        if self.embeddings is None:
            print("✗ Cannot create vector store: Ollama embeddings not available")
            return None
        
        # Select the appropriate vector store based on type
        if document_type == 'policy':
            vector_store_attr = 'policy_vector_store'
        elif document_type == 'regulatory':
            vector_store_attr = 'regulatory_vector_store'
        else:
            raise ValueError("Document type must be 'policy' or 'regulatory'")
        
        # Use chunks or split documents
        if chunks is None:
            chunks = self.split_documents(document_type)
        
        if not chunks:
            print(f"⚠ No chunks available for {document_type} documents")
            return None
        
        try:
            # Create Chroma vector store with Llama 3.2 embeddings
            vector_store = Chroma.from_documents(
                documents=chunks, 
                embedding=self.embeddings
            )
            
            # Set the appropriate vector store attribute
            setattr(self, vector_store_attr, vector_store)
            print(f"✓ Created vector store for {document_type} documents")
            
            return vector_store
        except Exception as e:
            print(f"✗ Error creating vector store for {document_type} documents: {e}")
            return None
    
    def setup_compliance_analysis_chain(self):
        """
        Set up the retrieval QA chain for compliance analysis
        
        :return: Retrieval QA Chain
        """
        try:
            # Use Ollama with Llama 3.2
            llm = Ollama(model='llama3.2', temperature=0.3)
            print("✓ Ollama LLM initialized successfully")
        except Exception as e:
            print(f"✗ Error initializing Ollama LLM: {e}")
            print("Please ensure Ollama is running and llama3.2 model is available")
            return None, None
        
        # Exact Prompt for Compliance Analysis
        compliance_template = """
You are an expert Compliance Analyst with extensive experience in regulatory compliance and policy alignment. Your role is to meticulously analyze and compare the institution's internal policies against government-issued regulatory documents. These documents may include formal regulations, guidelines, or informal releases such as press statements. You are methodical, detail-oriented, and focused on providing actionable recommendations to enhance compliance.

Instructions for Analysis:

1. Benchmarking Document
- Treat all government regulatory documents (e.g., regulations, press releases, guidelines) as potential benchmarks.
- When analyzing press releases or informal documents, focus on identifying implied or explicitly stated expectations relevant to institutional policies.

Regulatory Context: {regulatory_context}
Institutional Policy Context: {policy_context}

Analysis Requirements:
a) Benchmark each government regulatory document section against institutional policies
b) Identify compliance status:
   - Fully Compliant
   - Partially Compliant
   - Non-Compliant
   - Policy Gap

c) For press releases, focus on key statements implying compliance requirements

Handling Ambiguity:
- Clearly note the source of benchmarks
- Flag ambiguous or non-standardized requirements
- Provide interpretation context

Output Structure:
I. Document Type (Regulation/Guideline/Press Release)
II.Reference: Include the title, section, or specific statement from the government document.
III.Reference: Include the title, section, or specific statement from the Policy Sectiondocument
IV. Detailed Discrepancy Analysis
V. Actionable Recommendations
VI. Priority Level (High/Medium/Low)

Prioritization Criteria:
- Relevance of policy document
- Severity of non-compliance implications
- Ease of remediation

Ethical Considerations:
- Maintain confidentiality of institutional data
- Ethically handle less formal policy benchmarks
- Treat press release expectations as advisory unless explicitly mandated

Reporting Guidelines:
1. Executive Summary
   - Highlight critical compliance gaps
   - Emphasize potential operational impact
   - Focus on high-priority issues

2. Key Findings
   - Summarize discrepancies
   - Include compliance area 
   - Note priority level with 
   - Provide brief recommendations

3. Conclusion and Recommendations
   - Summarize actionable next steps
   - Emphasize urgency and feasibility
   - Limit report to 500 words

Key Objective: Provide precise and actionable insights to align institutional policies with diverse government-issued regulatory benchmarks, enhancing compliance, adaptability, and operational efficiency.
"""
        
        # Create prompt template
        prompt = PromptTemplate(
            template=compliance_template,
            input_variables=['regulatory_context', 'policy_context']
        )
        
        return prompt, llm
    
    def generate_compliance_report(self):
        """
        Generate a compliance analysis report
        
        :return: Detailed compliance report
        """
        # Check if vector stores are available
        if not self.policy_vector_store:
            print("⚠ Policy vector store not available. Creating it...")
            self.load_documents('policy')
            self.create_vector_store('policy')
        
        if not self.regulatory_vector_store:
            print("⚠ Regulatory vector store not available. Creating it...")
            self.load_documents('regulatory')
            self.create_vector_store('regulatory')
        
        if not self.policy_vector_store or not self.regulatory_vector_store:
            print("✗ Cannot generate report: Vector stores not available")
            return "Error: Cannot generate compliance report. Please ensure both policy and regulatory documents are loaded and vector stores are created."
        
        # Retrieve context from vector stores
        policy_retriever = self.policy_vector_store.as_retriever()
        regulatory_retriever = self.regulatory_vector_store.as_retriever()
        
        # Retrieve all documents (for comprehensive analysis)
        policy_docs = policy_retriever.get_relevant_documents("All policy documents")
        regulatory_docs = regulatory_retriever.get_relevant_documents("All regulatory documents")
        
        # Prepare context for analysis
        policy_context = ' '.join([doc.page_content for doc in policy_docs])
        regulatory_context = ' '.join([doc.page_content for doc in regulatory_docs])
        
        # Setup analysis chain
        prompt, llm = self.setup_compliance_analysis_chain()
        
        if prompt is None or llm is None:
            return "Error: Could not initialize analysis chain. Please ensure Ollama is running."
        
        # Generate compliance report
        try:
            analysis_chain = prompt | llm
            compliance_report = analysis_chain.invoke({
                'policy_context': policy_context,
                'regulatory_context': regulatory_context
            })
            return compliance_report
        except Exception as e:
            return f"Error generating compliance report: {e}"

def setup_document_folders():
    """Create the necessary document folders"""
    # Get current directory
    current_dir = os.getcwd()
    
    # Create folders in the current directory
    policy_folder = os.path.join(current_dir, "policy_documents")
    regulatory_folder = os.path.join(current_dir, "regulatory_documents")
    
    # Create folders if they don't exist
    os.makedirs(policy_folder, exist_ok=True)
    os.makedirs(regulatory_folder, exist_ok=True)
    
    print(f"✓ Created policy documents folder: {policy_folder}")
    print(f"✓ Created regulatory documents folder: {regulatory_folder}")
    
    return policy_folder, regulatory_folder

def main():
    print("=== Policy Compliance Analysis Tool ===")
    print("Setting up document folders...")
    
    # Setup document folders
    policy_folder, regulatory_folder = setup_document_folders()
    
    print("\n📁 Document Folders Created:")
    print(f"   Policy Documents: {policy_folder}")
    print(f"   Regulatory Documents: {regulatory_folder}")
    print("\n📋 Next Steps:")
    print("   1. Add your policy PDF documents to the 'policy_documents' folder")
    print("   2. Add your regulatory PDF documents to the 'regulatory_documents' folder")
    print("   3. Install Ollama from https://ollama.ai")
    print("   4. Run: ollama pull llama3.2")
    print("   5. Run this script again to generate the compliance report")
    
    # Check if folders have documents
    policy_files = [f for f in os.listdir(policy_folder) if f.lower().endswith('.pdf')]
    regulatory_files = [f for f in os.listdir(regulatory_folder) if f.lower().endswith('.pdf')]
    
    if not policy_files and not regulatory_files:
        print("\n⚠ No PDF documents found in the folders.")
        print("Please add your documents and run the script again.")
        return
    
    # Initialize and run compliance analysis tool
    try:
        print(f"\n📊 Found {len(policy_files)} policy documents and {len(regulatory_files)} regulatory documents")
        
        # Create compliance analysis tool with separate document folders
        compliance_tool = PolicyComplianceAnalysisTool(policy_folder, regulatory_folder)
        
        # Load and process documents
        policy_doc_count = compliance_tool.load_documents('policy')
        regulatory_doc_count = compliance_tool.load_documents('regulatory')
        
        if policy_doc_count == 0 and regulatory_doc_count == 0:
            print("⚠ No documents were loaded. Please check that your PDF files are valid.")
            return
        
        print(f"✓ Processed {policy_doc_count} policy documents")
        print(f"✓ Processed {regulatory_doc_count} regulatory documents")
        
        # Create vector stores
        if policy_doc_count > 0:
            compliance_tool.create_vector_store('policy')
        if regulatory_doc_count > 0:
            compliance_tool.create_vector_store('regulatory')
        
        # Generate compliance report
        print("\n🔍 Generating Compliance Analysis Report...")
        compliance_report = compliance_tool.generate_compliance_report()
        
        print("\n" + "="*50)
        print("COMPLIANCE ANALYSIS REPORT")
        print("="*50)
        print(compliance_report)
        
        # Save report to file
        report_file = "compliance_report.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(compliance_report)
        print(f"\n✓ Report saved to: {report_file}")
    
    except Exception as e:
        print(f"✗ An error occurred during compliance analysis: {e}")

if __name__ == "__main__":
    main()
