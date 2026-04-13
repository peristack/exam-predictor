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
        'poderes públicos', 'carta magna', 'estado social', 'estado democrático',
        'estado de derecho', 'promoverán las condiciones'
    ],
    'Código Civil': [
        'código civil', 'nacionalidad', 'matrimonio', 'herencia',
        'propiedad', 'contrato', 'obligación', 'persona jurídica',
        'menor de edad', 'tutela', 'adopción'
        'vecindad civil', 'afirmación correcta', 'aseveraciones'
    ],
    'Organización Policial': [
        'dirección general', 'unidad central', 'dao', 'dirección adjunta',
        'comisaría', 'brigada', 'jefatura', 'secretariado', 'fiscalía',
        'subdirección', 'área', 'dependencia'
        'inspección de personal', 'planificación estratégica', 'secretaría de estado',
        'comité de expertos', 'unidades adscritas', 'comunidades autónomas',
    'consejo de política de seguridad', 'dirección adjunta operativa'
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
        'lesión', 'primera asistencia', 'facultativa', 'bomba', 'amenaza',
        'denuncia', 'modalidad delictiva'
        'anciano', 'puerta abierta', 'individuos observan', 'robo con fuerza',
        'potestad sancionadora', 'infracciones administrativas'
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
        'phishing', 'spear phishing', 'ingeniería social', 'whaling',
        'ciberataque', 'ataque informático'
        'servidor', 'denegación de servicio', 'ddos', 'huella digital',
        'encaminamiento', 'enrutamiento', 'capa', 'dns', 'domain name system',
        'dominios', 'red informática'
        'adas', 'sistemas avanzados', 'osint', 'inteligencia de fuentes abiertas',
        'herramientas', 'implementar un sistema'
    ],
    'Ciencias Sociales': [
        'sociología', 'globalización', 'inmigración', 'drogodependencia',
        'droga', 'estupefaciente', 'geografía', 'población', 'desarrollo sostenible',
        'medio ambiente', 'ética', 'valores'
    ],
    'Ortografía y Gramática': [
        'ortografía', 'gramática', 'frase', 'oración', 'verbo', 'sinónimo',
        'antónimo', 'acento', 'tilde', 'escribir', 'correctamente escrita'
        'mayúsculas', 'sobrenombres', 'apodos', 'seudónimos', 'escriben',
        'primera letra', 'minúsculas'
    ],
    'Psicotécnicos': [
        'serie', 'secuencia', 'figura', 'patrón', 'siguiente término',
        'razonamiento', 'lógico', 'numérica'
    ],
    'Seguridad Privada': [
        'seguridad privada', 'vigilante', 'detective', 'empresa de seguridad'
        'vigilancia', 'protección de bienes', 'establecimientos', 'eventos',
        'habilitación profesional', 'empresa de seguridad'
        'detective privado', 'informes de investigación', 'conservarse',
        'detective', 'investigación privada'
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
    'daños no personales', 'trayecto', 'domicilio', 'lugar de trabajo',
    'accidente laboral', 'funcionario', 'real decreto 2/2006'
    'retribuciones', 'área de retribuciones', 'gestionar', 'salario',
    'complemento', 'nómina'
    ],
    'Criminalística y Topografía': [
    'topografía', 'planimetría', 'forense', 'instrumentos topográficos',
    'plano', 'criminalística', 'escena del crimen', 'vestigio', 'indicio'
    ],
    'Medio Ambiente': [
    'emas', 'gestión ambiental', 'desarrollo sostenible', 'brundtland',
    'objetivos de desarrollo', 'medio ambiente', 'ecología', 'reciclaje'
    ],
    'Instituciones Europeas': [
    'banco central europeo', 'sede', 'directiva comunitaria', 'igualdad',
    'transposición', 'parlamento europeo', 'comisión europea', 'tribunal de justicia'
    ],
    'DNI y Documentación': [
        'documento nacional de identidad', 'dni', 'permiso de conducir',
        'licencia', 'pasaporte', 'nacimiento', 'registro civil'
    ],
    'Tribunal del Jurado': [
        'tribunal del jurado', 'jurado', 'culpabilidad', 'acusado',
        'veredicto', 'competencia', 'fallo'
    ],
    'Psicología Social': [
        'maslow', 'pirámide', 'necesidades', 'motivación', 'conducta social',
        'psicología', 'personalidad', 'comportamiento'
        'escala f', 'estudios de escala', 'adorno', 'autoritarismo',
        'personalidad autoritaria'
    ],
    'Funcionarios Públicos': [
        'funcionario de carrera', 'situación administrativa', 'excedencia',
        'efectos económicos', 'personal no permanente', 'confianza',
        'asesoramiento', 'ley orgánica 9/2015', 'régimen disciplinario'
    ],
    'Geografía y Demografía': [
        'crecimiento vegetativo', 'tasa', 'núcleos urbanos', 'población',
        'demografía', 'geografía humana', 'municipio', 'área metropolitana'
    ],
    'Derecho Procesal': [
        'intimidad', 'interceptación', 'escucha', 'prueba', 'juicio oral',
        'instrucción', 'fiscal', 'juez', 'sentencia', 'recurso', 'apelación'
    ],
    'Tráfico y Vehículos': [
        'conducir', 'vehículo', 'tráfico', 'luces', 'señales acústicas',
        'permiso de conducir', 'accidente', 'infracción de tráfico'
    ],
    'Inmigración Internacional': [
        'organización internacional para las migraciones', 'oim',
        'migraciones', 'creada en', 'organismo internacional'
        'ruta migratoria', 'cuerno de áfrica', 'iniciativa', 'flujos migratorios'
    ],
    'Drogas y Drogodependencias': [
    'heroína', 'cocaína', 'droga', 'consumo combinado', 'estupefaciente',
    'speedball', 'cannabis', 'sustancia', 'drogodependencia', 'narcótico'
    ],
    'Organización Policial': [
        'unidades básicas', 'grandes urbes', 'comisaría', 'inspección de personal',
        'unidad de prevención de riesgos', 'orden int', 'estructura orgánica',
        'funciones de los', 'jefes de seguridad'
        'jefatura de unidades', 'intervención policial', 'guardapesca',
        'hospedaje', 'partes de entrada', 'consejo de política de seguridad',
        'comité de expertos', 'área de innovación formativa', 'centros de cooperación',
        'cooperación policial y aduanera', 'dirección general de la policía',
        'quejas y sugerencias', 'real decreto 2/2006'
    ],
    'Tribunal Constitucional': [
        'ley orgánica 2/1979', 'tribunal constitucional', 'recurso de amparo',
        'jueces del tribunal', 'magistrado', 'inconstitucionalidad'
    ],
    'Consejo Europeo': [
        'consejo europeo', 'consejo de la unión', 'cumbres europeas',
        'jefe de estado', 'jefe de gobierno', 'presidencia'
    ],
    'Delitos Concretos': [
        'registro domiciliario', 'mandamiento de entrada', 'detenido',
        'detención', 'ingreso', 'estafa', 'apropiación indebida',
        'consentimiento', 'venganza', 'privadas de libertad'
    ],
    'Seguridad Vial': [
        'seguridad vial', 'estrategia de seguridad vial', 'factor esencial',
        'accidente de tráfico', 'velocidad', 'alcohol', 'drogas al volante'
    ],
    'Sociología': [
        'fukuyama', 'wilson', 'sectas', 'sociólogo', 'crecimiento',
        'condiciones previas', 'capital social', 'teoría'
    ],
    'Derechos del Detenido': [
        'abogado', 'detenido', 'detención', 'habeas corpus', 'horas',
        'asistencia letrada', 'comunicación', 'miranda', 'derechos'
    ],
    'Infraestructuras Críticas': [
        'infraestructuras críticas', 'medidas de vigilancia', 'prevención',
        'protección', 'reacción', 'plan de seguridad', 'operador crítico'
    ],
    'Ley Orgánica de Protección de Datos': [
        'ley orgánica 7/2021', 'plazo máximo', 'datos policiales',
        'fichero', 'tratamiento de datos', 'conservación'
    ],
    'Organización Judicial': [
    'tribunal superior de justicia', 'organización judicial', 'culmina',
    'ámbito', 'jurisdicción', 'sala', 'audiencia provincial',
    'tribunal supremo', 'juzgado'
    ],
    'Derecho Internacional': [
    'caas', 'convenio de aplicación', 'schengen', 'entró en vigor',
    'acuerdo internacional', 'tratado', 'convenio'
    ],
    'Defensor del Pueblo': [
    'visitar los lugares', 'personas privadas de su libertad',
    'defensor del pueblo', 'mecanismo nacional', 'prevención de la tortura'
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