def validate_login(self):
    """
    Valida el inicio de sesión del usuario y abre la pantalla principal

    Verifica que el usuario y la contraseña sean válidos y que el usuario esté
    activo. Si todo es correcto, cierra la pantalla de inicio de sesión y abre
    la pantalla principal con el rol del usuario.
    """
    username = self.username_entry.get()
    password = self.password_entry.get()

    # Conectar con la base de datos
    conn = sqlite3.connect("erp_ventas.db")
    cursor = conn.cursor()

    # Consultar si el usuario y la contraseña son válidos
    cursor.execute('''
        SELECT rol FROM usuarios WHERE nombre_usuario = ? AND contrasena = ? AND activo = 1
    ''', (username, password))
    user = cursor.fetchone()

    # Cerrar conexión
    conn.close()

    if user:
        rol = user[0]
        # Mostrar mensaje de inicio de sesión exitoso
        self.error_label.configure(text="¡Inicio de sesión exitoso!", text_color="green")
        # Cerrar la pantalla de inicio de sesión
        self.destroy()
        # Abrir la pantalla principal con el rol del usuario
        MainApp(rol).mainloop()  
    else:
        # Mostrar mensaje de error
        self.error_label.configure(text="Usuario o contraseña incorrectos", text_color="red")
