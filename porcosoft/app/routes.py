from flask import current_app, jsonify
from flask import current_app, jsonify, request # ¡Añade request aquí!
import sqlite3

# Nota: Usamos current_app que es una referencia a la app que creamos en __init__.py
# Así no tenemos que importarla directamente.

def get_db_connection():
    conn = sqlite3.connect('app/database.db') # Ojo con la nueva ruta a la DB
    conn.row_factory = sqlite3.Row
    return conn

@current_app.route('/api/animales')
def get_animales():
    conn = get_db_connection()
    animales_cursor = conn.execute('SELECT * FROM Animales').fetchall()
    conn.close()

    animales_lista = [dict(row) for row in animales_cursor]
    return jsonify(animales_lista)

@current_app.route('/api/alimentacion') 
def get_alimentacion():
    conn = get_db_connection()
    alimentacion_cursor = conn.execute('SELECT * FROM Alimentacion').fetchall()
    conn.close()

    alimentacion_lista = [dict(row) for row in alimentacion_cursor]
    return jsonify(alimentacion_lista)

@current_app.route('/api/sanidad')  
def get_sanidad():
    conn = get_db_connection()
    sanidad_cursor = conn.execute('SELECT * FROM Sanidad').fetchall()
    conn.close()

    sanidad_lista = [dict(row) for row in sanidad_cursor]
    return jsonify(sanidad_lista)

@current_app.route('/api/Eventos_Reproductivos')    
def get_reproductores():
    conn = get_db_connection()
    reproductores_cursor = conn.execute('SELECT * FROM Eventos_Reproductivos').fetchall()
    conn.close()

    reproductores_lista = [dict(row) for row in reproductores_cursor]
    return jsonify(reproductores_lista)




# --- NUEVA RUTA ---
# Obtener un solo animal por su ID
@current_app.route('/api/animales/<int:animal_id>')
def get_animal(animal_id):
    conn = get_db_connection()
    # Usamos '?' para pasar variables de forma segura y prevenir inyección SQL
    animal_row = conn.execute('SELECT * FROM Animales WHERE id = ?', (animal_id,)).fetchone()
    conn.close()

    # Si la consulta no devuelve nada, el animal no existe
    if animal_row is None:
        # Devolvemos un error 404 (No Encontrado), que es el estándar
        return jsonify({'error': 'Animal no encontrado'}), 404

    # Si encontramos el animal, lo devolvemos como JSON
    return jsonify(dict(animal_row))



# --- RUTA POST---
@current_app.route('/api/animales', methods=['POST'])
def create_animal():
    data = request.get_json()

    # Extracción de todos los campos (nuevos y viejos)
    arete_id = data.get('arete_id')
    nombre = data.get('nombre')
    raza = data.get('raza')
    color = data.get('color')
    sexo = data.get('sexo')
    fecha_nacimiento = data.get('fecha_nacimiento')
    peso_nacimiento_kg = data.get('peso_nacimiento_kg')
    fecha_destete = data.get('fecha_destete')
    peso_destete_kg = data.get('peso_destete_kg')
    origen = data.get('origen')
    lote_id = data.get('lote_id')
    es_reproductor = data.get('es_reproductor')
    estado = data.get('estado')
    fecha_salida = data.get('fecha_salida')
    notas = data.get('notas')

    # Validación
    if not arete_id or not sexo:
        return jsonify({'error': 'El arete_id y el sexo son campos obligatorios'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Sentencia INSERT con todos los nuevos campos
    sql = '''INSERT INTO Animales (arete_id, nombre, raza, color, sexo, fecha_nacimiento, peso_nacimiento_kg, fecha_destete, peso_destete_kg, origen, lote_id,  es_reproductor, estado, fecha_salida, notas) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    
    cursor.execute(sql, ((arete_id, nombre, raza, color, sexo, fecha_nacimiento, peso_nacimiento_kg, fecha_destete, peso_destete_kg, origen, lote_id,  es_reproductor, estado, fecha_salida, notas) 
        
    ))
    
    conn.commit()
    new_animal_id = cursor.lastrowid
    conn.close()

    return jsonify({'message': 'Animal creado con éxito', 'id': new_animal_id}), 201




# --- RUTA PUT ACTUALIZADA ---
@current_app.route('/api/animales/<int:animal_id>', methods=['PUT'])
def update_animal(animal_id):
    data = request.get_json()

    # Extraemos todos los datos (nuevos y viejos)
    arete_id = data.get('arete_id')
    nombre = data.get('nombre')
    raza = data.get('raza')
    color = data.get('color')
    sexo = data.get('sexo')
    fecha_nacimiento = data.get('fecha_nacimiento')
    peso_nacimiento_kg = data.get('peso_nacimiento_kg')
    fecha_destete = data.get('fecha_destete')
    peso_destete_kg = data.get('peso_destete_kg')
    origen = data.get('origen')
    lote_id = data.get('lote_id')
    es_reproductor = data.get('es_reproductor')
    estado = data.get('estado')
    fecha_salida = data.get('fecha_salida')
    notas = data.get('notas')

    # Validación
    if not arete_id or not sexo:
        return jsonify({'error': 'El arete_id y el sexo son campos obligatorios'}), 400

    conn = get_db_connection()
    # Verificamos si el animal existe
    animal_existente = conn.execute('SELECT id FROM Animales WHERE id = ?', (animal_id,)).fetchone()

    if animal_existente is None:
        conn.close()
        return jsonify({'error': 'Animal no encontrado'}), 404

    # Actualizamos el animal con todos los campos
    sql = '''UPDATE Animales SET 
                arete_id = ?, nombre = ?, raza = ?, color = ?, sexo = ?, fecha_nacimiento = ?,  peso_nacimiento_kg = ?, fecha_destete = ?, peso_destete_kg = ?, origen = ?,  lote_id = ?, es_reproductor = ?, estado = ?, fecha_salida = ?, notas = ? WHERE id = ?'''
    
    conn.execute(sql, (
        arete_id, nombre, raza, color, sexo, fecha_nacimiento, peso_nacimiento_kg, fecha_destete, 
        peso_destete_kg, origen, lote_id, es_reproductor, estado, fecha_salida, notas, animal_id
    ))
    
    conn.commit()
    conn.close()

    return jsonify({'message': 'Animal actualizado con éxito'})




# --- NUEVA RUTA ---
# Eliminar un animal por su ID
@current_app.route('/api/animales/<int:animal_id>', methods=['DELETE'])
def delete_animal(animal_id):
    conn = get_db_connection()
    # Verificamos si el animal existe antes de intentar borrarlo
    animal_existente = conn.execute('SELECT id FROM Animales WHERE id = ?', (animal_id,)).fetchone()

    if animal_existente is None:
        conn.close()
        return jsonify({'error': 'Animal no encontrado'}), 404

    # Si existe, lo eliminamos con el comando DELETE de SQL
    conn.execute('DELETE FROM Animales WHERE id = ?', (animal_id,))
    conn.commit() # ¡No olvides el commit para guardar el cambio!
    conn.close()

    # Un DELETE exitoso no necesita devolver el objeto, solo una confirmación.
    return jsonify({'message': 'Animal eliminado con éxito'})






# =======================================
# RUTAS PARA EL MÓDULO DE LOTES
# =======================================

# --- NUEVA RUTA ---
# Obtener todos los lotes
@current_app.route('/api/lotes')
def get_lotes():
    conn = get_db_connection()
    lotes_cursor = conn.execute('SELECT * FROM Lotes').fetchall()
    conn.close()

    lotes_lista = [dict(row) for row in lotes_cursor]
    return jsonify(lotes_lista)




# --- NUEVA RUTA ---
# Crear un nuevo lote
@current_app.route('/api/lotes', methods=['POST'])
def create_lote():
    data = request.get_json()

    nombre_lote = data.get('nombre_lote')
    descripcion = data.get('descripcion')

    if not nombre_lote:
        return jsonify({'error': 'El nombre_lote es obligatorio'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO Lotes (nombre_lote, descripcion) VALUES (?, ?)',
        (nombre_lote, descripcion)
    )
    conn.commit()
    new_lote_id = cursor.lastrowid
    conn.close()

    return jsonify({'message': 'Lote creado con éxito', 'id': new_lote_id}), 201




# --- NUEVA RUTA ---
# Obtener un solo lote por su ID
@current_app.route('/api/lotes/<int:lote_id>')
def get_lote(lote_id):
    conn = get_db_connection()
    lote = conn.execute('SELECT * FROM Lotes WHERE id = ?', (lote_id,)).fetchone()
    conn.close()
    if lote is None:
        return jsonify({'error': 'Lote no encontrado'}), 404
    return jsonify(dict(lote))

# --- NUEVA RUTA ---
# Actualizar un lote existente
@current_app.route('/api/lotes/<int:lote_id>', methods=['PUT'])
def update_lote(lote_id):
    data = request.get_json()
    nombre_lote = data.get('nombre_lote')
    descripcion = data.get('descripcion')

    if not nombre_lote:
        return jsonify({'error': 'El nombre_lote es obligatorio'}), 400

    conn = get_db_connection()
    # Verificamos si el lote existe
    lote_existente = conn.execute('SELECT id FROM Lotes WHERE id = ?', (lote_id,)).fetchone()
    if lote_existente is None:
        conn.close()
        return jsonify({'error': 'Lote no encontrado'}), 404

    conn.execute(
        'UPDATE Lotes SET nombre_lote = ?, descripcion = ? WHERE id = ?',
        (nombre_lote, descripcion, lote_id)
    )
    conn.commit()
    conn.close()
    return jsonify({'message': 'Lote actualizado con éxito'})

# --- NUEVA RUTA ---
# Eliminar un lote
@current_app.route('/api/lotes/<int:lote_id>', methods=['DELETE'])
def delete_lote(lote_id):
    conn = get_db_connection()
    # Verificamos si el lote existe
    lote_existente = conn.execute('SELECT id FROM Lotes WHERE id = ?', (lote_id,)).fetchone()
    if lote_existente is None:
        conn.close()
        return jsonify({'error': 'Lote no encontrado'}), 404
        
    conn.execute('DELETE FROM Lotes WHERE id = ?', (lote_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Lote eliminado con éxito'})





# =======================================
# RUTAS DE INTERACCIÓN ENTRE MÓDULOS
# =======================================

# --- NUEVA RUTA ---
# Asignar un animal a un lote
@current_app.route('/api/lotes/<int:lote_id>/animales', methods=['POST'])
def assign_animal_to_lote(lote_id):
    data = request.get_json()
    animal_id = data.get('animal_id')

    if not animal_id:
        return jsonify({'error': 'El animal_id es obligatorio'}), 400

    conn = get_db_connection()
    # Verificamos que tanto el lote como el animal existan
    lote = conn.execute('SELECT * FROM Lotes WHERE id = ?', (lote_id,)).fetchone()
    if lote is None:
        conn.close()
        return jsonify({'error': 'Lote no encontrado'}), 404
    
    animal = conn.execute('SELECT * FROM Animales WHERE id = ?', (animal_id,)).fetchone()
    if animal is None:
        conn.close()
        return jsonify({'error': 'Animal no encontrado'}), 404

    # Actualizamos el campo lote_id en la tabla Animales
    conn.execute('UPDATE Animales SET lote_id = ? WHERE id = ?', (lote_id, animal_id))
    conn.commit()
    conn.close()

    return jsonify({'message': f'Animal {animal_id} asignado al lote {lote_id} con éxito'})



# ... (código anterior está arriba)

# --- NUEVA RUTA ---
# Obtener todos los animales de un lote específico
@current_app.route('/api/lotes/<int:lote_id>/animales')
def get_animales_by_lote(lote_id):
    conn = get_db_connection()
    # Verificamos que el lote exista
    lote = conn.execute('SELECT * FROM Lotes WHERE id = ?', (lote_id,)).fetchone()
    if lote is None:
        conn.close()
        return jsonify({'error': 'Lote no encontrado'}), 404

    # Si el lote existe, buscamos todos los animales con ese lote_id
    animales_cursor = conn.execute('SELECT * FROM Animales WHERE lote_id = ?', (lote_id,)).fetchall()
    conn.close()

    animales_lista = [dict(row) for row in animales_cursor]
    return jsonify(animales_lista)




# =======================================
# RUTAS PARA EL MÓDULO DE ALIMENTACION
# =======================================

# --- NUEVA RUTA ---
# Obtener todos los registros de alimentación de un lote
@current_app.route('/api/lotes/<int:lote_id>/alimentacion')
def get_alimentacion_by_lote(lote_id):
    conn = get_db_connection()
    # Verificamos que el lote exista
    lote = conn.execute('SELECT * FROM Lotes WHERE id = ?', (lote_id,)).fetchone()
    if lote is None:
        conn.close()
        return jsonify({'error': 'Lote no encontrado'}), 404

    # Buscamos todos los registros de alimentación con ese lote_id
    registros_cursor = conn.execute('SELECT * FROM Alimentacion WHERE lote_id = ?', (lote_id,)).fetchall()
    conn.close()

    registros_lista = [dict(row) for row in registros_cursor]
    return jsonify(registros_lista)




# --- NUEVA RUTA ---
# Registrar un nuevo evento de alimentación para un lote
@current_app.route('/api/lotes/<int:lote_id>/alimentacion', methods=['POST'])
def add_alimentacion_to_lote(lote_id):
    data = request.get_json()

    fecha = data.get('fecha')
    tipo_alimento = data.get('tipo_alimento')
    cantidad_kg = data.get('cantidad_kg')
    costo_total = data.get('costo_total') # Opcional

    if not fecha or not tipo_alimento or not cantidad_kg:
        return jsonify({'error': 'La fecha, tipo_alimento y cantidad_kg son obligatorios'}), 400

    conn = get_db_connection()
    # Verificamos que el lote exista
    lote = conn.execute('SELECT * FROM Lotes WHERE id = ?', (lote_id,)).fetchone()
    if lote is None:
        conn.close()
        return jsonify({'error': 'Lote no encontrado'}), 404

    # Insertamos el nuevo registro de alimentación
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO Alimentacion (lote_id, fecha, tipo_alimento, cantidad_kg, costo_total) VALUES (?, ?, ?, ?, ?)',
        (lote_id, fecha, tipo_alimento, cantidad_kg, costo_total)
    )
    conn.commit()
    new_alimentacion_id = cursor.lastrowid
    conn.close()

    return jsonify({'message': 'Registro de alimentación creado con éxito', 'id': new_alimentacion_id}), 201



# --- NUEVA RUTA ---
# Actualizar un registro de alimentación específico
@current_app.route('/api/alimentacion/<int:registro_id>', methods=['PUT'])
def update_alimentacion_registro(registro_id):
    data = request.get_json()
    
    fecha = data.get('fecha')
    tipo_alimento = data.get('tipo_alimento')
    cantidad_kg = data.get('cantidad_kg')
    costo_total = data.get('costo_total')

    if not fecha or not tipo_alimento or not cantidad_kg:
        return jsonify({'error': 'La fecha, tipo_alimento y cantidad_kg son obligatorios'}), 400

    conn = get_db_connection()
    # Verificamos si el registro existe
    registro_existente = conn.execute('SELECT id FROM Alimentacion WHERE id = ?', (registro_id,)).fetchone()
    if registro_existente is None:
        conn.close()
        return jsonify({'error': 'Registro de alimentación no encontrado'}), 404

    conn.execute(
        'UPDATE Alimentacion SET fecha = ?, tipo_alimento = ?, cantidad_kg = ?, costo_total = ? WHERE id = ?',
        (fecha, tipo_alimento, cantidad_kg, costo_total, registro_id)
    )
    conn.commit()
    conn.close()
    return jsonify({'message': 'Registro de alimentación actualizado con éxito'})

# --- NUEVA RUTA ---
# Eliminar un registro de alimentación
@current_app.route('/api/alimentacion/<int:registro_id>', methods=['DELETE'])
def delete_alimentacion_registro(registro_id):
    conn = get_db_connection()
    # Verificamos si el registro existe
    registro_existente = conn.execute('SELECT id FROM Alimentacion WHERE id = ?', (registro_id,)).fetchone()
    if registro_existente is None:
        conn.close()
        return jsonify({'error': 'Registro de alimentación no encontrado'}), 404

    conn.execute('DELETE FROM Alimentacion WHERE id = ?', (registro_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Registro de alimentación eliminado con éxito'})




# =======================================
# RUTAS PARA EL MÓDULO DE SANIDAD
# =======================================

# --- Crear un nuevo registro de sanidad ---
@current_app.route('/api/sanidad', methods=['POST'])
def create_sanidad_registro():
    data = request.get_json()
    
    animal_id = data.get('animal_id')
    lote_id = data.get('lote_id')
    fecha_tratamiento = data.get('fecha_tratamiento')
    producto = data.get('producto')
    tipo_tratamiento = data.get('tipo_tratamiento')
    dosis = data.get('dosis')
    periodo_resguardo_dias = data.get('periodo_resguardo_dias')
    notas = data.get('notas')

    if not fecha_tratamiento or not producto:
        return jsonify({'error': 'La fecha_tratamiento y el producto son obligatorios'}), 400
    if not animal_id and not lote_id:
        return jsonify({'error': 'Se debe especificar un animal_id o un lote_id'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''INSERT INTO Sanidad (animal_id, lote_id, fecha_tratamiento, producto, tipo_tratamiento, dosis, periodo_resguardo_dias, notas) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
        (animal_id, lote_id, fecha_tratamiento, producto, tipo_tratamiento, dosis, periodo_resguardo_dias, notas)
    )
    conn.commit()
    new_registro_id = cursor.lastrowid
    conn.close()
    return jsonify({'message': 'Registro de sanidad creado con éxito', 'id': new_registro_id}), 201



# --- Obtener todos los registros de sanidad de un animal ---
@current_app.route('/api/animales/<int:animal_id>/sanidad')
def get_sanidad_by_animal(animal_id):
    conn = get_db_connection()
    registros = conn.execute('SELECT * FROM Sanidad WHERE animal_id = ?', (animal_id,)).fetchall()
    conn.close()
    return jsonify([dict(row) for row in registros])


# --- Obtener todos los registros de sanidad de un lote ---
@current_app.route('/api/lotes/<int:lote_id>/sanidad')
def get_sanidad_by_lote(lote_id):
    conn = get_db_connection()
    registros = conn.execute('SELECT * FROM Sanidad WHERE lote_id = ?', (lote_id,)).fetchall()
    conn.close()
    return jsonify([dict(row) for row in registros])


# --- Actualizar un registro de sanidad ---
@current_app.route('/api/sanidad/<int:registro_id>', methods=['PUT'])
def update_sanidad_registro(registro_id):
    data = request.get_json()
    
    # Extraemos todos los datos del JSON que se envía
    animal_id = data.get('animal_id')
    lote_id = data.get('lote_id')
    fecha_tratamiento = data.get('fecha_tratamiento')
    producto = data.get('producto')
    tipo_tratamiento = data.get('tipo_tratamiento')
    dosis = data.get('dosis')
    periodo_resguardo_dias = data.get('periodo_resguardo_dias')
    notas = data.get('notas')

    # Validación de datos obligatorios
    if not fecha_tratamiento or not producto:
        return jsonify({'error': 'La fecha_tratamiento y el producto son obligatorios'}), 400
    if not animal_id and not lote_id:
        return jsonify({'error': 'Se debe especificar un animal_id o un lote_id'}), 400

    conn = get_db_connection()
    # Verificamos que el registro que queremos actualizar realmente exista
    registro_existente = conn.execute('SELECT id FROM Sanidad WHERE id = ?', (registro_id,)).fetchone()
    if registro_existente is None:
        conn.close()
        return jsonify({'error': 'Registro de sanidad no encontrado'}), 404

    # Si existe, procedemos a actualizarlo con el comando UPDATE
    conn.execute(
        '''UPDATE Sanidad SET animal_id = ?, lote_id = ?, fecha_tratamiento = ?, producto = ?, tipo_tratamiento = ?, dosis = ?, periodo_resguardo_dias = ?, notas = ? WHERE id = ?''',
        (animal_id, lote_id, fecha_tratamiento, producto, tipo_tratamiento, dosis, periodo_resguardo_dias, notas, registro_id)
    )
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Registro de sanidad actualizado con éxito'})


# --- Eliminar un registro de sanidad ---
@current_app.route('/api/sanidad/<int:registro_id>', methods=['DELETE'])
def delete_sanidad_registro(registro_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM Sanidad WHERE id = ?', (registro_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Registro de sanidad eliminado con éxito'})






# =======================================
# RUTAS PARA EL MÓDULO DE EVENTOS REPRODUCTIVOS
# =======================================

# --- Crear un nuevo evento reproductivo ---
@current_app.route('/api/eventos-reproductivos', methods=['POST'])
def create_evento_reproductivo():
    data = request.get_json()
    
    animal_id = data.get('animal_id')
    tipo_evento = data.get('tipo_evento')
    fecha_evento = data.get('fecha_evento')
    resultado = data.get('resultado')
    notas = data.get('notas')

    if not animal_id or not tipo_evento or not fecha_evento:
        return jsonify({'error': 'animal_id, tipo_evento y fecha_evento son obligatorios'}), 400

    conn = get_db_connection()
    # Verificamos que el animal exista y sea reproductor
    animal = conn.execute('SELECT * FROM Animales WHERE id = ? AND es_reproductor = 1', (animal_id,)).fetchone()
    if animal is None:
        conn.close()
        return jsonify({'error': 'Animal no encontrado o no está marcado como reproductor'}), 404

    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO Eventos_Reproductivos (animal_id, tipo_evento, fecha_evento, resultado, notas) VALUES (?, ?, ?, ?, ?)',
        (animal_id, tipo_evento, fecha_evento, resultado, notas)
    )
    conn.commit()
    new_evento_id = cursor.lastrowid
    conn.close()
    return jsonify({'message': 'Evento reproductivo creado con éxito', 'id': new_evento_id}), 201

# --- Obtener todos los eventos de un animal ---
@current_app.route('/api/animales/<int:animal_id>/eventos-reproductivos')
def get_eventos_by_animal(animal_id):
    conn = get_db_connection()
    eventos = conn.execute('SELECT * FROM Eventos_Reproductivos WHERE animal_id = ?', (animal_id,)).fetchall()
    conn.close()
    return jsonify([dict(row) for row in eventos])

# --- Eliminar un evento reproductivo ---
@current_app.route('/api/eventos-reproductivos/<int:evento_id>', methods=['DELETE'])
def delete_evento_reproductivo(evento_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM Eventos_Reproductivos WHERE id = ?', (evento_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Evento reproductivo eliminado con éxito'})




# ... (código anterior está arriba)

# =======================================
# RUTAS PARA EL MÓDULO DE REPORTES
# =======================================

# --- Crear un registro de reporte (simulado) ---
@current_app.route('/api/reportes', methods=['POST'])
def create_reporte_log():
    data = request.get_json()
    tipo_reporte = data.get('tipo_reporte')
    parametros = data.get('parametros')
    
    if not tipo_reporte:
        return jsonify({'error': 'El tipo_reporte es obligatorio'}), 400

    # Simulación: En un futuro, aquí iría la lógica para generar el PDF/Excel
    # y esta ruta sería la real donde se guardaría el archivo.
    ruta_archivo_simulada = f"/reports/{tipo_reporte.lower().replace(' ', '_')}_{request.date.strftime('%Y%m%d')}.pdf"

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO Reportes (tipo_reporte, parametros, ruta_archivo) VALUES (?, ?, ?)',
        (tipo_reporte, parametros, ruta_archivo_simulada)
    )
    conn.commit()
    new_reporte_id = cursor.lastrowid
    conn.close()
    return jsonify({'message': 'Registro de reporte creado con éxito', 'id': new_reporte_id, 'ruta_simulada': ruta_archivo_simulada}), 201

# --- Obtener todos los registros de reportes ---
@current_app.route('/api/reportes')
def get_reportes():
    conn = get_db_connection()
    reportes = conn.execute('SELECT * FROM Reportes').fetchall()
    conn.close()
    return jsonify([dict(row) for row in reportes])



