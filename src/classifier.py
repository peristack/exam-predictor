import pandas as pd
import re

TEMAS = {
    'Constitución Española': [
        'constitución', 'constitucional', 'título', 'artículo', 'cortes generales',
        'senado', 'congreso', 'tribunal constitucional', 'defensor del pueblo',
        'derechos fundamentales', 'estatuto de autonomía', 'reforma constitucional'
        'administración pública', 'administración general', 'gobierno', 
        'presidente', 'moción de censura', 'estatuto', 'autonomía',
        'tribunal supremo', 'fiscal', 'ministerio'
    ],
    'Código Civil': [
        'código civil', 'nacionalidad', 'matrimonio', 'herencia',
        'propiedad', 'contrato', 'obligación', 'persona jurídica',
        'menor de edad', 'tutela', 'adopción'
    ],
    'Organización Policial': [
        'dirección general', 'unidad central', 'dao', 'dirección adjunta',
        'comisaría', 'brigada', 'jefatura', 'secretariado', 'fiscalía',
        'subdirección', 'área', 'dependencia'
    ],
    'Armamento y Física': [
        'armamento', 'arma', 'pistola', 'munición', 'satélite',
        'energía', 'unidad de energía', 'periodo orbital', 'velocidad',
        'física', 'óptica'
    ],
    'Economía y Finanzas': [
        'pasivo financiero', 'cuentas anuales', 'balance', 'activo',
        'financiero', 'presupuesto', 'deuda', 'contabilidad'
    ],
    'Código Penal': [
        'código penal', 'delito', 'pena', 'prisión', 'multa', 'homicidio',
        'robo', 'hurto', 'estafa', 'agresión', 'lesiones', 'asesinato',
        'tentativa', 'imprudencia', 'dolo', 'autor', 'cómplice'
    ],
    'Ley Orgánica FFCC': [
        'fuerzas y cuerpos', 'policía nacional', 'guardia civil',
        'ley orgánica 2/1986', 'seguridad ciudadana', 'funciones policiales',
        'misiones', 'cuerpos de seguridad'
    ],
    'Violencia de Género': [
        'violencia de género', 'víctima', 'maltrato', 'orden de protección',
        'viogen', 'violencia doméstica', 'mujer', 'feminicidio'
    ],
    'Extranjería': [
        'extranjero', 'extranjería', 'inmigración', 'residencia', 'visado',
        'expulsión', 'ciudadano comunitario', 'unión europea', 'asilo', 'refugiado'
    ],
    'Informática': [
        'informática', 'sistema operativo', 'windows', 'linux', 'internet',
        'red', 'protocolo', 'ip', 'navegador', 'virus', 'malware', 'cifrado',
        'base de datos', 'software', 'hardware', 'cpu', 'memoria'
        'open office', 'periférico', 'dispositivo', 'cableado', 'ataque informático',
        'usuario', 'diagrama'
    ],
    'Ciencias Sociales': [
        'sociología', 'globalización', 'inmigración', 'drogodependencia',
        'droga', 'estupefaciente', 'geografía', 'población', 'desarrollo sostenible',
        'medio ambiente', 'ética', 'valores'
    ],
    'Ortografía y Gramática': [
        'ortografía', 'gramática', 'frase', 'oración', 'verbo', 'sinónimo',
        'antónimo', 'acento', 'tilde', 'escribir', 'correctamente escrita'
    ],
    'Psicotécnicos': [
        'serie', 'secuencia', 'figura', 'patrón', 'siguiente término',
        'razonamiento', 'lógico', 'numérica'
    ],
    'Seguridad Privada': [
        'seguridad privada', 'vigilante', 'detective', 'empresa de seguridad'
    ],
    'Protección de Datos': [
        'protección de datos', 'rgpd', 'datos personales', 'lopd', 'agencia española'
    ],
    'Criminología y Sociología': [
    'criminología', 'teoría social', 'aprendizaje social', 'conducta',
    'delincuencia', 'factores', 'park', 'burgess', 'bandura', 'foro social',
    'globalización', 'integración', 'cultura', 'aculturation'
    ],
    'Europol e Internacional': [
    'europol', 'consejo de administración', 'convenio europeo', 'comité europeo',
    'tortura', 'convención', 'interpol', 'extradición', 'ley 23/2014'
    ],
    'Régimen de Personal': [
    'excedencia', 'junta de coordinación', 'real decreto 734', 'real decreto 726',
    'régimen de personal', 'habilitación profesional', 'instrucción operativa'
    ],
    'Criminalística y Topografía': [
    'topografía', 'planimetría', 'forense', 'instrumentos topográficos',
    'plano', 'criminalística', 'escena del crimen', 'vestigio', 'indicio'
    ],
    'Medio Ambiente': [
    'emas', 'gestión ambiental', 'desarrollo sostenible', 'brundtland',
    'objetivos de desarrollo', 'medio ambiente', 'ecología', 'reciclaje'
    ],
}

def classify_question(question_text):
    question_lower = question_text.lower()
    scores = {}
    
    for tema, keywords in TEMAS.items():
        score = sum(1 for kw in keywords if kw in question_lower)
        if score > 0:
            scores[tema] = score
    
    if scores:
        return max(scores, key=scores.get)
    return 'Sin clasificar'

def classify_all(csv_path):
    df = pd.read_csv(csv_path)
    df['tema'] = df['question'].apply(classify_question)
    
    output_path = csv_path.replace('questions.csv', 'questions_classified.csv')
    df.to_csv(output_path, index=False, encoding='utf-8')
    
    print("Distribución por temas:")
    print(df['tema'].value_counts().to_string())
    print(f"\nSin clasificar: {(df['tema'] == 'Sin clasificar').sum()} preguntas")
    
    return df

if __name__ == "__main__":
    df = classify_all('data/processed/questions.csv')