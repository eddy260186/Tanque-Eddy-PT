# ==========================================
# 2.5 BASE DE DATOS DE EJERCICIOS
# ==========================================
ejercicios_db = {
    "Pecho": ["Press de Banca Plano", "Press Inclinado con Mancuernas", "Aperturas o Peck Deck", "Cruces en Polea", "Fondos en Paralelas (Dips)"],
    "Espalda": ["Dominadas o Jalón al Pecho", "Remo con Barra o Mancuerna", "Remo en Polea Baja", "Pull-over con Cuerda", "Remo en Punta (Barra T)"],
    "Cuádriceps": ["Sentadilla Libre o Multipower", "Prensa Inclinada", "Extensiones de Cuádriceps", "Sentadilla Búlgara", "Zancadas (Lunges)"],
    "Femorales": ["Peso Muerto Rumano (RDL)", "Curl de Isquiotibiales Sentado", "Curl de Isquiotibiales Tumbado", "Peso Muerto Piernas Rígidas", "Buenos Días"],
    "Glúteos": ["Hip Thrust (Empuje de Cadera)", "Puente de Glúteo", "Patada de Glúteo en Polea", "Abducciones en Máquina", "Sentadilla Sumo"],
    "Pantorrillas": ["Elevación de Talones de pie", "Elevación de Talones sentado en máquina"],
    "Hombros": ["Press Militar", "Vuelos Laterales con Mancuerna", "Vuelos Posteriores (Pájaros)", "Face Pull", "Elevaciones Frontales con Polea"],
    "Brazos": ["Curl con Barra (Bíceps)", "Curl Martillo Alternado", "Extensión en Polea (Tríceps)", "Press Francés o Copa", "Curl Predicador en Banco Scott"],
    "Core": ["Plancha Abdominal Isométrica", "Crunch en Polea Alta", "Elevación de Piernas Colgado", "Rueda Abdominal (Ab Wheel)", "Giros Rusos con Peso"]
}

# ==========================================
# BASE DE DATOS ELITE - RUTINAS DE ENTRENAMIENTO V60.7
# ==========================================

rutinas_elite = {
    "Fuerza / Hipertrofia (Gimnasio)": {
        "Principiante": [
            ["Día 1: Full Body A", "Prensa de Piernas 3x15", "Press de Pecho en Máquina 3x12", "Jalón al Pecho 3x12", "Plancha Abdominal 3x30s"],
            ["Día 2: Full Body B", "Sentadilla con Mancuerna (Copa) 3x12", "Press Militar con Mancuernas 3x12", "Remo en Polea Baja 3x12", "Curl de Bíceps 3x15"],
            ["Día 3: Descanso Activo", "Caminata moderada 30-40 min", "Movilidad articular general"],
            ["Día 4: Full Body A", "Prensa de Piernas 3x15", "Press de Pecho en Máquina 3x12", "Jalón al Pecho 3x12", "Plancha Abdominal 3x30s"],
            ["Día 5: Circuito Metabólico", "Kettlebell Swings 3x15", "Flexiones apoyando rodillas 3x10", "Remo TRX 3x12", "Crunches 3x20"]
        ],
        "Intermedio": [
            ["Día 1: Empuje (Push)", "Press de Banca Plano 4x8-10", "Press Inclinado con Mancuernas 3x10", "Vuelos Laterales 4x12", "Extensión de Tríceps en Polea 4x12"],
            ["Día 2: Tracción (Pull)", "Dominadas Asistidas o Jalón 4x8-10", "Remo con Barra 4x10", "Face Pull 3x15", "Curl de Bíceps con Barra Z 4x10"],
            ["Día 3: Piernas (Legs)", "Sentadilla Libre 4x8-10", "Peso Muerto Rumano 4x10", "Prensa 45° 3x12", "Elevación de Talones 4x15"],
            ["Día 4: Torso", "Press Militar con Barra 4x8", "Remo con Mancuerna a una mano 4x10", "Cruces en Polea 3x12", "Elevaciones Frontales 3x15"],
            ["Día 5: Piernas y Core", "Hip Thrust 4x10", "Estocadas Búlgaras 3x10/pierna", "Curl de Isquios en Máquina 3x15", "Rueda Abdominal (Ab Wheel) 4x10"]
        ],
        "Avanzado": [
            ["Día 1: Pecho y Bíceps (Fuerza/Hipertrofia)", "Press de Banca Plano 5x5 (RIR 1-2)", "Press Inclinado 4x8", "Aperturas con Mancuernas 3x12", "Curl Predicador 4x8-10"],
            ["Día 2: Piernas (Enfoque Cuádriceps)", "Sentadilla Tras Nuca 5x5 (RIR 1-2)", "Sentadilla Hack 4x10", "Extensiones de Cuádriceps 4x15 (Drop set final)", "Gemelos Parado 5x12"],
            ["Día 3: Espalda y Tríceps", "Dominadas con Lastre 4x6-8", "Remo Pendlay 4x8", "Pull-over en Polea 3x12", "Press Francés 4x10"],
            ["Día 4: Hombros y Core", "Press Militar de Pie 4x6", "Remo al Mentón 4x10", "Vuelos Laterales en Polea 4x15", "Dragon Flags 4xFallo"],
            ["Día 5: Piernas (Enfoque Cadena Posterior)", "Peso Muerto Convencional 4x5", "Hip Thrust Pesado 4x8", "Curl Femoral Tumbado 4x12", "Gemelos Sentado 4x15"]
        ]
    },
    
    "CrossFit / Funcional": {
        "Principiante": [
            ["Día 1: Técnica y EMOM", "Skill: Técnica de Air Squat y Push-up", "EMOM 10 min: Min 1: 10 Air Squats | Min 2: 5-8 Push-ups"],
            ["Día 2: AMRAP Adaptación", "Skill: Kettlebell Swing Ruso", "AMRAP 12 min: 10 KB Swings, 10 Sit-ups, 30 Single Unders"],
            ["Día 3: Descanso o Movilidad", "Yoga básico", "Estiramientos estáticos (20 min)"],
            ["Día 4: For Time (Por Tiempo)", "Skill: Remo en anillas", "4 Rondas: 200m Run, 10 Remo Anillas, 10 Box Step-ups"],
            ["Día 5: Circuito Core", "Tabata 8 min: Plancha frontal y V-ups", "Práctica de Wall Balls con balón ligero (3 series x 10)"]
        ],
        "Intermedio": [
            ["Día 1: Fuerza y WOD", "Fuerza: Back Squat 4x5", "WOD: 'Helen' - 3 Rondas: 400m Run, 21 KB Swings, 12 Pull-ups"],
            ["Día 2: Gimnásticos y WOD", "Skill: Toes to Bar (T2B)", "AMRAP 15 min: 10 T2B, 15 Wall Balls, 20 Double Unders"],
            ["Día 3: Halterofilia Ligera", "Skill: Clean & Jerk (Técnica)", "EMOM 12 min: 2 Clean & Jerk (70% 1RM)"],
            ["Día 4: Intervalos de Alta Intensidad", "5 Rondas: 500m Row, 2 min descanso", "Core: 50 GHD Sit-ups acumulados"],
            ["Día 5: WOD Chipper", "Por tiempo: 50 Box Jumps, 40 Kettlebell Swings, 30 Push-ups, 20 Pull-ups, 10 Burpees"]
        ],
        "Avanzado": [
            ["Día 1: Levantamiento Pesado y Hero WOD", "Fuerza: Snatch 1RM del día", "WOD 'Fran': 21-15-9 Thrusters (43kg/30kg) y Pull-ups"],
            ["Día 2: Capacidad Aeróbica y Gimnásticos", "Skill: Muscle-ups", "WOD: 5 Rondas: 400m Run, 5 Bar Muscle-ups, 10 Handstand Push-ups"],
            ["Día 3: Fuerza Pura", "Deadlift 5-3-1-1-1", "Accesorio: 4x10 Bulgarian Split Squats pesadas"],
            ["Día 4: WOD Largo (Endurance)", "WOD 'Murph': 1 milla Run, 100 Pull-ups, 200 Push-ups, 300 Squats, 1 milla Run (con Chaleco 10kg)"],
            ["Día 5: Halterofilia bajo fatiga", "EMOM 20 min: Min 1: 15 Cal Bike | Min 2: 3 Power Cleans (80% 1RM)"]
        ]
    },

    "Powerlifting / Levantamiento Olímpico": {
        "Principiante": [
            ["Día 1: Técnica de Sentadilla", "Sentadilla Goblet 4x10", "Prensa de Piernas 3x12", "Plancha 3x45s"],
            ["Día 2: Técnica de Empuje", "Press de Banca con barra sola 4x10", "Press con mancuernas 3x10", "Remo invertido 3x10"],
            ["Día 3: Movilidad", "Liberación miofascial y estiramientos", "Rotaciones de cadera y hombros"],
            ["Día 4: Técnica de Bisagra", "Peso Muerto Rumano ligero 4x8", "Curl Femoral 3x12", "Crunches 3x15"],
            ["Día 5: Accesorios Generales", "Press Militar sentado 3x10", "Jalón al pecho 3x12", "Extensiones de espalda 3x15"]
        ],
        "Intermedio": [
            ["Día 1: Sentadilla Pesada", "Back Squat 5x5 (RPE 7-8)", "Prensa 45° 3x10", "Ab Wheel 3x10"],
            ["Día 2: Press de Banca", "Bench Press 5x5 (RPE 7-8)", "Press Cerrado 3x8", "Remo con barra 4x8"],
            ["Día 3: Peso Muerto (Deadlift)", "Peso Muerto Convencional/Sumo 1x5, 2x5 (Back-off)", "Dominadas 3x8", "Hip Thrust 3x10"],
            ["Día 4: Variación de Sentadilla/Press", "Sentadilla Pausada 3x5", "Press Militar 4x6", "Face Pull 3x15"],
            ["Día 5: Accesorios y Puntos Débiles", "Fondos en paralelas con lastre 3x8", "Remo con mancuerna 3x10", "Elevaciones laterales 3x12"]
        ],
        "Avanzado": [
            ["Día 1: Fuerza Máxima - Sentadilla", "Sentadilla de Competición 1x3 (RPE 9), 4x3 (RPE 8)", "Sentadilla Búlgara pesada 3x8/pierna", "Core Anti-rotación 3x12"],
            ["Día 2: Fuerza Máxima - Press de Banca", "Press de Banca (con pausa de competición) 1x3 (RPE 9), 4x3 (RPE 8)", "Spoto Press 3x5", "Remo Pendlay 4x6"],
            ["Día 3: Fuerza Máxima - Peso Muerto", "Peso Muerto de Competición 1x2 (RPE 9), 3x3 (RPE 8)", "Deficit Deadlift 3x5", "Dominadas lastradas 3x6"],
            ["Día 4: GPP e Hipertrofia", "Press Inclinado con mancuernas 4x8", "Remo en polea 4x10", "Curl de Bíceps y Tríceps en polea (Superserie) 4x12"],
            ["Día 5: Variantes Secundarias", "Pin Squat 3x4", "Press de Banca con agarre cerrado y bandas 3x5", "Trabajo de cuello y trapecios"]
        ]
    },

    "Calistenia / Street Workout": {
        "Principiante": [
            ["Día 1: Empuje Básico", "Flexiones inclinadas (manos en banco) 4x10", "Fondos en banco 3x12", "Plancha 3x30s"],
            ["Día 2: Tracción Básica", "Remos Australianos (anillas/barra baja) 4x10", "Aguante colgado (Dead hang) 3x30s", "Elevaciones de rodillas colgado 3x10"],
            ["Día 3: Piernas y Core", "Sentadillas al aire (Air Squats) 4x15", "Estocadas 3x12/pierna", "Hollow Body Hold 3x20s"],
            ["Día 4: Empuje y Tracción", "Flexiones en el piso 4x5-8", "Remos invertidos 4x8", "Pinos contra la pared (Wall Walk) 3 repeticiones"],
            ["Día 5: Full Body", "Burpees sin salto 3x10", "Sentadilla isométrica (Wall sit) 3x45s", "Supermans (Lumbares) 3x15"]
        ],
        "Intermedio": [
            ["Día 1: Progresiones Push", "Fondos en paralelas (Dips) 4x8-10", "Flexiones diamante 4x10", "Pino asistido en pared 4x30s"],
            ["Día 2: Progresiones Pull", "Dominadas estrictas (Pull-ups) 4x5-8", "Dominadas supinas (Chin-ups) 3x6-8", "L-Sit en suelo progresiones 4x15s"],
            ["Día 3: Piernas Explosivas", "Pistol Squats asistidas 4x5/pierna", "Saltos al cajón 4x10", "Elevación de talones a una pierna 4x15"],
            ["Día 4: Core y Estáticos", "Progresión Tuck Planche 4x10s", "Elevaciones de piernas a la barra (Toes to bar) 4x8", "Dragon Flag progresiones 4x5"],
            ["Día 5: Resistencia Muscular", "Max repeticiones: Flexiones, Dominadas y Fondos (Circuito 3 rondas)"]
        ],
        "Avanzado": [
            ["Día 1: Estáticos - Empuje", "Straddle Planche intentos 5x5s", "Handstand Push-ups (HSPU) libres 4x5", "Fondos en anillas búlgaros 4x8"],
            ["Día 2: Estáticos - Tracción", "Front Lever progresiones/intentos 5x5s", "Muscle-ups estrictos 4x3-5", "Dominadas a una mano (asistidas) 4x3/brazo"],
            ["Día 3: Piernas y Potencia", "Pistol Squats libres lastradas 4x5/pierna", "Sprints cortos 6x50m", "Nordic Curls 4x5"],
            ["Día 4: Lastre (Street Lifting)", "Dominadas con Lastre (+30kg) 4x5", "Fondos con Lastre (+40kg) 4x5", "L-Sit en anillas 4x20s"],
            ["Día 5: Combinaciones y Freestyle", "Entrenamiento de transiciones en barra", "Práctica de 360s o dinámicos en barra (30 min)", "Acondicionamiento final"]
        ]
    },

    "Resistencia (Running, Ciclismo, Natación)": {
        "Principiante": [
            ["Día 1: Base Aeróbica", "Caminata rápida / Trote suave 20-30 min (Zona 2)", "Estiramientos dinámicos 10 min"],
            ["Día 2: Acondicionamiento Físico", "Sentadillas 3x15", "Planchas 3x30s", "Puentes de glúteo 3x15"],
            ["Día 3: Base Aeróbica", "Ciclismo estático o Natación suave 30 min", "Trabajo de movilidad de cadera"],
            ["Día 4: Intervalos Suaves", "Trote 1 min / Caminata 2 min (Repetir 8 veces)", "Abdominales básicos 3x20"],
            ["Día 5: Tirada 'Larga' Suave", "Caminata sostenida o Trote continuo muy suave 40 min", "Estiramiento completo"]
        ],
        "Intermedio": [
            ["Día 1: Tempo Run / Umbral", "10 min calentamiento, 20 min a ritmo moderado-alto (Tempo), 10 min enfriamiento"],
            ["Día 2: Fuerza Específica", "Estocadas caminando 4x12", "Subidas a cajón 4x10", "Planchas laterales 3x40s"],
            ["Día 3: Intervalos de VO2 Max", "Calentamiento. 6x400m a ritmo fuerte (recuperación 90s). Enfriamiento."],
            ["Día 4: Recuperación Activa", "Bicicleta suave 40 min o Natación continua", "Yoga o movilidad 20 min"],
            ["Día 5: Tirada Larga", "Carrera continua 60-80 min a ritmo conversacional (Zona 2)", "Hidratación y estiramiento profundo"]
        ],
        "Avanzado": [
            ["Día 1: Series Cortas y Potencia", "Calentamiento. 10x200m a sprint (recuperación 60s). Enfriamiento."],
            ["Día 2: Fuerza Máxima y Pliometría", "Sentadilla Tras Nuca pesada 4x5", "Saltos al cajón reactivos 4x8", "Trabajo unilateral de isquios"],
            ["Día 3: Tempo / Umbral Anaeróbico", "Calentamiento. 3x10 min a ritmo de umbral (recuperación 3 min). Enfriamiento."],
            ["Día 4: Recuperación o Doble Turno", "Mañana: Nado suave 45 min. Tarde: Movilidad y rolo miofascial."],
            ["Día 5: Tirada Larga / Fondo", "Carrera o Ciclismo de fondo: 90-120+ min a ritmo de maratón/base", "Reposición de carbohidratos estricta"]
        ]
    },

    "Deportes de Equipo (Fútbol, Básquet, Rugby)": {
        "Principiante": [
            ["Día 1: Fuerza Base", "Sentadillas en Copa 3x12", "Flexiones 3x10", "Plancha 3x30s"],
            ["Día 2: Coordinación y Agilidad", "Drills de escalera de agilidad 15 min", "Saltos a la cuerda 4x2 min"],
            ["Día 3: Core y Estabilidad", "Bird-Dog 3x12/lado", "Puente de glúteos a 1 pierna 3x10", "Rotaciones de tronco con banda 3x15"],
            ["Día 4: Potencia Básica", "Saltos largos sin impulso 4x5", "Lanzamiento de balón medicinal (pecho) 3x10", "Estocadas laterales 3x10"],
            ["Día 5: Acondicionamiento (GPP)", "Carrera continua 25 min", "Estiramientos balísticos"]
        ],
        "Intermedio": [
            ["Día 1: Fuerza Explosiva", "Power Clean colgante (Hang Clean) 4x5", "Sentadilla Frontal 4x8", "Press Militar 4x8"],
            ["Día 2: Cambio de Dirección (COD)", "Sprints en 'T' o Conos", "Desplazamientos defensivos laterales con banda 4x30s"],
            ["Día 3: Resistencia Intermitente", "Método Tartan: 15s sprint / 15s trote pasivo x 10 minutos", "Abdominales con peso 4x15"],
            ["Día 4: Potencia Unilateral", "Subidas al cajón explosivas 4x6/pierna", "Press a una mano con mancuerna 4x8", "Pallof Press (Core anti-rotación) 3x15"],
            ["Día 5: Prevención de Lesiones", "Nordic Curls 3x6", "Ejercicios propioceptivos en Bosu", "Copenhagen Planks (Aductores) 3x30s"]
        ],
        "Avanzado": [
            ["Día 1: Fuerza Máxima y Potencia de Contraste", "Sentadilla Tras Nuca 4x3 (Pesado) superseriado con 5 Saltos al Cajón altos", "Press de Banca 4x4"],
            ["Día 2: Velocidad y Agilidad Reactiva", "Sprints resistidos (Paracaídas o Trineo) 6x15m", "Ejercicios de reacción a estímulo visual/sonoro"],
            ["Día 3: Potencia en Planos Transversales", "Lanzamientos rotacionales con balón medicinal pesado 4x8/lado", "Landmine Rotations 4x10"],
            ["Día 4: Resistencia Específica al Deporte", "Circuitos RSA (Repeated Sprint Ability): 6x30m Sprints con 20s de pausa", "Trabajo de cuello y trapecios (Rugby/Fútbol)"],
            ["Día 5: Prevención Elite y Pliometría", "Drop Jumps (Caída desde cajón + rebote) 4x5", "Trabajo excéntrico de Isquiotibiales en máquina inercial o polea"]
        ]
    },

    "Artes Marciales / Deportes de Contacto": {
        "Principiante": [
            ["Día 1: Acondicionamiento Básico", "Saltos a la cuerda 3x3 min", "Flexiones de brazos 3x10", "Sentadillas libres 3x20"],
            ["Día 2: Core y Cuello", "Crunches 4x25", "Puentes isométricos de cuello 3x30s", "Plancha lateral 3x30s"],
            ["Día 3: Sombra y Movimiento", "Sombra de boxeo/kickboxing con pesas ligeras (1kg) 3x3 min", "Desplazamientos (Footwork) 15 min"],
            ["Día 4: Potencia Ligera", "Burpees 4x10", "Lanzamiento de balón medicinal al piso (Slams) 3x15", "Dominadas isométricas 3x15s"],
            ["Día 5: Flexibilidad y Movilidad", "Estiramientos estáticos y dinámicos enfocados en caderas y hombros (30 min)"]
        ],
        "Intermedio": [
            ["Día 1: Fuerza Específica", "Sentadilla Frontal 4x8", "Press Militar 4x8", "Remo con barra 4x10", "Encogimientos de trapecios 4x15"],
            ["Día 2: Resistencia Anaeróbica Láctica", "Golpeo al saco (Heavy Bag): 5 rounds de 3 min a máxima intensidad (1 min descanso)"],
            ["Día 3: Potencia Rotacional", "Golpes con mazo a neumático (Sledgehammer) 4x15/lado", "Rotaciones rusas con disco 4x20"],
            ["Día 4: Condicionamiento Específico", "Sprawls (defensa de derribo) 4x15", "Saltos al cajón 4x10", "Dominadas 4x8"],
            ["Día 5: Sparring o Drills de Alta Intensidad", "Drills de combate con compañero", "Trabajo intenso de cuello con arnés 3x15"]
        ],
        "Avanzado": [
            ["Día 1: Fuerza Explosiva (Fight Camp)", "Power Cleans 5x3", "Press de Banca Explosivo (cadenas/bandas) 5x3", "Sentadilla Búlgara pesada 4x6/pierna"],
            ["Día 2: Sistema Energético Anaeróbico Aláctico", "Sprints en colina (Hill Sprints) 10x30m (Descanso total)", "Pliometría de tren superior (Flexiones con palmada) 4x6"],
            ["Día 3: Acondicionamiento en Saco", "Burnouts en saco pesado: 30s golpes rectos max velocidad / 30s potencia (Repetir 6 min continuos)"],
            ["Día 4: Fuerza Isométrica y Agarre", "Paseo del Granjero (Farmer's Walk) pesado 4x40m", "Dominadas colgado de toalla (Grip) 4xMáx", "Abrazos de oso con saco de arena (Sandbag hold) 4x45s"],
            ["Día 5: Simulación de Combate", "Sparring duro 5 rounds o Circuito metabólico imitando duración del round (Ej: 5 min MMA / 3 min Boxeo)"]
        ]
    },

    "Deportes de Raqueta (Tenis, Pádel)": {
        "Principiante": [
            ["Día 1: Fuerza General", "Sentadillas Goblet 3x15", "Remo TRX 3x12", "Planchas 3x30s"],
            ["Día 2: Desplazamientos Básicos", "Saltos a la cuerda 10 min", "Desplazamientos laterales (Side steps) 4x20m", "Estocadas 3x12/pierna"],
            ["Día 3: Core Rotacional", "Rotaciones rusas 3x20", "Woodchoppers en polea (bajos) 3x12/lado", "Crunches oblicuos 3x15"],
            ["Día 4: Acondicionamiento Aeróbico", "Bicicleta o Trote suave 30 min", "Estiramientos de hombros y antebrazos"],
            ["Día 5: Agilidad Ligera", "Drills de escalera de agilidad", "Saques simulados con banda elástica (resistencia ligera) 3x15"]
        ],
        "Intermedio": [
            ["Día 1: Fuerza y Estabilidad", "Estocadas Multidireccionales (Reloj) 3x3 rondas/pierna", "Press Inclinado mancuernas 4x10", "Remo a un brazo 4x10"],
            ["Día 2: Velocidad y Cambio de Dirección", "Sprints 5m, 10m y frenado", "Drills de la 'Araña' (recoger pelotas en la cancha)"],
            ["Día 3: Potencia del Core", "Lanzamientos laterales con Balón Medicinal contra pared 4x10/lado", "Planchas laterales con rotación 3x12/lado"],
            ["Día 4: Fuerza del Brazo Dominante/No Dominante", "Rotaciones externas/internas manguito rotador con bandas 4x15", "Curl y Extensión de muñeca 3x20"],
            ["Día 5: Resistencia Anaeróbica Específica", "Suicidios en cancha de tenis 5 series", "Shadow Tennis (Simulación de golpes rápidos) 5 min"]
        ],
        "Avanzado": [
            ["Día 1: Potencia Pliométrica Unilateral", "Skater Jumps (Saltos laterales) 4x8/pierna", "Lanzamiento de balón medicinal en suspensión (simulando saque) 4x6"],
            ["Día 2: Fuerza Máxima y Contraste", "Sentadilla Tras Nuca 4x4", "Inmediatamente después: 6 Saltos explosivos", "Press Militar pesado 4x6"],
            ["Día 3: Agilidad Reactiva Elite", "Reacción a luces o comandos de voz (Cambios de dirección fulminantes)", "Sprints con freno excéntrico máximo"],
            ["Día 4: Prevención de Lesiones Específica", "Trabajo intensivo manguito rotador excéntrico", "Fortalecimiento de tendón rotuliano (Isométricos pesados)", "Core Anti-extensión intenso"],
            ["Día 5: HIIT Específico en Cancha", "Intervalos de trabajo de 15s a máxima intensidad (golpeo) / 15s descanso (Simulación de rally largo). 10 repeticiones x 3 series."]
        ]
    },

    "Pilates / Yoga / Movilidad": {
        "Principiante": [
            ["Día 1: Fundamentos", "Respiración diafragmática 5 min", "Gato-Vaca 10 reps", "Postura del Niño (Balasana) 2 min"],
            ["Día 2: Core Básico (Pilates)", "The Hundred (adaptado) 5 respiraciones", "Pelvic Curls (Puente pélvico) 10 reps", "Single Leg Stretch 10 reps"],
            ["Día 3: Flexibilidad Isométrica", "Postura del Perro Boca Abajo (Adho Mukha Svanasana) 3x30s", "Postura de la Montaña (Tadasana) con alineación postural"],
            ["Día 4: Movilidad Articular", "Círculos de cadera 10/lado", "Rotaciones torácicas en cuadrupedia 10/lado", "Rotaciones de cuello y hombros"],
            ["Día 5: Integración", "Secuencia de Saludos al Sol A (modificados) x 5", "Relajación Final (Savasana) 10 min"]
        ],
        "Intermedio": [
            ["Día 1: Flow de Vinyasa", "Saludos al Sol A y B x 5", "Transiciones a Guerreros I, II y III", "Equilibrio: Postura del Árbol (Vrksasana)"],
            ["Día 2: Pilates Mat Clásico", "The Roll Up 8 reps", "The Teaser (Progresiones) 5 reps", "Criss Cross 15 reps/lado", "Double Leg Stretch 10 reps"],
            ["Día 3: Apertura de Caderas e Isquios", "Postura de la Paloma (Kapotasana) 2 min/lado", "Pliegue hacia adelante sentado (Paschimottanasana)", "Happy Baby"],
            ["Día 4: Fuerza Estabilizadora", "Planchas laterales (Vashistasana) 45s/lado", "Postura del Bote (Navasana) 4x30s", "Extensiones de espalda (Swan Dive)"],
            ["Día 5: Inversiones Básicas y Movilidad Activa", "Progresión Parada de Cabeza (Sirsasana) con pared", "Movilidad CARs (Controlled Articular Rotations) nivel 2"]
        ],
        "Avanzado": [
            ["Día 1: Ashtanga Primary Series (Porción)", "Secuencia completa vigorosa (hasta Navasana)", "Uso avanzado de Bandhas (cierres energéticos)"],
            ["Día 2: Pilates Reformer/Mat Elite", "The Jackknife", "The Boomerang", "Control Balance", "Push Ups Pilates avanzado"],
            ["Día 3: Flexibilidad Extrema", "Splits frontales (Hanumanasana) activo y pasivo", "Postura de la Rueda (Urdhva Dhanurasana) progresiones de drop-backs"],
            ["Día 4: Equilibrio en Brazos e Inversiones", "Postura del Cuervo (Bakasana) a Parada de Manos (Adho Mukha Vrksasana)", "Pincha Mayurasana (Equilibrio en antebrazos)"],
            ["Día 5: Restauración Profunda (Yin Yoga)", "Mantenciones de posturas profundas por 5-8 minutos", "Respiración Pranayama (Nadi Shodhana avanzado)"]
        ]
    },

    "Danza / Baile Deportivo": {
        "Principiante": [
            ["Día 1: Base Postural", "Alineación en primera y segunda posición (Ballet básico)", "Elevaciones de gemelos (Relevé) 4x15", "Plancha abdominal 3x30s"],
            ["Día 2: Movilidad Articular", "Círculos de cadera, tobillos y muñecas 15 min", "Estiramiento mariposa 3 min", "Apertura lateral suave"],
            ["Día 3: Resistencia Coreográfica", "Repetición de pasos básicos al ritmo de la música 30 min continuos", "Respiración acompasada"],
            ["Día 4: Fuerza del Core", "Crunches 3x20", "Superman (lumbares) 3x15", "Elevación de piernas acostado 3x15"],
            ["Día 5: Expresión Corporal y Flexibilidad", "Improvisación libre 15 min", "Estiramientos isquiotibiales y cuádriceps profundos"]
        ],
        "Intermedio": [
            ["Día 1: Fuerza Explosiva Ligera", "Saltos verticales (Sautés) 4x15", "Estocadas cruzadas (Curtsy lunges) 3x12/lado", "Puente de glúteo a una pierna 3x12/lado"],
            ["Día 2: Equilibrio y Estabilidad", "Mantenciones en equilibrio a una pierna (Passé) 4x45s/lado", "Giros simples (Pirouettes) práctica 15 min", "Bosu ball balance"],
            ["Día 3: Resistencia Anaeróbica Láctica", "Pasadas coreográficas a intensidad de competencia (Full Out) x 5", "Descanso activo 1 min entre pasadas"],
            ["Día 4: Apertura y Flexibilidad Activa", "Desarrollos de pierna al frente y lateral (Développé) 3x8/lado", "Isométricos en máxima extensión", "Splits asistidos"],
            ["Día 5: Acondicionamiento Complementario", "Pilates para bailarines (Teaser, Roll ups)", "Fortalecimiento de tobillos con bandas elásticas 4x20"]
        ],
        "Avanzado": [
            ["Día 1: Pliometría y Potencia de Salto", "Grand Jeté (Saltos largos) progresiones", "Tuck Jumps (Saltos al pecho) 4x10", "Fuerza máxima excéntrica para recepción de saltos"],
            ["Día 2: Control Isométrico Elite", "Mantenciones de pierna en alto a 90° o más (Isométrico sin manos) 4x30s/lado", "Fuerza profunda de psoas e ilíaco"],
            ["Día 3: Simulación de Performance", "Ejecución de rutina completa 3 veces sin descanso (Resistencia extrema)", "Corrección técnica bajo fatiga"],
            ["Día 4: Prevención de Lesiones Específica", "Trabajo avanzado de tendón de Aquiles y rodillas", "Core anti-extensión (Dragon flags)", "Liberación de fascia plantar"],
            ["Día 5: Flexibilidad Extrema y Contorsionismo Básico", "Oversplits (Splits con elevación frontal/trasera)", "Flexibilidad de columna extrema (Cambré profundo)"]
        ]
    },

    "Gimnasia Artística / Rítmica": {
        "Principiante": [
            ["Día 1: Acondicionamiento Básico (Fuerza)", "Hollow Body Hold 4x20s", "Arch Body Hold (Superman) 4x20s", "Flexiones de brazos 3x10"],
            ["Día 2: Flexibilidad General", "Splits frontales asistidos", "Pike stretch (Plegado al frente) 3x1 min", "Puente básico 3x15s"],
            ["Día 3: Posturas Estáticas", "Práctica de vertical (Pino) de cara a la pared 4x20s", "Parada de cabeza básica 3x30s"],
            ["Día 4: Fuerza de Piernas y Saltos", "Saltos en extensión 4x15", "Sentadillas profundas 3x20", "Elevaciones de talón 4x20"],
            ["Día 5: Bases Rítmicas/Aparatos", "Manipulación básica de aro, cinta o pelota", "Coordinación ojo-mano"]
        ],
        "Intermedio": [
            ["Día 1: Fuerza de Empuje y Tracción", "Fondos en paralelas 4x8", "Dominadas supinas 4x6", "Progresión L-Sit 4x15s"],
            ["Día 2: Tumbling (Acrobacia Básica)", "Rondadas", "Flic Flac (Back Handspring) en trampolín/asistido", "Ruedas laterales (Medialuna) 4x10"],
            ["Día 3: Flexibilidad Activa", "Lanzamientos de pierna (Battements) en todos los planos 3x15/pierna", "Puente caminando (Walkovers)"],
            ["Día 4: Estáticos en Anillas / Barra", "Skin the cat 4x3", "Soporte (Support hold) en anillas 4x20s", "Balanceos (Swings) técnicos en barra"],
            ["Día 5: Resistencia Coreográfica", "Pasadas de rutina a piso/aparatos completas", "Fuerza específica de empeines y puntas"]
        ],
        "Avanzado": [
            ["Día 1: Estáticos de Alta Dificultad", "Progresiones de Plancha (Planche) en suelo o anillas", "Progresiones de Cristo (Iron Cross) con poleas", "Manna o V-Sit alto"],
            ["Día 2: Acrobacia Elite", "Múltiples giros (Twists) en saltos", "Mortales dobles en foso de espuma", "Conexiones de Tumbling complejas"],
            ["Día 3: Potencia Pliométrica Extrema", "Saltos desde cajón alto (Drop jumps) con rebote máximo", "Pliometría de tren superior (HSPU con aplauso asistidas)"],
            ["Día 4: Sobrecarga Excéntrica (Prevención)", "Trabajo intenso de protección de manguito rotador y codos", "Nordic Curls", "Acondicionamiento de muñecas"],
            ["Día 5: Perfeccionamiento de Rutina de Competición", "Limpieza de descuentos técnicos bajo máxima presión cardíaca", "Evaluación de amplitudes y aterrizajes (Sticks)"]
        ]
    },

    "Rehabilitación / Fisioterapia Activa": {
        "Principiante": [
            ["Día 1: Isométricos y Control del Dolor", "Contracciones isométricas suaves de la zona afectada 5x10s", "TENS o aplicación de frío/calor", "Movilidad pasiva"],
            ["Día 2: ROM (Rango de Movimiento)", "Movilizaciones articulares sin dolor (Pain-free ROM) 3x15", "Estiramientos muy suaves 3x30s"],
            ["Día 3: Activación Muscular Aislada", "Ejercicios con banda elástica de muy baja resistencia 3x15", "Trabajo propioceptivo básico (pararse en una pierna)"],
            ["Día 4: Respiración y Core Base", "Respiración diafragmática 10 min", "Activación del transverso abdominal (Drawing-in maneuver) 4x10"],
            ["Día 5: Descanso y Evaluación", "Reevaluación de los niveles de dolor y rigidez", "Caminata muy ligera (si está permitida)"]
        ],
        "Intermedio": [
            ["Día 1: Fortalecimiento Concéntrico Ligero", "Ejercicios isotónicos con peso ligero o bandas 4x12", "Cadenas cinéticas cerradas (ej: prensa de piernas suave)"],
            ["Día 2: Propiocepción y Equilibrio", "Sentadillas sobre Bosu o almohadón 3x10", "Alcances en estrella a una pierna 3x5/pierna"],
            ["Día 3: Control Neuromuscular", "Ejercicios de estabilización rítmica", "Trabajo de core intermedio (Dead bugs, Bird dogs) 3x12/lado"],
            ["Día 4: Progresión de Carga", "Aumento progresivo del peso en ejercicios clave (Regla del 10%)", "Estiramientos activos"],
            ["Día 5: Acondicionamiento Cardiovascular Suave", "Bicicleta estática o Elíptico 20-30 min a ritmo moderado (sin impacto)"]
        ],
        "Avanzado": [
            ["Día 1: Trabajo Excéntrico Pesado", "Fase excéntrica de 4-5 segundos en ejercicios de la zona recuperada", "Prevención de recaídas tendinosas"],
            ["Día 2: Retorno a la Actividad (Return to Play)", "Drills específicos del deporte o actividad laboral a velocidad media", "Cambios de dirección controlados"],
            ["Día 3: Fuerza Funcional Integrada", "Movimientos multiplanares (Levantamientos olímpicos ligeros o Kettlebell swings)", "Sentadillas y Pesos muertos con técnica estricta"],
            ["Día 4: Pliometría y Absorción de Impacto", "Saltos suaves prestando atención al aterrizaje", "Drills de agilidad con desaceleración (Frenado)"],
            ["Día 5: Alta Intensidad Controlada", "Simulación del escenario real (competencia/rutina pesada) bajo supervisión de fatiga y molestias"]
        ]
    },

    "Ninguno (Sedentario)": {
        "Principiante": [
            ["Día 1: Primeros Pasos", "Caminata suave 15-20 min", "Movilidad de articulaciones (cuello, hombros, rodillas) 5 min"],
            ["Día 2: Despertar Muscular", "Sentarse y pararse de una silla 3x10", "Empuje de pared (Flexiones de pie) 3x10", "Estiramientos en silla"],
            ["Día 3: Movimiento Suave", "Caminata 20 min", "Respiraciones profundas y relajación 10 min"],
            ["Día 4: Core y Postura", "Puente de glúteos en el suelo 3x10", "Rodillas al pecho acostado 3x15s", "Activación abdominal isométrica"],
            ["Día 5: Cierre de Semana", "Paseo recreativo 30 min a ritmo cómodo", "Estiramientos generales"]
        ],
        "Intermedio": [
            ["Día 1: Caminata Activa y Base", "Caminata a ritmo ligero 30 min", "Sentadillas libres (sin silla) 3x12"],
            ["Día 2: Fuerza con Peso Corporal", "Flexiones apoyando rodillas 3x10", "Estocadas estáticas 3x10/pierna", "Plancha abdominal 3x20s"],
            ["Día 3: Cardio Ligero", "Bicicleta, Elíptico o Caminata rápida 30-40 min", "Estiramientos"],
            ["Día 4: Tren Superior y Core", "Remo con bandas elásticas o botellas de agua 3x15", "Vuelos laterales ligeros 3x15", "Crunches cortos 3x15"],
            ["Día 5: Circuito Básico", "3 Rondas: 10 Sentadillas, 10 Flexiones en pared, 20 Jumping Jacks (sin salto/paso lateral), 30s Plancha"]
        ],
        "Avanzado": [
            ["Día 1: Transición a Entrenamiento Formal", "Caminata rápida/Trote suave 30 min", "Sentadillas Goblet con peso ligero 3x15"],
            ["Día 2: Entrenamiento de Fuerza Full Body", "Press con mancuernas ligeras 3x12", "Remo con mancuernas 3x12", "Estocadas caminando 3x12/pierna"],
            ["Día 3: Intervalos de Cardio (HIIT Suave)", "1 min trote / 1 min caminata (Repetir 10 veces)"],
            ["Día 4: Fuerza y Core", "Flexiones clásicas (o rodillas avanzadas) 3x10", "Ab Wheel o Planchas largas 3x40s", "Hip Thrust 3x15"],
            ["Día 5: Circuito Metabólico", "4 Rondas por tiempo: 15 Sentadillas, 10 Burpees adaptados, 15 Sit-ups, 200m trote"]
        ]
    }
}