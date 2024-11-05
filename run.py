from app import app
from app.api_routes import api_bp
from app.page_routes import page_bp

app.register_blueprint(api_bp)
app.register_blueprint(page_bp)

if __name__ == "__main__":
    app.run(debug=False)
