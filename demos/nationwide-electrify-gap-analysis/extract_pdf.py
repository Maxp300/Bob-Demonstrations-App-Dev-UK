#!/usr/bin/env python3
"""
PDF Text Extraction Script
Extracts text content from PDF files for analysis
"""

import PyPDF2
import sys
import json

def extract_pdf_text(pdf_path):
    """Extract text from PDF file"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Get metadata
            metadata = {
                'num_pages': len(pdf_reader.pages),
                'title': pdf_reader.metadata.title if pdf_reader.metadata else None,
                'author': pdf_reader.metadata.author if pdf_reader.metadata else None,
            }
            
            # Extract text from all pages
            full_text = []
            for page_num, page in enumerate(pdf_reader.pages, 1):
                text = page.extract_text()
                if text.strip():
                    full_text.append({
                        'page': page_num,
                        'text': text
                    })
            
            return {
                'metadata': metadata,
                'content': full_text,
                'success': True
            }
    
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python extract_pdf.py <pdf_file>")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    result = extract_pdf_text(pdf_path)
    
    if result['success']:
        print(f"Successfully extracted text from {result['metadata']['num_pages']} pages")
        print(f"Title: {result['metadata']['title']}")
        print("\n" + "="*80 + "\n")
        
        # Print first 2000 characters of content
        for page_data in result['content'][:3]:  # First 3 pages
            print(f"--- Page {page_data['page']} ---")
            print(page_data['text'][:1000])
            print("\n")
        
        # Save full content to file
        output_file = pdf_path.replace('.pdf', '_extracted.txt')
        with open(output_file, 'w', encoding='utf-8') as f:
            for page_data in result['content']:
                f.write(f"\n{'='*80}\n")
                f.write(f"PAGE {page_data['page']}\n")
                f.write(f"{'='*80}\n\n")
                f.write(page_data['text'])
                f.write("\n\n")
        
        print(f"\nFull content saved to: {output_file}")
    else:
        print(f"Error: {result['error']}")
        sys.exit(1)

# Made with Bob
