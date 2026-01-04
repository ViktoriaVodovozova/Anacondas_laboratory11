from flaskr import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # или любой другой порт: 8000, 3000 и т.д.