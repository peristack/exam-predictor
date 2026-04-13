import pdfplumber
import pandas as pd
import os
import re
def fix_encoding(text):
    replacements = {
        'B': 'ti',
        'Bempo': 'tiempo',
        'Bene': 'tiene',
        'ConsBtución': 'Constitución',
        'consBtución': 'constitución',
        'obje Bvos': 'objetivos',
        'objeBvos': 'objetivos',
        'OperaBva': 'Operativa',
        'operaBva': 'operativa',
        'habilitaBón': 'habilitación',
        'artículo': 'artículo',
        'armculo': 'artículo',
        'Berra': 'tierra',
    }
    for wrong, right in replacements.items():
        text = text.replace(wrong, right)
    return text

def extract_questions_from_pdf(pdf_path, year):
    questions = []
    
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
                full_text = fix_encoding(full_text)
    
    blocks = re.split(r'\n(?=\d+[\.\-]{1,2}\s)', full_text)
    
    for block in blocks:
        lines = block.strip().split('\n')
        if not lines:
            continue
            
        question_text = lines[0].strip()
        answers = []
        
        for line in lines[1:]:
            line = line.strip()
            if re.match(r'^[aAbBcC][).]', line):
                answers.append(line)
        
        if question_text and len(answers) >= 2:
            questions.append({
                'year': year,
                'question': question_text,
                'answers': ' | '.join(answers),
                'num_answers': len(answers),
                'source': os.path.basename(pdf_path)
            })
    
    return questions

def process_all_pdfs(raw_folder):
    all_questions = []
    
    for filename in os.listdir(raw_folder):
        if filename.endswith('.pdf'):
            year_match = re.search(r'20\d{2}', filename)
            year = int(year_match.group()) if year_match else 0
            
            pdf_path = os.path.join(raw_folder, filename)
            print(f"Procesando: {filename} (año: {year})")
            
            questions = extract_questions_from_pdf(pdf_path, year)
            all_questions.extend(questions)
            print(f"  → {len(questions)} preguntas extraídas")
    
    df = pd.DataFrame(all_questions)
    output_path = 'data/processed/questions.csv'
    df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"\nTotal: {len(all_questions)} preguntas guardadas en {output_path}")
    return df

if __name__ == "__main__":
    df = process_all_pdfs('data/raw')
    print(df.head())