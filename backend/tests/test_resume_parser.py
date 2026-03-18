"""
Test script for resume text extraction module.

This script demonstrates how to use the extract_resume_text function
to extract text from PDF and DOCX resume files.
"""

from ai.resume_parser import extract_resume_text, get_file_info

def test_resume_extraction():
    """Test resume text extraction with sample files."""
    
    # Example usage for PDF file
    print("=" * 50)
    print("Testing PDF Resume Extraction")
    print("=" * 50)
    
    try:
        pdf_path = "uploads/sample_resume.pdf"
        text = extract_resume_text(pdf_path)
        print(f"Extracted {len(text)} characters from PDF")
        print(f"Preview: {text[:200]}...")
        
        file_info = get_file_info(pdf_path)
        print(f"File Info: {file_info}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n")
    
    # Example usage for DOCX file
    print("=" * 50)
    print("Testing DOCX Resume Extraction")
    print("=" * 50)
    
    try:
        docx_path = "uploads/sample_resume.docx"
        text = extract_resume_text(docx_path)
        print(f"Extracted {len(text)} characters from DOCX")
        print(f"Preview: {text[:200]}...")
        
        file_info = get_file_info(docx_path)
        print(f"File Info: {file_info}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_resume_extraction()
