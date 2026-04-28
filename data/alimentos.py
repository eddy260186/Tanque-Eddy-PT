# ==========================================
# 2. BASE DE DATOS (ALIMENTOS COMPLETOS)
# ==========================================
alimentos_db = {
    "Prot_Desayuno": [
        "Yogur Griego Natural", "Yogur Natural Descremado", "Huevo Entero", "Claras de Huevo", 
        "Queso Cottage", "Whey Protein", "Jamón Cocido Magro", "Ricotta Magra", "Tofu Suave", 
        "Queso Feta", "Kefir de Leche", "Queso Blanco", "Huevo Poché", "Leche Proteica", 
        "Batido de Proteína", "Queso Magro", "Yogur de Soja", "Requesón", "Proteína de Soja", 
        "Queso Quark", "Yogur Skyr", "Queso Untable Proteico", "Jamón de Pavo", "Huevos Revueltos",
        "Omellete de Claras", "Batido de Caseína", "Queso Mascarpone Light", "Yogur de Coco (Protein)",
        "Queso Brie (Porción)", "Salame de Pavo", "Lomo Embuchado", "Pechuga Ahumada"
    ],
    "Bebidas_Arg": ["Mate Amargo", "Café solo/cortado", "Té de Hierbas", "Mate Cocido", "Té con Limón"],
    "Bebidas_Gral": ["Café Negro", "Té Verde", "Infusión de Manzanilla", "Té de Frutos Rojos", "Té Negro", "Café Helado sin azúcar", "Agua con Limón", "Infusión de jengibre", "Agua con Gas"],
    "Prot_Principal": [
        "Pechuga de Pollo", "Lomo Vacuno Magro", "Solomillo de Cerdo", "Pechuga de Pavo", 
        "Cordero Magro", "Bife de Cuadril", "Conejo", "Bisonte", "Ternera Magra", "Pollo a la Parrilla", 
        "Bife de Chorizo Magro", "Pavo Horneado", "Carne de Ciervo", "Costilla de Cerdo Magra", 
        "Pollo al Horno", "Cuadril", "Vacío Magro", "Peceto", "Bola de Lomo", "Nalga",
        "Bondiola Desgrasada", "Entraña Magra", "Lomito de Cerdo", "Carne Picada Magra",
        "Matambre Vacuno (Magro)", "Colita de Cuadril", "Paleta Vacuna", "Tortuguita",
        "Bife Angosto", "Tapa de Asado (Limpia)", "Panceta de Pavo", "Churrasco de Pollo"
    ],
    "Prot_Pescado": [
        "Merluza", "Salmón Fresco", "Atún al Natural", "Trucha", "Sardinas", "Mejillones", 
        "Gambas/Camarones", "Pulpo", "Abadejo", "Lenguado", "Pejerrey", "Caballa", "Mariscos Mix", 
        "Bacalao", "Calamar", "Anillas de Calamar", "Corvina", "Dorado", "Surubí", "Salmón Ahumado", 
        "Lomito de Atún Fresco", "Filet de Pescado Blanco", "Besugo", "Langostinos al Ajillo", 
        "Brocheta de Pescado", "Atún Rojo", "Gatuzo"
    ],
    "Prot_Vegana": [
        "Tofu Firme", "Tempeh", "Seitan", "Lentejas", "Garbanzos", "Heura", "Soja Texturizada", 
        "Frijoles Negros (Feijão)", "Guisantes", "Quinoa", "Altramuces", "Edamame", "Proteína de Guisante", 
        "Levadura Nutricional", "Semillas de Chía", "Espirulina", "Amaranto", "Cáñamo", "Miso", 
        "Tempeh de Garbanzos", "Hamburguesa de Soja", "Porotos Mung", "Lupines", "Porotos Colorados", 
        "Tofu Ahumado", "Natto", "Proteína de Arroz", "Frijol de Carita"
    ],
    "Carb_Desayuno": [
        "Avena en Hojuelas", "Pan de Centeno", "Granola sin Azúcar", "Pan de Masa Madre", "Fruta Picada", 
        "Tortitas de Arroz", "Muesli", "Espelta", "Salvado de Trigo", "Cereales Integrales", "Pan Integral", 
        "Tortitas de Avena", "Arándanos", "Manzana", "Banana", "Kiwi", "Fresa", "Mango", "Pera", 
        "Ciruelas", "Tapioca (Brasil)", "Mamão / Papaya", "Açaí puro", "Arepa de Maíz", "Galletas de Arroz", 
        "Pan de Sarraceno", "Dátiles", "Higos", "Melón", "Piña / Ananá", "Pomelo", "Sandía"
    ],
    "Carb_Principal": [
        "Arroz Integral", "Pasta Integral", "Quinoa Real", "Cuscús", "Lentejas", "Garbanzos", 
        "Arroz Basmati", "Pasta de Legumbres", "Bulgur", "Polenta", "Mijo", "Trigo Sarraceno", "Choclo", 
        "Trigo Burgol", "Arroz Negro", "Kamut", "Espelta", "Cebada", "Fideos de Arroz", "Yuca/Mandioca/Macaxeira", 
        "Feijão Preto (Brasil)", "Plátano Macho", "Puré de Papa", "Arroz Blanco", "Ñoquis de Papa", 
        "Batata Asada", "Trigo en Grano", "Garbanzos Fritos", "Arroz de Coliflor", "Pasta de Espelta", 
        "Sémola de Trigo", "Arvejas Partidas"
    ],
    "Carb_Vegetales": [
        "Papa Hervida", "Batata al Horno", "Calabaza", "Yuca/Mandioca", "Zanahoria", "Remolacha", 
        "Boniato", "Plátano Macho", "Nabos", "Pastinaca", "Calabacín", "Berenjena", "Puerros", "Cebolla", 
        "Alcachofas", "Pimientos", "Zapallo Anco", "Hinojo", "Rabanitos", "Tomates", "Brócoli", "Coliflor", 
        "Espinaca (Volumen libre)", "Zapallo Cabutia", "Echalotes", "Ajo", "Champiñones", "Portobello", "Repollo Colorado"
    ],
    "Verduras_Keto": [
        "Espinaca", "Brócoli", "Espárragos", "Acelga", "Coliflor", "Lechuga", "Pepino", "Zucchini", 
        "Champiñones", "Pimientos", "Kale", "Rúcula", "Apio", "Tomatitos Cherry", "Rabanitos", "Endivias", 
        "Bok Choy", "Col de Bruselas", "Judías Verdes", "Hinojo", "Repollo Blanca", "Berenjena", "Berros", 
        "Brotes de Soja", "Radicheta"
    ],
    "Grasas": [
        "Palta/Aguacate", "Nueces", "Aceite de Oliva", "Almendras", "Pistachos", "Semillas de Zapallo", 
        "Mantequilla de Maní", "Aceitunas", "Aceite de Coco", "Castañas de Cajú", "Tahini", "Avellanas", 
        "Aceite de Lino", "Nueces de Macadamia", "Semillas de Girasol", "Coco Rallado", "Mantequilla de Pasto", 
        "Yema de Huevo", "Chía", "Sésamo", "Chocolate Amargo 85%", "Ghee (Manteca Clarificada)", "Pasta de Almendras", 
        "Aceite de Girasol Alto Oleico", "Manteca de Cacao", "Crema de Leche Light", "Queso Azul (Porción)", 
        "Mayonesa de Oliva", "Aceite de Sésamo", "Nueces Pecán"
    ]
}

