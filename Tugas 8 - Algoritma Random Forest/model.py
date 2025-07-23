from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

# Ekstraksi fitur dari dataset
X_train = [extract_features(img_path) for img_path in train_images]
y_train = [...]  # Label sesuai folder

# Bangun model
model = make_pipeline(
    StandardScaler(),
    RandomForestClassifier(n_estimators=150, max_depth=20, random_state=42)
)
model.fit(X_train, y_train)

# Simpan model
import joblib
joblib.dump(model, 'garbage_classifier.pkl')